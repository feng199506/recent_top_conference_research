"""Shared helpers for recent_top_conference_research.

Five-year window is judged by official conference publication date.
arXiv v1 is recorded separately and is not the inclusion criterion.
"""
import fcntl
import hashlib
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CACHE = SCRIPTS / "cache"
STATE = SCRIPTS / "state"
SEEDS = SCRIPTS / "seeds"
WORK = Path(os.environ.get("RTCR_WORK", "/root/.cache/rtcr_lit"))
STAGING = WORK / "staging"
PYLIB = WORK / "pylib"
LOCK_DIR = WORK / "locks"
LISTINGS = WORK / "listings"
META = WORK / "meta"
TEXT = WORK / "text"
SHARED_LOCKS = {"arxiv.org": Path("/root/.cache/ipm_lit/locks/arxiv.org")}
UA = ("Mozilla/5.0 (compatible; rtcr_recent_top_conference_research/1.0; "
      "personal study library, low request rate)")

SEARCH_DATE = "2026-10-30"
WINDOW_START, WINDOW_END = "2021-10-30", "2026-10-30"

CATS = {
    "01": ("gp_probml_uncertainty", "高斯过程、概率机器学习与不确定性",
           ["ICML", "NeurIPS", "ICLR", "COLT"], ["AISTATS", "UAI"]),
    "02": ("timeseries_spatiotemporal_env", "时间序列、空间时间预测及环境应用",
           ["ICML", "NeurIPS", "ICLR", "KDD", "AAAI", "IJCAI"], []),
    "03": ("industrial_process_monitoring", "工业过程监控",
           ["ICML", "NeurIPS", "ICLR", "KDD", "AAAI", "IJCAI"], []),
    "04": ("llm_multimodal", "大语言模型与多模态",
           ["ICML", "NeurIPS", "ICLR", "ACL", "EMNLP", "CVPR", "ICCV", "ECCV"], []),
    "05": ("coding_software_agents", "Coding 与软件智能体",
           ["ICSE", "FSE", "ASE", "ISSTA", "ACL", "EMNLP", "ICLR", "ICML", "NeurIPS"], []),
    "06": ("systems_mlsys", "训练、推理及生产系统",
           ["SOSP", "OSDI", "NSDI", "ASPLOS", "ISCA", "SC"], ["MLSys"]),
    "07": ("robotics_uav_control", "机器人、无人机与学习控制",
           ["RSS", "CoRL", "ICRA", "IROS"], ["L4DC", "CDC", "ACC"]),
}

SIBLINGS = [
    Path("/root/gaussian_process_literature"),
    Path("/root/industrial_process_monitoring_literature"),
    Path("/root/ai_undergraduate_graduate_curriculum_literature"),
    Path("/root/probability_statistics_curriculum_literature"),
]

INTERVAL = {
    "arxiv.org": 5.0,
    "api.crossref.org": 1.5,
    "api.github.com": 2.5,
    "github.com": 1.5,
    "raw.githubusercontent.com": 1.0,
    "proceedings.mlr.press": 1.5,
    "papers.nips.cc": 1.5,
    "openreview.net": 2.0,
    "openaccess.thecvf.com": 1.5,
    "aclanthology.org": 1.5,
    "export.arxiv.org": 5.0,
}

STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "via", "by", "is", "are",
        "from", "at", "as", "its", "do", "how", "can", "using", "based", "towards", "toward", "under",
        "through", "into", "over", "after", "before", "between", "without", "within"}

MAIN_TRACK_OK = {
    "main", "conference", "oral", "poster", "spotlight", "long", "main conference track",
    "datasets and benchmarks", "datasets and benchmarks track",
}
MAIN_TRACK_NO = {
    "workshop", "findings", "demo", "demonstration", "short", "tiny", "tiny paper",
    "competition", "challenge", "blog", "shared task", "industry track", "doctoral",
    "tutorial", "abstract", "extended abstract",
}


def cat_dir(cat):
    return f"{cat}_{CATS[cat][0]}"


def cat_label(cat):
    return f"{cat} {CATS[cat][1]}"


def host_key(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    if host.endswith("arxiv.org"):
        return "arxiv.org"
    return host


def wait(key, interval):
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    path = SHARED_LOCKS.get(key) or LOCK_DIR / re.sub(r"[^A-Za-z0-9._-]", "_", key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        raw = f.read().strip()
        try:
            last = float(raw) if raw else 0.0
        except ValueError:
            last = 0.0
        delay = interval - (time.time() - last)
        if delay > 0:
            time.sleep(delay)
        f.seek(0)
        f.truncate()
        f.write(str(time.time()))


def http(url, accept="*/*", timeout=120, tries=3, headers=None, max_bytes=200_000_000):
    """Return (status, body_bytes, final_url, content_type)."""
    key = host_key(url)
    err = ""
    for attempt in range(tries):
        wait(key, INTERVAL.get(key, 2.0))
        try:
            h = {"User-Agent": UA, "Accept": accept, **(headers or {})}
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read(max_bytes), r.geturl(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            body = b""
            try:
                body = e.read(4096)
            except Exception:
                pass
            if e.code == 429:
                time.sleep(30 * (attempt + 1))
                continue
            if 400 <= e.code < 500:
                return e.code, body, url, ""
        except Exception as e:
            err = repr(e)[:200]
        time.sleep(6 * (attempt + 1))
    return None, err.encode(), url, ""


def get_json(url, **kw):
    st, body, _, _ = http(url, accept="application/json", **kw)
    if st != 200:
        return None
    try:
        return json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return None


def load(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("\u00ad", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def norm_title(s):
    s = norm(s).lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def has_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


def surname(name):
    name = norm(name)
    if not name:
        return ""
    if "," in name:
        return re.sub(r"[^A-Za-z\-]", "", name.split(",", 1)[0])
    parts = name.split()
    for p in reversed(parts):
        p = re.sub(r"[^A-Za-z\-]", "", p)
        if p and p.lower() not in {"jr", "sr", "ii", "iii", "iv"}:
            return p
    return re.sub(r"[^A-Za-z\-]", "", parts[-1])


def short_title(title, n=8):
    words = [w for w in re.findall(r"[A-Za-z0-9]+", title or "") if w.lower() not in STOP]
    out = "".join(w.capitalize() for w in words[:n]) or "Paper"
    return out[:80]


def title_tokens(title):
    return [w for w in re.findall(r"[A-Za-z0-9]+", (title or "").lower()) if w not in STOP and len(w) > 2]


def title_in_text(title, text, thresh=0.8):
    toks = title_tokens(title)
    if not toks:
        return 0.0
    blob = (text or "").lower()
    hit = sum(1 for t in toks if t in blob)
    return hit / len(toks)


def in_window(date_s):
    if not date_s:
        return None
    d = date_s[:10]
    if len(d) == 4:
        return None  # year-only: caller must flag
    if len(d) == 7:
        d = d + "-01"
    return WINDOW_START <= d <= WINDOW_END


def date_precision(date_s):
    if not date_s:
        return ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_s[:10]):
        return "日"
    if re.match(r"^\d{4}-\d{2}$", date_s[:7]):
        return "月"
    if re.match(r"^\d{4}$", date_s[:4]):
        return "年"
    return "未知"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def append_log(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")
