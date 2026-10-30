"""Download and verify PDFs; copy from sibling libraries when they match.

  python3 -I scripts/download_en.py papers 01
  python3 -I scripts/download_en.py status 01
"""
import csv
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import (CACHE, CATS, PYLIB, ROOT, SEEDS, SIBLINGS, STAGING, STATE, TEXT,  # noqa: E402
                       WORK, http, load, save, sha256_file, short_title, surname,
                       title_in_text)
from venues_en import meeting_date  # noqa: E402

sys.path.insert(0, str(PYLIB))
import logging  # noqa: E402
logging.getLogger("pypdf").setLevel(logging.ERROR)
from pypdf import PdfReader  # noqa: E402


def seed_path(cat):
    return SEEDS / f"{cat}_{CATS[cat][0]}_seed_cn.json"


def state_path(cat):
    return STATE / f"papers_{cat}_en.json"


def fail_csv():
    return ROOT / "download_failures_cn.csv"


FAIL_FIELDS = ["sid", "标题", "会议", "年份", "阶段", "URL", "状态码", "原因", "备注"]


def log_fail(row):
    path = fail_csv()
    new = not path.exists()
    with open(path, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FAIL_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in FAIL_FIELDS})


def verify_pdf(path, title, authors):
    raw = path.read_bytes()
    if not raw.startswith(b"%PDF"):
        return False, "非 PDF 头"
    try:
        r = PdfReader(str(path))
        n = len(r.pages)
        head = []
        for i, p in enumerate(r.pages[: min(3, n)]):
            head.append(p.extract_text() or "")
        full = "\n".join(head)
        all_chars = 0
        for p in r.pages[: min(12, n)]:
            all_chars += len(p.extract_text() or "")
        if n < 4:
            return False, f"页数不足 {n}"
        if all_chars < 8000:
            return False, f"可提取字符不足 {all_chars}"
        sim = title_in_text(title, full)
        if sim < 0.8:
            return False, f"标题匹配 {sim:.2f}"
        sn = surname(authors[0] if authors else "")
        def fold(s):
            import unicodedata
            return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
        if sn and fold(sn) not in fold(full) and fold(sn) not in fold(title) and sn.lower() not in full.lower():
            return "pending", f"第一作者姓氏未在首页检出（{sn}）"
        blob = full.lower()
        if "supplementary" in blob and "references" not in blob and n < 8:
            return False, "疑似补充材料首页"
        return True, f"通过：%PDF；pypdf {n} 页、{all_chars} 字符；标题匹配 {sim:.2f}"
    except Exception as e:
        return False, f"pypdf 解析失败 {e!r}"[:200]


def sibling_index():
    idx = load(CACHE / "sibling_index_en.json", None)
    if idx:
        return idx
    idx = {"by_arxiv": {}, "by_title": {}, "files": []}
    for lib in SIBLINGS:
        if not lib.exists():
            continue
        for pdf in lib.rglob("*.pdf"):
            rec = {"lib": lib.name, "path": str(pdf)}
            idx["files"].append(rec)
        cat = lib / "catalog_cn.csv"
        if cat.exists():
            with open(cat, encoding="utf-8-sig") as f:
                r = csv.DictReader(f)
                for row in r:
                    arx = (row.get("arXiv ID") or row.get("标识符") or "").strip()
                    m = re.search(r"(\d{4}\.\d{4,5})", arx)
                    path = row.get("本地相对路径") or row.get("本地路径") or ""
                    full = str(lib / path) if path else ""
                    title = row.get("标题") or ""
                    if m and full:
                        idx["by_arxiv"][m.group(1)] = {"path": full, "lib": lib.name, "title": title}
                    if title and full:
                        from common_en import norm_title
                        idx["by_title"][norm_title(title)] = {"path": full, "lib": lib.name, "title": title}
    save(CACHE / "sibling_index_en.json", idx)
    return idx


def try_reuse(p, idx):
    arx = p.get("arxiv") or ""
    hit = idx.get("by_arxiv", {}).get(arx)
    if not hit:
        from common_en import norm_title
        hit = idx.get("by_title", {}).get(norm_title(p.get("title", "")))
    if not hit:
        return None
    src = Path(hit["path"])
    if src.exists() and src.stat().st_size > 10000:
        return src, hit["lib"]
    return None


def dest_name(p):
    year = p.get("year") or (p.get("pub_date") or "0000")[:4]
    au = surname((p.get("authors") or ["Anon"])[0]) or "Anon"
    st = short_title(p.get("title", "Paper"))
    return f"{year}_{au}_{st}_en.pdf"


def download_one(p, idx):
    sid = p["sid"]
    dest = ROOT / "papers" / dest_name(p)
    reuse = try_reuse(p, idx)
    STAGING.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(STAGING)) as td:
        tmp = Path(td) / "paper.pdf"
        source_kind = "新下载"
        reused_lib = ""
        if reuse:
            src, lib = reuse
            shutil.copy2(src, tmp)
            source_kind = "已有复用"
            reused_lib = lib
        else:
            urls = []
            if p.get("pdf_url"):
                urls.append(p["pdf_url"])
            if p.get("arxiv"):
                urls.append(f"https://arxiv.org/pdf/{p['arxiv']}.pdf")
            last = ""
            ok = False
            for u in urls:
                st, body, final, ct = http(u, timeout=120, max_bytes=80_000_000)
                last = f"{st} {u}"
                if st == 200 and body.startswith(b"%PDF"):
                    tmp.write_bytes(body)
                    p["downloaded_from"] = final
                    ok = True
                    break
                # USENIX presentation pages and similar HTML with a PDF link
                if st == 200 and body and not body.startswith(b"%PDF"):
                    html = body.decode("utf-8", "replace")
                    pdfs = re.findall(r'href="(https?://[^"]+\.pdf)"', html)
                    pdfs += ["https://www.usenix.org" + x if x.startswith("/") else x
                             for x in re.findall(r'href="(/[^"]+\.pdf)"', html)]
                    pdfs = [x for x in pdfs if "proceedings_cover" not in x and "full_proceedings" not in x
                            and "supplement" not in x.lower()]
                    for pu in pdfs[:3]:
                        st2, b2, fin2, _ = http(pu, timeout=120, max_bytes=80_000_000)
                        last = f"{st2} {pu}"
                        if st2 == 200 and b2.startswith(b"%PDF"):
                            tmp.write_bytes(b2)
                            p["downloaded_from"] = fin2
                            ok = True
                            break
                    if ok:
                        break
            if not ok:
                log_fail({"sid": sid, "标题": p.get("title", ""), "会议": p.get("venue", ""),
                          "年份": p.get("year", ""), "阶段": "pdf", "URL": p.get("pdf_url", ""),
                          "状态码": last, "原因": "下载失败或非 PDF", "备注": ""})
                return {"sid": sid, "status": "fail", "detail": last}
        ok, detail = verify_pdf(tmp, p.get("title", ""), p.get("authors") or [])
        if ok is False:
            log_fail({"sid": sid, "标题": p.get("title", ""), "会议": p.get("venue", ""),
                      "年份": p.get("year", ""), "阶段": "verify", "URL": p.get("pdf_url", ""),
                      "状态码": "", "原因": detail, "备注": source_kind})
            return {"sid": sid, "status": "fail", "detail": detail}
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp, dest)
        rec = {
            "sid": sid, "status": "ok" if ok is True else "pending",
            "detail": detail, "path": str(dest.relative_to(ROOT)),
            "sha256": sha256_file(dest), "source_kind": source_kind,
            "reused_lib": reused_lib, "bytes": dest.stat().st_size,
        }
        # keep first-page text for github extraction
        try:
            r = PdfReader(str(dest))
            t = "\n".join((pg.extract_text() or "") for pg in r.pages[:2])
            (TEXT / f"{sid}.txt").write_text(t, encoding="utf-8")
        except Exception:
            pass
        return rec


def cmd_papers(cat):
    seeds = load(seed_path(cat), [])
    st = load(state_path(cat), {})
    idx = sibling_index()
    n_ok = n_fail = n_reuse = 0
    for p in seeds:
        sid = p.get("sid")
        if not sid:
            continue
        prev = st.get(sid, {})
        if prev.get("status") in {"ok", "pending"} and Path(ROOT / prev.get("path", "missing")).exists():
            n_ok += 1
            if prev.get("source_kind") == "已有复用":
                n_reuse += 1
            continue
        print(f"  {sid} {p.get('venue')} {p.get('year')} {p.get('title','')[:70]}")
        rec = download_one(p, idx)
        st[sid] = rec
        save(state_path(cat), st)
        if rec.get("status") in {"ok", "pending"}:
            n_ok += 1
            if rec.get("source_kind") == "已有复用":
                n_reuse += 1
        else:
            n_fail += 1
    print(f"{cat}: verified {n_ok} fail {n_fail} reused {n_reuse} / seeds {len(seeds)}")


def cmd_status(cat):
    st = load(state_path(cat), {})
    seeds = load(seed_path(cat), [])
    ok = sum(1 for v in st.values() if v.get("status") in {"ok", "pending"})
    print(f"{cat}: {ok}/{len(seeds)} papers on disk")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "papers":
        cmd_papers(argv[2])
    elif cmd == "status":
        cmd_status(argv[2])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
