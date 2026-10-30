"""Download official (or third-party) code snapshots and statically inspect them.

  python3 -I scripts/code_en.py fetch 01
  python3 -I scripts/code_en.py inspect 01

L0 = downloaded. L1 = entry/config/deps statically checked.
This round never claims runtime reproduction.
"""
import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import (CATS, ROOT, SEEDS, STATE, TEXT, WORK, http, load, save, surname)  # noqa: E402

GITHUB_RX = re.compile(r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", re.I)
BLOCK_OWNERS = {
    "mlresearch", "papers-neurips", "neuripsproceedings", "nipsproceedings",
    "iclr-conf", "icml-conf", "proceedings", "gist", "acl-org",
}
BLOCK_REPOS = {"acl-anthology", "anthology", "github"}
ENTRY_NAMES = {
    "train.py", "training.py", "run.py", "main.py", "fit.py", "experiment.py",
    "train.sh", "run.sh", "main.ipynb", "demo.py", "eval.py", "evaluate.py",
    "inference.py", "test.py", "predict.py",
}
CONFIG_NAMES = {
    "config.yaml", "config.yml", "config.json", "configs", "conf", "hydra",
    "default.yaml", "params.yaml", "argparse",
}
DEP_NAMES = {
    "requirements.txt", "environment.yml", "environment.yaml", "pyproject.toml",
    "setup.py", "setup.cfg", "Pipfile", "poetry.lock", "package.json",
    "Cargo.toml", "environment.lock.yml",
}
LICENSE_NAMES = {
    "license", "license.md", "license.txt", "copying", "copyright", "licence",
}


def seed_path(cat):
    return SEEDS / f"{cat}_{CATS[cat][0]}_seed_cn.json"


def paper_state(cat):
    return STATE / f"papers_{cat}_en.json"


def code_state(cat):
    return STATE / f"code_{cat}_en.json"


def run(cmd, cwd=None, timeout=180):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 99, repr(e)


def urls_from_text(text):
    out = []
    for m in GITHUB_RX.finditer(text or ""):
        owner, repo = m.group(1), m.group(2)
        repo = repo.rstrip(".").removesuffix(".git")
        if owner.lower() in BLOCK_OWNERS:
            continue
        if repo.lower() in BLOCK_REPOS or repo.lower() in {"github", "span", "https", "blob", "tree"}:
            continue
        if re.match(r"^v\d+$", repo.lower()):
            continue
        out.append(f"https://github.com/{owner}/{repo}")
    return list(dict.fromkeys(out))


def collect_urls(p, pst):
    urls = []
    urls += urls_from_text(" ".join(p.get("github_hint") or []))
    urls += urls_from_text(p.get("comment", ""))
    urls += urls_from_text(p.get("abstract", ""))
    sid = p.get("sid", "")
    tpath = TEXT / f"{sid}.txt"
    if tpath.exists():
        urls += urls_from_text(tpath.read_text("utf-8", "replace"))
    # unique
    clean = []
    for u in urls:
        u = u.split("#")[0].rstrip("/")
        if "/tree/" in u or "/blob/" in u:
            parts = u.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                u = f"https://github.com/{parts[0]}/{parts[1]}"
        if u not in clean:
            clean.append(u)
    return clean


def gh_api(path):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return http("https://api.github.com" + path, headers=headers, timeout=40)


def parse_gh_url(url):
    m = GITHUB_RX.search(url or "")
    if not m:
        return None, None
    return m.group(1), m.group(2).removesuffix(".git")


def official_guess(owner, authors):
    if not owner or not authors:
        return "未核实"
    ow = owner.lower().replace("-", "")
    surnames = [surname(a).lower() for a in authors if a]
    for s in surnames:
        if s and s in ow:
            return "疑似作者（仓库名含作者姓氏）"
    # org names commonly official
    if any(k in ow for k in ["google", "deepmind", "facebook", "meta", "microsoft",
                             "openai", "anthropic", "amazon", "nvidia", "ibm",
                             "cambridge", "oxford", "stanford", "mit", "cmu",
                             "cornell", "berkeley", "ucl", "imperial", "epfl",
                             "ethz", "inria", "turing", "vectorinstitute",
                             "gpytorch", "gpflow", "cornellius"]):
        return "疑似官方机构/实验室组织"
    return "未核实官方归属（仅仓库存在）"


def clone_repo(url, dest):
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        return True, "already"
    dest.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["GIT_LFS_SKIP_SMUDGE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    cmd = ["git", "clone", "--depth", "1", "--single-branch", "--no-recurse-submodules",
           url, str(dest)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=env)
        if p.returncode != 0:
            return False, (p.stderr or p.stdout or "")[:400]
        return True, "cloned"
    except subprocess.TimeoutExpired:
        shutil.rmtree(dest, ignore_errors=True)
        return False, "clone timeout"
    except Exception as e:
        shutil.rmtree(dest, ignore_errors=True)
        return False, repr(e)[:200]


def walk_limited(root, max_files=8000):
    files = []
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__",
                                                        ".venv", "venv", "data", "datasets",
                                                        "checkpoints", "weights", "wandb"}]
        for fn in filenames:
            n += 1
            if n > max_files:
                return files, True
            files.append(Path(dirpath) / fn)
    return files, False


def inspect_repo(dest, authors):
    files, truncated = walk_limited(dest)
    names = {f.name.lower(): f for f in files}
    rels = [str(f.relative_to(dest)).lower() for f in files]
    license_f = ""
    license_txt = ""
    for key in LICENSE_NAMES:
        for f in files:
            if f.name.lower() == key:
                license_f = str(f.relative_to(dest))
                try:
                    license_txt = f.read_text("utf-8", "replace")[:2000]
                except Exception:
                    license_txt = ""
                break
        if license_f:
            break
    lic_name = ""
    if license_txt:
        blob = license_txt.lower()
        for lab in ["mit license", "apache license", "bsd-3", "bsd 3", "gpl-3", "gpl-2",
                    "mozilla public", "cc-by", "cc by", "unlicense", "boost"]:
            if lab in blob:
                lic_name = lab
                break
        if not lic_name:
            lic_name = "有 LICENSE 文件但未识别 SPDX/常用名称"
    else:
        lic_name = "未发现许可证（不标为可自由复用）"

    entries = [r for r in rels if Path(r).name in ENTRY_NAMES or
               Path(r).name.endswith(("_train.py", "_eval.py"))]
    configs = [r for r in rels if any(c in r for c in ["config", "hydra", "conf/"]) and
               Path(r).suffix in {".yaml", ".yml", ".json", ".toml", ".cfg", ".ini"}]
    deps = [r for r in rels if Path(r).name.lower() in {x.lower() for x in DEP_NAMES}]
    readmes = [r for r in rels if Path(r).name.lower().startswith("readme")]
    tests = [r for r in rels if "/test" in r or r.startswith("test") or "/tests/" in r]
    notebooks = [r for r in rels if r.endswith(".ipynb")]
    gitmod = (dest / ".gitmodules").exists()
    lfs = any("filter=lfs" in f.read_text("utf-8", "replace")
              for f in files if f.name == ".gitattributes") if any(f.name == ".gitattributes" for f in files) else False

    code_kind = "D"
    note = []
    if entries and (configs or True) and (deps or True) and readmes:
        # distinguish complete vs partial
        missing = []
        if not entries:
            missing.append("训练/方法入口")
        if not deps:
            missing.append("依赖声明")
        if not configs:
            missing.append("配置（可能用 argparse）")
        if not tests:
            missing.append("测试")
        if missing and (not entries or not readmes):
            code_kind = "B"
            note = missing
        else:
            code_kind = "A"
            note = missing
    elif readmes or entries or notebooks:
        code_kind = "B"
        note = ["仅部分实现可见"]
    else:
        code_kind = "D"
        note = ["仓库空或无可识别实现"]

    l1_ok = bool(entries) and bool(deps or notebooks) and bool(readmes)
    return {
        "license_file": license_f,
        "license_name": lic_name,
        "readme": readmes[:5],
        "entries": entries[:12],
        "configs": configs[:12],
        "deps": deps[:8],
        "tests": tests[:8],
        "notebooks": notebooks[:8],
        "n_files": len(files),
        "truncated_listing": truncated,
        "has_gitmodules": gitmod,
        "has_lfs_pointers": lfs,
        "code_kind": code_kind,
        "missing": note,
        "level": "L1" if l1_ok else "L0",
        "l1_ok": l1_ok,
    }


def git_head(dest):
    rc, out = run(["git", "rev-parse", "HEAD"], cwd=dest, timeout=20)
    if rc == 0:
        return out.strip()[:40]
    return ""


def cmd_fetch(cat):
    seeds = load(seed_path(cat), [])
    pst = load(paper_state(cat), {})
    cst = load(code_state(cat), {})
    n_ok = n_fail = n_none = 0
    for p in seeds:
        sid = p.get("sid")
        if not sid:
            continue
        if cst.get(sid, {}).get("level") in {"L0", "L1"} and cst[sid].get("path"):
            dest = ROOT / cst[sid]["path"]
            if dest.exists():
                n_ok += 1
                continue
        urls = collect_urls(p, pst)
        print(f"  {sid} urls={urls[:3] or ['(none)']}", flush=True)
        if not urls:
            cst[sid] = {"sid": sid, "code_kind": "D", "level": "", "urls": [],
                        "note": "未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现"}
            n_none += 1
            save(code_state(cat), cst)
            continue
        ok_any = False
        for url in urls[:3]:
            owner, repo = parse_gh_url(url)
            if not owner:
                continue
            if owner.lower() in BLOCK_OWNERS or re.match(r"^v\d+$", (repo or "").lower()):
                continue
            folder = f"{sid}_{owner}_{repo}_en"
            dest = ROOT / "code" / folder
            ok, msg = clone_repo(url + ".git" if not url.endswith(".git") else url, dest)
            if not ok:
                # try without .git
                ok, msg = clone_repo(url, dest)
            if not ok:
                cst[sid] = {"sid": sid, "code_kind": "D", "level": "", "urls": urls,
                            "note": f"clone 失败 {msg[:180]}", "tried": url}
                continue
            insp = inspect_repo(dest, p.get("authors") or [])
            head = git_head(dest)
            evidence = official_guess(owner, p.get("authors") or [])
            kind = insp["code_kind"]
            if evidence.startswith("未核实") and kind in {"A", "B"}:
                kind = "C" if "作者" not in evidence else kind
                # keep A/B if author-like
            if evidence.startswith("疑似作者") or evidence.startswith("疑似官方"):
                pass
            else:
                # third party if we cannot link
                if kind in {"A", "B"}:
                    kind = "C"
                    insp["missing"] = list(insp.get("missing") or []) + ["官方归属未证实，按第三方实现登记"]
            rec = {
                **insp,
                "sid": sid, "url": url, "owner": owner, "repo": repo,
                "commit": head, "path": str(dest.relative_to(ROOT)),
                "official_evidence": evidence, "code_kind": kind,
            }
            cst[sid] = rec
            ok_any = True
            n_ok += 1
            print(f"  {sid} {kind} {insp['level']} {url} {head[:8]}")
            break
        if not ok_any:
            n_fail += 1
        save(code_state(cat), cst)
    print(f"{cat}: code ok {n_ok} fail {n_fail} none {n_none}")


def cmd_inspect(cat):
    cst = load(code_state(cat), {})
    n = 0
    for sid, rec in cst.items():
        path = rec.get("path")
        if not path:
            continue
        dest = ROOT / path
        if not dest.exists():
            continue
        insp = inspect_repo(dest, [])
        rec.update(insp)
        rec["commit"] = rec.get("commit") or git_head(dest)
        cst[sid] = rec
        n += 1
    save(code_state(cat), cst)
    print(f"re-inspected {n}")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "fetch":
        cmd_fetch(argv[2])
    elif cmd == "inspect":
        cmd_inspect(argv[2])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
