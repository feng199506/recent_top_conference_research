"""Discover candidate main-track papers from official proceedings and arXiv.

  python3 -I scripts/discover_en.py listings     # download/cache venue listings
  python3 -I scripts/discover_en.py scan 01      # score listings into candidates
  python3 -I scripts/discover_en.py arxiv 01     # ICLR (and gaps) via arXiv comments
  python3 -I scripts/discover_en.py enrich 01    # abstracts + github hints
  python3 -I scripts/discover_en.py select 01    # write seed json
"""
import html as htmlmod
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import (CACHE, CATS, LISTINGS, META, SEEDS, WINDOW_END, WINDOW_START,  # noqa: E402
                       append_log, http, load, norm, norm_title, save)
from keywords_en import relation_label, score_text  # noqa: E402
from venues_en import (ICLR_YEARS, NEURIPS_YEARS, PMLR_MAIN,  # noqa: E402
                       in_window_meeting, meeting_date)

VENUE_ALIAS = {
    "NIPS": "NeurIPS", "NEURIPS": "NeurIPS", "ESEC/FSE": "FSE", "ESEC": "FSE",
    "MLSYS": "MLSys", "CORL": "CoRL",
}
VENUE_FROM_TEXT = re.compile(
    r"\b(ICML|NeurIPS|NIPS|ICLR|COLT|AISTATS|UAI|KDD|AAAI|IJCAI|ACL|EMNLP|"
    r"CVPR|ICCV|ECCV|ICSE|FSE|ASE|ISSTA|SOSP|OSDI|NSDI|ASPLOS|ISCA|SC|MLSys|"
    r"RSS|CoRL|ICRA|IROS|L4DC|CDC|ACC|ESEC/FSE)\b\s*(20\d{2})",
    re.I)
PUBLISHED = re.compile(
    r"published as a conference paper|accepted (at|to|for)|proceedings of|"
    r"to appear in|appeared in",
    re.I)
SELECT_CAP = {
    "01": {"ICML": 28, "NeurIPS": 26, "ICLR": 22, "COLT": 8, "AISTATS": 16, "UAI": 12},
    "02": {"ICML": 22, "NeurIPS": 22, "ICLR": 18, "KDD": 16, "AAAI": 16, "IJCAI": 16},
    "03": {"ICML": 22, "NeurIPS": 22, "ICLR": 18, "KDD": 16, "AAAI": 16, "IJCAI": 16},
    "04": {"ICML": 16, "NeurIPS": 16, "ICLR": 16, "ACL": 16, "EMNLP": 16, "CVPR": 12, "ICCV": 10, "ECCV": 10},
    "05": {"ICSE": 18, "FSE": 14, "ASE": 14, "ISSTA": 12, "ACL": 14, "EMNLP": 12, "ICLR": 10, "ICML": 10, "NeurIPS": 10},
    "06": {"SOSP": 12, "OSDI": 14, "NSDI": 14, "ASPLOS": 16, "ISCA": 12, "SC": 12, "MLSys": 18},
    "07": {"RSS": 16, "CoRL": 18, "ICRA": 22, "IROS": 18, "L4DC": 14, "CDC": 12, "ACC": 10},
}
IJCAI_YEARS = [2022, 2023, 2024, 2025, 2026]

ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"
API = "https://export.arxiv.org/api/query?"
LOG = Path(__file__).resolve().parent.parent / "search_log_cn.md"


def cand_path(cat):
    return CACHE / f"candidates_{cat}_en.json"


def seed_path(cat):
    slug = CATS[cat][0]
    return SEEDS / f"{cat}_{slug}_seed_cn.json"


def listing_file(kind, key):
    return LISTINGS / f"{kind}_{key}.html"


# ---------------------------------------------------------------- PMLR
def fetch_pmlr_volume(vol):
    dest = listing_file("pmlr", f"v{vol}")
    if dest.exists() and dest.stat().st_size > 5000:
        return dest.read_text("utf-8", "replace")
    url = f"https://proceedings.mlr.press/v{vol}/"
    st, body, final, _ = http(url, timeout=90, max_bytes=12_000_000)
    if st != 200 or not body:
        print(f"  PMLR v{vol} failed {st}")
        return ""
    dest.write_bytes(body)
    print(f"  PMLR v{vol} {len(body)} bytes {final}")
    return body.decode("utf-8", "replace")


def parse_pmlr(vol, html):
    venue, year, track, rank = PMLR_MAIN[vol]
    ok, note, prec = in_window_meeting(venue, year)
    papers = []
    blocks = re.split(r'<div class="paper">', html)[1:]
    for b in blocks:
        tm = re.search(r'<p class="title">\s*(.*?)\s*</p>', b, re.S)
        am = re.search(r'<span class="authors">\s*(.*?)\s*</span>', b, re.S)
        if not tm:
            continue
        title = norm(htmlmod.unescape(re.sub(r"<[^>]+>", "", tm.group(1))))
        authors = []
        if am:
            raw = htmlmod.unescape(re.sub(r"<[^>]+>", " ", am.group(1)))
            authors = [norm(x) for x in re.split(r",|&nbsp;|;", raw.replace("\xa0", " ")) if norm(x)]
        abs_url, pdf_url = "", ""
        for href in re.findall(r'href="([^"]+)"', b):
            if href.endswith(".html") and "proceedings.mlr.press" in href and not abs_url:
                abs_url = href
            if href.endswith(".pdf") and not pdf_url:
                pdf_url = href
        pid = ""
        m = re.search(r"/v%d/([^/]+)\.html" % vol, abs_url or "")
        if m:
            pid = m.group(1)
        papers.append({
            "source": "pmlr",
            "venue": venue, "year": year, "track": track, "venue_rank_note": rank,
            "title": title, "authors": authors,
            "abs_url": abs_url, "pdf_url": pdf_url, "pmlr_id": pid, "pmlr_vol": vol,
            "window_ok": ok, "window_note": note, "date_precision": prec,
            "pub_date": meeting_date(venue, year)[0],
        })
    return papers


# ---------------------------------------------------------------- NeurIPS
def fetch_neurips(year):
    dest = listing_file("neurips", str(year))
    urls = [f"https://papers.nips.cc/paper_files/paper/{year}"]
    if year >= 2025:
        urls = [
            f"https://papers.nips.cc/paper_files/paper/{year}/vol{year-1987}-main-conference",
            f"https://papers.nips.cc/paper_files/paper/{year}/vol38-main-conference",
            f"https://papers.nips.cc/paper_files/paper/{year}",
        ]
    if dest.exists() and dest.stat().st_size > 200_000:
        return dest.read_text("utf-8", "replace")
    body = b""
    for url in urls:
        st, body, final, _ = http(url, timeout=90, max_bytes=12_000_000)
        html = (body or b"").decode("utf-8", "replace")
        if st == 200 and ("Abstract-Conference" in html or html.count("paper title") > 200):
            dest.write_bytes(body)
            print(f"  NeurIPS {year} {len(body)} bytes {final}")
            return html
        print(f"  NeurIPS {year} skip {st} {url} bytes={len(body or b'')}")
    if body:
        dest.write_bytes(body)
    return (body or b"").decode("utf-8", "replace")


def parse_neurips(year, html):
    ok, note, prec = in_window_meeting("NeurIPS", year)
    papers = []
    for m in re.finditer(
            r'<li class="([^"]+)" data-track="([^"]+)">\s*<div class="paper-content">\s*'
            r'<a title="paper title" href="([^"]+)">\s*(.*?)\s*</a>\s*'
            r'<span class="paper-authors">(.*?)</span>',
            html, re.S):
        css, track, href, title, authors = m.groups()
        title = norm(htmlmod.unescape(title))
        authors = [norm(htmlmod.unescape(x)) for x in authors.split(",") if norm(x)]
        track_l = htmlmod.unescape(track).lower()
        if "workshop" in track_l or "competition" in track_l or "demo" in track_l:
            continue
        if "conference" not in track_l and "datasets" not in track_l:
            continue
        hm = re.search(r"/hash/([0-9a-f]+)-Abstract-([A-Za-z0-9_]+)\.html", href)
        if not hm:
            continue
        hsh, kind = hm.group(1), hm.group(2)
        if kind not in {"Conference", "Datasets_and_Benchmarks_Track"}:
            continue
        pdf = (f"https://papers.nips.cc/paper_files/paper/{year}/file/"
               f"{hsh}-Paper-{kind}.pdf")
        abs_url = "https://papers.nips.cc" + href
        papers.append({
            "source": "neurips",
            "venue": "NeurIPS", "year": year,
            "track": "datasets_and_benchmarks" if "Datasets" in kind else "main",
            "venue_rank_note": "core",
            "title": title, "authors": authors,
            "abs_url": abs_url, "pdf_url": pdf, "nips_hash": hsh,
            "window_ok": ok, "window_note": note, "date_precision": prec,
            "pub_date": meeting_date("NeurIPS", year)[0],
        })
    return papers


# ---------------------------------------------------------------- arXiv (ICLR + comment confirmation)
ICLR_OK = re.compile(
    r"(published as a conference paper at iclr\s*(20\d{2})|"
    r"accepted (to|at|for) iclr\s*(20\d{2})|"
    r"published (in|at|as).{0,80}iclr\s*(20\d{2})|"
    r"international conference on learning representations\s*\(?iclr\)?\s*(20\d{2})|"
    r"iclr\s*(20\d{2})\s*(poster|oral|spotlight|conference)?)",
    re.I)
ICLR_BAD = re.compile(
    r"workshop|tiny paper|blogpost|blog post|under review|submitted to|withdraw|"
    r"rejected|findings",
    re.I)


def parse_arxiv_entries(body):
    out = []
    root = ET.fromstring(body)
    for e in root.findall(ATOM + "entry"):
        idtext = e.findtext(ATOM + "id") or ""
        if "/abs/" not in idtext:
            continue
        aid = idtext.rsplit("/abs/", 1)[-1]
        m = re.match(r"(.+?)v(\d+)$", aid)
        base, ver = (m.group(1), int(m.group(2))) if m else (aid, 1)
        pc = e.find(ARX + "primary_category")
        out.append({
            "arxiv": base,
            "title": " ".join((e.findtext(ATOM + "title") or "").split()),
            "authors": [a.findtext(ATOM + "name") for a in e.findall(ATOM + "author")],
            "v1_date": (e.findtext(ATOM + "published") or "")[:10],
            "latest_version": ver,
            "latest_date": (e.findtext(ATOM + "updated") or "")[:10],
            "journal_ref": (e.findtext(ARX + "journal_ref") or "").strip(),
            "doi": (e.findtext(ARX + "doi") or "").lower(),
            "comment": " ".join((e.findtext(ARX + "comment") or "").split()),
            "abstract": " ".join((e.findtext(ATOM + "summary") or "").split()),
            "primary": pc.get("term") if pc is not None else "",
            "pdf_url": f"https://arxiv.org/pdf/{base}.pdf",
            "abs_url": f"https://arxiv.org/abs/{base}",
        })
    total = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    return out, int(total or 0)


def arxiv_search(query, maxn=200):
    hits, start, total = [], 0, None
    while start < maxn:
        n = min(50, maxn - start)
        url = API + urllib.parse.urlencode({
            "search_query": query, "start": start, "max_results": n,
            "sortBy": "relevance", "sortOrder": "descending"})
        st, body, _, _ = http(url, accept="application/atom+xml", tries=4)
        if st != 200:
            print(f"  arXiv {st} for {query[:80]}")
            break
        ents, total = parse_arxiv_entries(body)
        if not ents:
            break
        hits.extend(ents)
        start += len(ents)
        if start >= total:
            break
    return hits, total or 0


def iclr_year_from_meta(comment, jr):
    blob = f"{comment} {jr}"
    if ICLR_BAD.search(comment) and not re.search(r"published as a conference paper at iclr", comment, re.I):
        if ICLR_BAD.search(comment):
            # still allow if explicit published-as
            if not re.search(r"published as a conference paper at iclr\s*20", comment, re.I):
                return None
    m = ICLR_OK.search(blob)
    if not m:
        return None
    for g in m.groups():
        if g and re.match(r"20\d{2}$", g):
            y = int(g)
            if y in ICLR_YEARS:
                return y
    # journal_ref like "ICLR 2024"
    m2 = re.search(r"ICLR\s*(20\d{2})", blob, re.I)
    if m2:
        y = int(m2.group(1))
        if y in ICLR_YEARS:
            return y
    return None


GITHUB_RX = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", re.I)


def normalize_venue(v):
    v = (v or "").strip()
    return VENUE_ALIAS.get(v.upper(), v if v in {"MLSys", "CoRL"} else v.upper() if v.upper() in VENUE_ALIAS.values() or True else v)


def venue_year_from_text(blob, allowed=None):
    if ICLR_BAD.search(blob or "") and not re.search(r"published as a conference paper at iclr", blob or "", re.I):
        if re.search(r"workshop|tiny paper|findings|demo", blob or "", re.I):
            return None, None
    m = VENUE_FROM_TEXT.search(blob or "")
    if not m:
        y = iclr_year_from_meta(blob, "")
        return ("ICLR", y) if y else (None, None)
    raw, year = m.group(1), int(m.group(2))
    venue = VENUE_ALIAS.get(raw.upper(), "NeurIPS" if raw.upper() == "NIPS" else raw)
    if venue == "ICLR" or raw.upper() == "ICLR":
        venue = "ICLR"
    if allowed and venue not in allowed and venue.upper() not in {a.upper() for a in allowed}:
        return None, None
    return venue, year


def github_urls(*texts):
    out = []
    for t in texts:
        for u in GITHUB_RX.findall(t or ""):
            u = u.rstrip(").,;")
            if "/gist/" in u.lower():
                continue
            out.append(u)
    return list(dict.fromkeys(out))


# ---------------------------------------------------------------- IJCAI (open proceedings)
def fetch_ijcai(year):
    dest = listing_file("ijcai", str(year))
    if dest.exists() and dest.stat().st_size > 20000:
        return dest.read_text("utf-8", "replace")
    url = f"https://www.ijcai.org/proceedings/{year}/"
    st, body, final, _ = http(url, timeout=90, max_bytes=12_000_000)
    if st != 200 or not body:
        print(f"  IJCAI {year} failed {st}")
        return ""
    dest.write_bytes(body)
    print(f"  IJCAI {year} {len(body)} bytes")
    return body.decode("utf-8", "replace")


def parse_ijcai(year, html):
    ok, note, prec = in_window_meeting("IJCAI", year)
    papers = []
    parts = re.split(r"<h3>(.*?)</h3>", html, flags=re.S | re.I)
    sections = []
    if len(parts) >= 3:
        for i in range(1, len(parts), 2):
            sections.append((norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", parts[i]))), parts[i + 1] if i + 1 < len(parts) else ""))
    else:
        sections = [("Main Track", html)]
    for heading, body in sections:
        hl = heading.lower()
        if any(x in hl for x in ["survey", "demo", "doctoral", "sister", "early career", "workshop"]):
            continue
        track = "main" if "main" in hl or heading == "Main Track" else heading[:40]
        if track != "main":
            # IJCAI special tracks are not the main research track
            continue
        for block in re.split(r'<div class="paper_wrapper', body)[1:]:
            tm = re.search(r'<a class="title"[^>]*>\s*(.*?)\s*</a>', block, re.S)
            if not tm:
                continue
            title = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", tm.group(1))))
            authors = [norm(htmlmod.unescape(a)) for a in re.findall(r'<div class="authors">.*?</div>', block, re.S)]
            aus = []
            am = re.search(r'<div class="authors">(.*?)</div>', block, re.S)
            if am:
                aus = [norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", x))) for x in re.split(r",", am.group(1)) if norm(re.sub(r"<[^>]+>", " ", x))]
            pm = re.search(r'href="([^"]+\.pdf)"', block)
            if not pm:
                continue
            href = pm.group(1)
            pdf = href if href.startswith("http") else "https://www.ijcai.org" + href
            dm = re.search(r'doi:(10\.[^<\s]+)', block)
            papers.append({
                "source": "ijcai", "venue": "IJCAI", "year": year, "track": "main",
                "venue_rank_note": "core", "title": title, "authors": aus,
                "abs_url": f"https://www.ijcai.org/proceedings/{year}/",
                "pdf_url": pdf, "doi": dm.group(1) if dm else "",
                "window_ok": ok, "window_note": note,
                "date_precision": prec, "pub_date": meeting_date("IJCAI", year)[0],
            })
    return papers


# ---------------------------------------------------------------- ACL Anthology (long / main volumes only)
ACL_VOLUMES = [
    ("ACL", 2022, "2022.acl-long", "long"),
    ("ACL", 2023, "2023.acl-long", "long"),
    ("ACL", 2024, "2024.acl-long", "long"),
    ("ACL", 2025, "2025.acl-long", "long"),
    ("ACL", 2026, "2026.acl-long", "long"),
    ("EMNLP", 2021, "2021.emnlp-main", "main"),
    ("EMNLP", 2022, "2022.emnlp-main", "main"),
    ("EMNLP", 2023, "2023.emnlp-main", "main"),
    ("EMNLP", 2024, "2024.emnlp-main", "main"),
    ("EMNLP", 2025, "2025.emnlp-main", "main"),
    ("EMNLP", 2026, "2026.emnlp-main", "main"),
]

CVF_MAIN = [
    ("CVPR", 2022), ("CVPR", 2023), ("CVPR", 2024), ("CVPR", 2025), ("CVPR", 2026),
    ("ICCV", 2023), ("ICCV", 2025),
]
ECCV_YEARS = [2022, 2024, 2026]


def _unbrace_bib(s):
    s = re.sub(r"\s+", " ", s or "")
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return norm(htmlmod.unescape(s))


def _bib_field(block, name):
    m = re.search(rf'{name}\s*=\s*"((?:\\.|[^"\\])*)"', block, re.S)
    return _unbrace_bib(m.group(1)) if m else ""


def fetch_acl_bib(vol_id):
    dest = listing_file("acl", vol_id)
    if dest.exists() and dest.stat().st_size > 20000:
        return dest.read_text("utf-8", "replace")
    url = f"https://aclanthology.org/volumes/{vol_id}.bib"
    st, body, final, _ = http(url, timeout=90, max_bytes=20_000_000)
    if st != 200 or not body or b"@inproceedings" not in body:
        print(f"  ACL {vol_id} failed {st} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  ACL {vol_id} {len(body)} bytes")
    return body.decode("utf-8", "replace")


def parse_acl_bib(bib, venue, year, track):
    ok, note, prec = in_window_meeting(venue, year)
    papers = []
    chunks = re.split(r"(?=@inproceedings\{)", bib)
    for block in chunks:
        if not block.startswith("@inproceedings"):
            continue
        title = _bib_field(block, "title")
        if not title:
            continue
        authors_raw = _bib_field(block, "author")
        authors = [norm(a) for a in re.split(r"\s+and\s+", authors_raw) if norm(a)]
        url = _bib_field(block, "url").rstrip("/")
        if not url:
            continue
        pdf = url + ".pdf"
        doi = _bib_field(block, "doi")
        papers.append({
            "source": "acl_anthology", "venue": venue, "year": year,
            "track": track, "venue_rank_note": "core",
            "title": title, "authors": authors,
            "abs_url": url + "/", "pdf_url": pdf, "doi": doi,
            "window_ok": ok, "window_note": note,
            "date_precision": prec, "pub_date": meeting_date(venue, year)[0],
        })
    return papers


def fetch_cvf(venue, year):
    dest = listing_file("cvf", f"{venue}{year}")
    if dest.exists() and dest.stat().st_size > 100_000:
        return dest.read_text("utf-8", "replace")
    url = f"https://openaccess.thecvf.com/{venue}{year}?day=all"
    st, body, final, _ = http(url, timeout=120, max_bytes=40_000_000)
    html = (body or b"").decode("utf-8", "replace")
    if st != 200 or html.count('class="ptitle"') < 50:
        print(f"  CVF {venue} {year} failed {st} ptitle={html.count('class=\"ptitle\"')} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  CVF {venue} {year} {len(body)} bytes ptitle={html.count('class=\"ptitle\"')}")
    return html


def parse_cvf(venue, year, html):
    ok, note, prec = in_window_meeting(venue, year)
    papers = []
    for block in re.split(r'<dt class="ptitle">', html)[1:]:
        tm = re.search(r'<a href="([^"]+)">\s*(.*?)\s*</a>', block, re.S)
        if not tm:
            continue
        href, title = tm.group(1), norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", tm.group(2))))
        authors = [norm(htmlmod.unescape(a)) for a in re.findall(r'query_author" value="([^"]+)"', block)]
        pdfs = re.findall(r'href="([^"]+\.pdf)"', block)
        pdf = ""
        for p in pdfs:
            pl = p.lower()
            if "supplement" in pl or "supp" in pl:
                continue
            pdf = p
            break
        if not pdf or not title:
            continue
        if pdf.startswith("/"):
            pdf = "https://openaccess.thecvf.com" + pdf
        abs_url = href if href.startswith("http") else "https://openaccess.thecvf.com" + href
        papers.append({
            "source": "cvf", "venue": venue, "year": year, "track": "main",
            "venue_rank_note": "core", "title": title, "authors": authors,
            "abs_url": abs_url, "pdf_url": pdf,
            "window_ok": ok, "window_note": note,
            "date_precision": prec, "pub_date": meeting_date(venue, year)[0],
        })
    return papers


def fetch_eccv_all():
    dest = listing_file("eccv", "all")
    if dest.exists() and dest.stat().st_size > 80_000:
        return dest.read_text("utf-8", "replace")
    url = "https://www.ecva.net/papers.php"
    st, body, final, _ = http(url, timeout=120, max_bytes=40_000_000)
    html = (body or b"").decode("utf-8", "replace")
    if st != 200 or html.count('class="ptitle"') < 30:
        print(f"  ECCV all failed {st} ptitle={html.count('class=\"ptitle\"')} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  ECCV all {len(body)} bytes ptitle={html.count('class=\"ptitle\"')}")
    return html


def parse_eccv_all(html):
    papers = []
    for block in re.split(r'<dt class="ptitle">', html)[1:]:
        ym = re.search(r"eccv_(\d{4})", block)
        if not ym:
            continue
        year = int(ym.group(1))
        ok, note, prec = in_window_meeting("ECCV", year)
        if ok is False:
            continue
        tm = re.search(r'<a href=([^>\s]+)\s*>\s*(.*?)\s*</a>', block, re.S)
        if not tm:
            tm = re.search(r'<a href="([^"]+)">\s*(.*?)\s*</a>', block, re.S)
        if not tm:
            continue
        href, title = tm.group(1).strip("\"'"), norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", tm.group(2))))
        authors = []
        am = re.search(r"</dt>\s*<dd>\s*(.*?)\s*</dd>", block, re.S)
        if am:
            authors = [norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", x))) for x in re.split(r",|\*", am.group(1)) if norm(re.sub(r"<[^>]+>", " ", x))]
        pdfs = re.findall(r"href=['\"]([^'\"]+\.pdf)['\"]", block)
        pdf = ""
        for p in pdfs:
            if "supp" in p.lower():
                continue
            pdf = p
            break
        if not pdf or not title:
            continue
        if not pdf.startswith("http"):
            pdf = "https://www.ecva.net/" + pdf.lstrip("./")
        abs_url = href if href.startswith("http") else "https://www.ecva.net/" + href.lstrip("./")
        papers.append({
            "source": "ecva", "venue": "ECCV", "year": year, "track": "main",
            "venue_rank_note": "core", "title": title, "authors": authors,
            "abs_url": abs_url, "pdf_url": pdf,
            "window_ok": ok, "window_note": note,
            "date_precision": prec, "pub_date": meeting_date("ECCV", year)[0],
        })
    return papers


RSS_VOLS = [
    (2022, "rss18"), (2023, "rss19"), (2024, "rss20"),
    (2025, "rss21"), (2026, "rss22"),
]
MLSYS_YEARS = [2022, 2023, 2024, 2025, 2026]
USENIX_SESSIONS = [
    ("OSDI", 2022, "osdi22"), ("OSDI", 2023, "osdi23"), ("OSDI", 2024, "osdi24"),
    ("OSDI", 2025, "osdi25"), ("OSDI", 2026, "osdi26"),
    ("NSDI", 2022, "nsdi22"), ("NSDI", 2023, "nsdi23"), ("NSDI", 2024, "nsdi24"),
    ("NSDI", 2025, "nsdi25"), ("NSDI", 2026, "nsdi26"),
    ("SOSP", 2023, "sosp23"), ("SOSP", 2025, "sosp25"),
]


def fetch_rss(year, vol):
    dest = listing_file("rss", vol)
    if dest.exists() and dest.stat().st_size > 10000:
        return dest.read_text("utf-8", "replace")
    url = f"https://www.roboticsproceedings.org/{vol}/index.html"
    st, body, final, _ = http(url, timeout=90, max_bytes=8_000_000)
    html = (body or b"").decode("utf-8", "replace")
    if st != 200 or html.count(".pdf") < 10:
        print(f"  RSS {year} {vol} failed {st} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  RSS {year} {vol} {len(body)} bytes")
    return html


def parse_rss(year, vol, html):
    ok, note, prec = in_window_meeting("RSS", year)
    papers = []
    for m in re.finditer(
            r'<a href="(p\d+)\.html">\s*(.*?)\s*</a>\s*<br>\s*<i>(.*?)</i>',
            html, re.S | re.I):
        pid, title, authors = m.groups()
        title = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", title)))
        authors = [norm(htmlmod.unescape(x)) for x in re.split(r",|;", authors) if norm(x)]
        if not title:
            continue
        base = f"https://www.roboticsproceedings.org/{vol}/"
        papers.append({
            "source": "rss", "venue": "RSS", "year": year, "track": "main",
            "venue_rank_note": "core", "title": title, "authors": authors,
            "abs_url": base + pid + ".html", "pdf_url": base + pid + ".pdf",
            "window_ok": ok, "window_note": note, "date_precision": prec,
            "pub_date": meeting_date("RSS", year)[0],
        })
    return papers


def fetch_mlsys(year):
    dest = listing_file("mlsys", str(year))
    if dest.exists() and dest.stat().st_size > 5000:
        return dest.read_text("utf-8", "replace")
    url = f"https://proceedings.mlsys.org/paper/{year}"
    st, body, final, _ = http(url, timeout=90, max_bytes=12_000_000)
    html = (body or b"").decode("utf-8", "replace")
    if st != 200 or html.count("paper title") < 5:
        print(f"  MLSys {year} failed {st} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  MLSys {year} {len(body)} bytes")
    return html


def parse_mlsys(year, html):
    ok, note, prec = in_window_meeting("MLSys", year)
    papers = []
    for m in re.finditer(
            r'<li class="([^"]+)" data-track="([^"]+)">\s*<div class="paper-content">\s*'
            r'<a title="paper title" href="([^"]+)">\s*(.*?)\s*</a>\s*'
            r'<span class="paper-authors">(.*?)</span>',
            html, re.S):
        css, track, href, title, authors = m.groups()
        title = norm(htmlmod.unescape(title))
        authors = [norm(htmlmod.unescape(x)) for x in authors.split(",") if norm(x)]
        hm = re.search(r"/hash/([0-9a-f]+)-Abstract", href)
        if not hm:
            continue
        hsh = hm.group(1)
        pdf = (f"https://proceedings.mlsys.org/paper_files/paper/{year}/file/"
               f"{hsh}-Paper-Conference.pdf")
        abs_url = href if href.startswith("http") else "https://proceedings.mlsys.org" + href
        papers.append({
            "source": "mlsys", "venue": "MLSys", "year": year, "track": "main",
            "venue_rank_note": "supplement_venue", "title": title, "authors": authors,
            "abs_url": abs_url, "pdf_url": pdf, "mlsys_hash": hsh,
            "window_ok": ok, "window_note": note, "date_precision": prec,
            "pub_date": meeting_date("MLSys", year)[0],
        })
    return papers


def fetch_usenix(venue, year, slug):
    dest = listing_file("usenix", f"{venue}{year}")
    if dest.exists() and dest.stat().st_size > 20000:
        return dest.read_text("utf-8", "replace")
    url = f"https://www.usenix.org/conference/{slug}/technical-sessions"
    st, body, final, _ = http(url, timeout=90, max_bytes=12_000_000)
    html = (body or b"").decode("utf-8", "replace")
    if st != 200 or html.count("/presentation/") < 10:
        print(f"  USENIX {venue} {year} failed {st} {final}")
        return ""
    dest.write_bytes(body)
    print(f"  USENIX {venue} {year} {len(body)} bytes")
    return html


def parse_usenix(venue, year, slug, html):
    ok, note, prec = in_window_meeting(venue, year)
    papers = []
    seen = set()
    for href, title in re.findall(
            rf'<a href="(/conference/{slug}/presentation/[^"]+)"[^>]*>(.*?)</a>',
            html, re.S):
        title = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", title)))
        if not title or len(title) < 8:
            continue
        if href in seen:
            continue
        seen.add(href)
        low = title.lower()
        if any(x in low for x in ["keynote", "opening remarks", "break with", "continental breakfast",
                                  "poster session", "workshop", "tutorial"]):
            continue
        abs_url = "https://www.usenix.org" + href
        papers.append({
            "source": "usenix", "venue": venue, "year": year, "track": "main",
            "venue_rank_note": "core", "title": title, "authors": [],
            "abs_url": abs_url, "pdf_url": abs_url,
            "window_ok": ok, "window_note": note, "date_precision": prec,
            "pub_date": meeting_date(venue, year)[0],
        })
    return papers


# ---------------------------------------------------------------- commands
def cmd_listings():
    n = 0
    for vol, meta in PMLR_MAIN.items():
        venue, year, _, _ = meta
        ok, note, _ = in_window_meeting(venue, year)
        if ok is False:
            print(f"skip PMLR v{vol} {venue} {year}: {note}")
            continue
        html = fetch_pmlr_volume(vol)
        n += 1 if html else 0
    for y in NEURIPS_YEARS:
        html = fetch_neurips(y)
        n += 1 if html else 0
    for y in IJCAI_YEARS:
        ok, note, _ = in_window_meeting("IJCAI", y)
        if ok is False:
            continue
        html = fetch_ijcai(y)
        n += 1 if html else 0
    for venue, year, vol_id, track in ACL_VOLUMES:
        ok, _, _ = in_window_meeting(venue, year)
        if ok is False:
            continue
        bib = fetch_acl_bib(vol_id)
        n += 1 if bib else 0
    for venue, year in CVF_MAIN:
        ok, _, _ = in_window_meeting(venue, year)
        if ok is False:
            continue
        html = fetch_cvf(venue, year)
        n += 1 if html else 0
    html = fetch_eccv_all()
    n += 1 if html else 0
    for year, vol in RSS_VOLS:
        ok, _, _ = in_window_meeting("RSS", year)
        if ok is False:
            continue
        html = fetch_rss(year, vol)
        n += 1 if html else 0
    for y in MLSYS_YEARS:
        ok, _, _ = in_window_meeting("MLSys", y)
        if ok is False:
            continue
        html = fetch_mlsys(y)
        n += 1 if html else 0
    for venue, year, slug in USENIX_SESSIONS:
        ok, _, _ = in_window_meeting(venue, year)
        if ok is False:
            continue
        html = fetch_usenix(venue, year, slug)
        n += 1 if html else 0
    print(f"listings fetched/cached: {n}")
    append_log(LOG, f"\n## 列表抓取 {__import__('datetime').date.today()}\nPMLR 主会卷、NeurIPS {NEURIPS_YEARS}、IJCAI {IJCAI_YEARS}、ACL/EMNLP 主卷、CVF、ECCV 已缓存到 listings。\n")


def all_listing_papers(venues):
    papers = []
    for vol, meta in PMLR_MAIN.items():
        venue, year, _, _ = meta
        if venue not in venues:
            continue
        ok, note, _ = in_window_meeting(venue, year)
        if ok is False:
            continue
        dest = listing_file("pmlr", f"v{vol}")
        if not dest.exists():
            fetch_pmlr_volume(vol)
        html = dest.read_text("utf-8", "replace") if dest.exists() else ""
        if html:
            papers.extend(parse_pmlr(vol, html))
    if "NeurIPS" in venues:
        for y in NEURIPS_YEARS:
            dest = listing_file("neurips", str(y))
            if not dest.exists():
                fetch_neurips(y)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_neurips(y, html))
    if "IJCAI" in venues:
        for y in IJCAI_YEARS:
            ok, note, _ = in_window_meeting("IJCAI", y)
            if ok is False:
                continue
            dest = listing_file("ijcai", str(y))
            if not dest.exists():
                fetch_ijcai(y)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_ijcai(y, html))
    if any(v in venues for v in ("ACL", "EMNLP")):
        for venue, year, vol_id, track in ACL_VOLUMES:
            if venue not in venues:
                continue
            ok, _, _ = in_window_meeting(venue, year)
            if ok is False:
                continue
            dest = listing_file("acl", vol_id)
            if not dest.exists():
                fetch_acl_bib(vol_id)
            bib = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if bib:
                papers.extend(parse_acl_bib(bib, venue, year, track))
    if any(v in venues for v in ("CVPR", "ICCV")):
        for venue, year in CVF_MAIN:
            if venue not in venues:
                continue
            ok, _, _ = in_window_meeting(venue, year)
            if ok is False:
                continue
            dest = listing_file("cvf", f"{venue}{year}")
            if not dest.exists():
                fetch_cvf(venue, year)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_cvf(venue, year, html))
    if "ECCV" in venues:
        dest = listing_file("eccv", "all")
        if not dest.exists():
            fetch_eccv_all()
        html = dest.read_text("utf-8", "replace") if dest.exists() else ""
        if not html:
            # leftover per-year copies from an earlier fetch of the same index
            for y in ECCV_YEARS:
                alt = listing_file("eccv", str(y))
                if alt.exists():
                    html = alt.read_text("utf-8", "replace")
                    break
        if html:
            papers.extend(parse_eccv_all(html))
    if "RSS" in venues:
        for year, vol in RSS_VOLS:
            ok, _, _ = in_window_meeting("RSS", year)
            if ok is False:
                continue
            dest = listing_file("rss", vol)
            if not dest.exists():
                fetch_rss(year, vol)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_rss(year, vol, html))
    if "MLSys" in venues:
        for y in MLSYS_YEARS:
            ok, _, _ = in_window_meeting("MLSys", y)
            if ok is False:
                continue
            dest = listing_file("mlsys", str(y))
            if not dest.exists():
                fetch_mlsys(y)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_mlsys(y, html))
    if any(v in venues for v in ("OSDI", "NSDI", "SOSP")):
        for venue, year, slug in USENIX_SESSIONS:
            if venue not in venues:
                continue
            ok, _, _ = in_window_meeting(venue, year)
            if ok is False:
                continue
            dest = listing_file("usenix", f"{venue}{year}")
            if not dest.exists():
                fetch_usenix(venue, year, slug)
            html = dest.read_text("utf-8", "replace") if dest.exists() else ""
            if html:
                papers.extend(parse_usenix(venue, year, slug, html))
    return papers


def cmd_scan(cat):
    core, extra = CATS[cat][2], CATS[cat][3]
    venues = core + extra
    papers = all_listing_papers(venues)
    print(f"{cat}: {len(papers)} listing papers from {venues}")
    cands = load(cand_path(cat), {})
    kept = 0
    for p in papers:
        if p.get("window_ok") is False:
            continue
        sc, thresh, hits, pens = score_text(cat, p["title"], p.get("abstract", ""))
        if sc < 3:
            continue
        key = f"{p['venue']}:{p['year']}:" + norm_title(p["title"])
        rec = dict(p)
        rec.update({"score": sc, "thresh": thresh, "hits": hits, "pens": pens,
                    "relation": relation_label(hits), "key": key})
        prev = cands.get(key, {})
        if prev.get("abstract") and not rec.get("abstract"):
            rec["abstract"] = prev["abstract"]
        cands[key] = rec
        kept += 1
    save(cand_path(cat), cands)
    print(f"  title-prefilter kept {kept}, pool {len(cands)}")
    append_log(LOG, f"- {cat} 列表扫描：来源论文 {len(papers)}，标题预筛 {kept}，候选池 {len(cands)}")


ARXIV_QUERIES = {
    "01": [
        'all:"gaussian process"',
        'all:"gaussian processes"',
        'ti:"neural process"',
        'ti:"conformal prediction"',
        'all:"bayesian neural"',
        'all:"uncertainty quantification"',
        'all:"laplace approximation"',
        'all:"pac-bayes" OR all:"pac-bayesian"',
        'all:"variational gaussian process"',
        'all:"deep kernel learning"',
        'ti:"tabpfn" OR all:"prior-data fitted"',
        'all:"evidential deep"',
        'all:"inducing points" AND all:gaussian',
        '(all:"gaussian process" OR all:"conformal prediction" OR all:"bayesian neural" OR all:"uncertainty quantification" OR all:"neural process" OR all:"pac-bayes" OR all:"laplace") AND (co:ICLR OR jr:ICLR)',
        '(ti:"gaussian process" OR ti:"conformal" OR ti:"bayesian neural") AND (co:"NeurIPS" OR co:ICML OR jr:ICML OR jr:NeurIPS)',
    ],
    "02": [
        'all:"time series" AND (all:forecast OR all:probabilistic)',
        'all:"spatio-temporal" OR all:spatiotemporal',
        'all:"air quality"',
        'all:"water quality" OR all:hydrology',
        'all:"distribution shift" AND (all:forecast OR all:"time series")',
        'ti:"time series" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD OR co:AAAI OR co:IJCAI)',
        'all:"probabilistic forecast" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD)',
        'all:"energy forecasting" OR all:"load forecasting" OR all:"wind power" OR all:"solar power"',
    ],
    "03": [
        'all:"soft sensor"',
        'all:"fault detection" AND all:industrial',
        'all:"anomaly detection" AND all:industrial',
        'all:"tennessee eastman"',
        'all:"root cause" AND (all:process OR all:industrial)',
        '(all:"soft sensor" OR all:"process monitoring" OR all:"fault diagnosis") AND (co:ICML OR co:NeurIPS OR co:ICLR OR co:AAAI OR co:IJCAI OR co:KDD)',
        'all:"predictive maintenance" OR all:"remaining useful life"',
        'all:"multivariate time series" AND all:"anomaly detection"',
    ],
    "04": [
        'all:"large language model" AND (all:alignment OR all:retrieval)',
        'all:"vision-language" OR all:multimodal',
        'all:RAG AND all:"language model"',
        '(all:"instruction tuning" OR all:RLHF OR all:DPO) AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:ACL OR co:EMNLP)',
        'all:"tool use" AND all:"language model"',
        'ti:"multilingual" AND all:"language model" AND (co:ACL OR co:EMNLP OR co:ICLR)',
        'ti:"large language model" AND (co:ACL OR co:EMNLP OR co:ICLR OR co:ICML OR co:NeurIPS)',
        'all:"vision-language model" AND (co:CVPR OR co:ICCV OR co:ECCV OR co:ICLR)',
        'all:"retrieval-augmented generation"',
        'all:"direct preference optimization" OR all:RLHF',
        'all:"mixture of experts" AND all:"language model"',
    ],
    "05": [
        'all:"code generation" OR all:"program repair"',
        'all:"software engineering" AND all:"language model"',
        'all:swe-bench OR all:humaneval',
        'all:"autonomous software agent" OR all:"coding agent"',
        '(all:"unit test generation" OR all:"bug localization") AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL)',
        'all:"repository-level" AND all:code',
        'ti:"code generation" AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL OR co:ICLR OR co:ICML OR co:NeurIPS)',
        'all:"program repair" AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL)',
        'all:"language model" AND all:"software engineering" AND (co:ICSE OR co:FSE OR co:ASE OR co:ICLR)',
        'all:"issue resolution" OR all:"swe-agent" OR all:"coding agent"',
        'all:"test generation" AND (all:llm OR all:"language model")',
        'all:"vulnerability detection" AND (all:code OR all:software) AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA)',
    ],
    "06": [
        'all:"inference serving" OR all:vllm OR all:pagedattention',
        'all:"distributed training"',
        'all:"machine learning system"',
        '(all:"inference engine" OR all:"GPU scheduling") AND (co:SOSP OR co:OSDI OR co:NSDI OR co:ASPLOS OR co:MLSys)',
        'all:mlsys OR all:"MLSys"',
        'all:"pipeline parallelism" OR all:FSDP OR all:"zero redundancy"',
        'all:"kv cache" OR all:pagedattention OR all:vllm',
        '(all:"distributed training" OR all:"inference serving") AND (co:OSDI OR co:SOSP OR co:NSDI OR co:ASPLOS OR co:MLSys)',
        'all:"gpu kernel" OR all:"cluster scheduling" AND (all:training OR all:inference)',
        'ti:"serving" AND (all:llm OR all:"language model") AND (co:OSDI OR co:SOSP OR co:MLSys OR co:NSDI)',
        'co:ASPLOS AND (all:gpu OR all:training OR all:serving OR all:inference)',
        'co:ISCA AND (all:gpu OR all:accelerator OR all:training OR all:inference)',
        '(co:SOSP OR co:"SC 20") AND (all:training OR all:serving OR all:gpu)',
        'co:OSDI AND (all:LLM OR all:"language model" OR all:training)',
    ],
    "07": [
        'all:quadrotor OR all:uav OR all:quadcopter',
        'all:"learning-based control" OR all:"model predictive control"',
        'all:robot AND all:"reinforcement learning"',
        '(all:quadrotor OR all:uav) AND (co:ICRA OR co:IROS OR co:RSS OR co:CoRL)',
        'all:"sim-to-real" AND all:robot',
        'all:"control barrier" OR all:"safe control"',
        'all:"gaussian process" AND all:control AND (co:L4DC OR co:CDC OR co:ACC OR co:CoRL)',
        'ti:quadrotor OR ti:uav OR ti:quadcopter',
        '(all:manipulation OR all:humanoid OR all:legged) AND (co:CoRL OR co:RSS OR co:ICRA)',
        'co:ICRA AND (all:uav OR all:quadrotor OR all:"learning-based control" OR all:mpc)',
        'co:IROS AND (all:uav OR all:quadrotor OR all:control)',
        'co:L4DC AND (all:control OR all:mpc OR all:robot)',
    ],
}


def cmd_arxiv(cat):
    qs = ARXIV_QUERIES.get(cat, [])
    cands = load(cand_path(cat), {})
    n_new = 0
    win = f"submittedDate:[{WINDOW_START.replace('-', '')}0000 TO {WINDOW_END.replace('-', '')}2359]"
    for q in qs:
        qq = f"({q}) AND {win}"
        hits, total = arxiv_search(qq, maxn=120)
        print(f"  arXiv {len(hits)}/{total}  {q}")
        append_log(LOG, f"- arXiv `{q}` 命中 {total}，取回 {len(hits)}")
        allowed = CATS[cat][2] + CATS[cat][3]
        for h in hits:
            blob = f"{h.get('comment','')} {h.get('journal_ref','')}"
            if re.search(r"workshop|tiny paper|findings|under review|submitted to", blob, re.I) and not PUBLISHED.search(blob):
                continue
            venue, year = venue_year_from_text(blob, allowed)
            track = "main"
            rank = "supplement_venue" if venue in {"AISTATS", "UAI", "MLSys", "L4DC", "CDC", "ACC"} else "core"
            if not venue or not year:
                continue
            if not PUBLISHED.search(blob) and venue != "ICLR":
                # ICLR comments often only say "ICLR 2024"; other venues need a year tag.
                if not re.search(
                    r"\b(ICLR|ICML|NeurIPS|NIPS|AAAI|IJCAI|KDD|ACL|EMNLP|CVPR|ICCV|ECCV|"
                    r"ICSE|FSE|ASE|ISSTA|SOSP|OSDI|NSDI|ASPLOS|ISCA|SC|MLSys|"
                    r"RSS|CoRL|ICRA|IROS|L4DC|CDC|ACC|ESEC/FSE)\s*20",
                    blob, re.I):
                    continue
            ok, note, prec = in_window_meeting(venue, year)
            if ok is False:
                continue
            sc, thresh, hits_l, pens = score_text(cat, h["title"], h.get("abstract", ""))
            if sc < 4:
                continue
            key = f"{venue}:{year}:" + norm_title(h["title"])
            ghs = github_urls(h.get("comment", ""), h.get("abstract", ""))
            rec = {
                "source": "arxiv_comment",
                "venue": venue, "year": year, "track": track, "venue_rank_note": rank,
                "title": h["title"], "authors": h["authors"],
                "abs_url": h["abs_url"], "pdf_url": h["pdf_url"],
                "arxiv": h["arxiv"], "arxiv_v1": h["v1_date"],
                "arxiv_version": h["latest_version"], "comment": h.get("comment", ""),
                "journal_ref": h.get("journal_ref", ""), "abstract": h.get("abstract", ""),
                "doi": h.get("doi", ""),
                "github_hint": ghs,
                "window_ok": ok, "window_note": note, "date_precision": prec,
                "pub_date": meeting_date(venue, year)[0],
                "score": sc, "thresh": thresh, "hits": hits_l, "pens": pens,
                "relation": relation_label(hits_l), "key": key,
            }
            prev = cands.get(key, {})
            if prev:
                rec["pdf_url"] = prev.get("pdf_url") or rec["pdf_url"]
                rec["abs_url"] = prev.get("abs_url") or rec["abs_url"]
                rec["source"] = prev.get("source", rec["source"]) + "+arxiv"
                rec["pmlr_id"] = prev.get("pmlr_id", "")
                rec["nips_hash"] = prev.get("nips_hash", "")
            if key not in cands:
                n_new += 1
            cands[key] = rec
            save(META / f"arxiv_{h['arxiv'].replace('/', '_')}.json", h)
    save(cand_path(cat), cands)
    print(f"  arXiv new/updated, pool {len(cands)}, new keys ~{n_new}")


def fetch_abstract(p):
    url = p.get("abs_url") or ""
    if not url:
        return p
    st, body, _, _ = http(url, timeout=60, max_bytes=2_000_000)
    if st != 200 or not body:
        return p
    html = body.decode("utf-8", "replace")
    abs_txt = ""
    for pat in [
        r'<div class="abstract">\s*(.*?)\s*</div>',
        r'<p class="abstract">\s*(.*?)\s*</p>',
        r'<div class="abstract-card"[^>]*>.*?<p>\s*(.*?)\s*</p>',
        r'Abstract</h4>\s*<p>\s*(.*?)\s*</p>',
        r'id="abstract"[^>]*>\s*(.*?)\s*</div>',
    ]:
        m = re.search(pat, html, re.S | re.I)
        if m:
            abs_txt = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", m.group(1))))
            if len(abs_txt) > 80:
                break
    if abs_txt:
        p["abstract"] = abs_txt
    ghs = github_urls(html, abs_txt, p.get("comment", ""))
    if ghs:
        p["github_hint"] = list(dict.fromkeys(list(p.get("github_hint") or []) + ghs))
    # NeurIPS abstract pages often have arXiv link
    m = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})", html, re.I)
    if m and not p.get("arxiv"):
        p["arxiv"] = m.group(1)
    return p


def cmd_enrich(cat, limit=400):
    cands = load(cand_path(cat), {})
    # enrich highest-score items missing abstracts
    rows = sorted(cands.values(), key=lambda x: -x.get("score", 0))
    n = 0
    for p in rows:
        if n >= limit:
            break
        if p.get("abstract") and p.get("github_hint"):
            continue
        if p.get("source", "").startswith("arxiv"):
            continue
        if p.get("score", 0) < 4:
            continue
        if cat == "04":
            blob = (p.get("title", "") + " " + p.get("abstract", ""))
            if not re.search(r"language model|\bllms?\b|multimodal|vision-language|\brag\b|vlm", blob, re.I):
                continue
        fetch_abstract(p)
        sc, thresh, hits, pens = score_text(cat, p["title"], p.get("abstract", ""))
        p["score"], p["thresh"], p["hits"], p["pens"] = sc, thresh, hits, pens
        p["relation"] = relation_label(hits)
        cands[p["key"]] = p
        n += 1
        if n % 20 == 0:
            save(cand_path(cat), cands)
            print(f"  enriched {n}")
    save(cand_path(cat), cands)
    print(f"enriched {n}, pool {len(cands)}")


def cmd_select(cat, target=110):
    cands = load(cand_path(cat), {})
    rows = []
    seen_title = set()
    for other in CATS:
        if other == cat:
            continue
        for s in load(seed_path(other), []) or []:
            if s.get("title"):
                seen_title.add(norm_title(s["title"]))
    venue_norm = {
        "NIPS": "NeurIPS", "NEURIPS": "NeurIPS", "ICML": "ICML", "ICLR": "ICLR",
        "COLT": "COLT", "AISTATS": "AISTATS", "UAI": "UAI", "KDD": "KDD",
        "AAAI": "AAAI", "IJCAI": "IJCAI", "ACL": "ACL", "EMNLP": "EMNLP",
        "CVPR": "CVPR", "ICCV": "ICCV", "ECCV": "ECCV", "ICSE": "ICSE",
        "FSE": "FSE", "ASE": "ASE", "ISSTA": "ISSTA", "SOSP": "SOSP",
        "OSDI": "OSDI", "NSDI": "NSDI", "ASPLOS": "ASPLOS", "ISCA": "ISCA",
        "SC": "SC", "MLSYS": "MLSys", "RSS": "RSS", "CORL": "CoRL",
        "ICRA": "ICRA", "IROS": "IROS", "L4DC": "L4DC", "CDC": "CDC", "ACC": "ACC",
    }
    for p in cands.values():
        p["venue"] = venue_norm.get(str(p.get("venue", "")).upper(), p.get("venue", ""))
        allowed_v = set(CATS[cat][2] + CATS[cat][3])
        if p.get("venue") not in allowed_v:
            continue
        ok, note, prec = in_window_meeting(p.get("venue", ""), p.get("year") or 0)
        if ok is False or ok is None:
            continue
        p["window_ok"], p["window_note"], p["date_precision"] = ok, note, prec
        p["pub_date"] = meeting_date(p.get("venue", ""), p.get("year") or 0)[0]
        if not meeting_date(p.get("venue", ""), p.get("year") or 0)[0]:
            continue
        if p.get("score", 0) < p.get("thresh", 5) and p.get("score", 0) < 5:
            continue
        nt = norm_title(p["title"])
        if nt in seen_title:
            continue
        blob = (p.get("title", "") + " " + p.get("abstract", "")).lower()
        if "gaussian splatting" in blob or "3d gaussian" in blob:
            if "gaussian process" not in blob:
                continue
        if str(p.get("title", "")).lower().startswith("position:"):
            continue
        if cat == "04":
            blob = (p.get("title", "") + " " + p.get("abstract", ""))
            if not re.search(
                r"large language model|\bllms?\b|vision-language|\bvlm\b|multimodal|"
                r"retrieval-augmented|\brag\b|instruction tun|rlhf|\bdpo\b|"
                r"language model",
                blob, re.I):
                continue
            if re.search(r"findings of the association|findings of emnlp|acl findings", blob, re.I):
                continue
            if re.search(r"endpoint detection and response|\bedr\b", blob, re.I):
                continue
        if cat == "07":
            blob = (p.get("title", "") + " " + p.get("abstract", ""))
            if not re.search(
                r"quadrotor|quadcopter|\buav\b|drone|unmanned aerial|robot|"
                r"manipulat|humanoid|legged|model predictive control|\bmpc\b|"
                r"learning[- ]based control|control barrier|sim-to-real|sim2real|"
                r"imitation learning|visuomotor",
                blob, re.I):
                continue
        if cat == "06":
            blob = (p.get("title", "") + " " + p.get("abstract", ""))
            if not re.search(
                r"inference|serving|distributed training|vllm|pagedattention|kv cache|"
                r"pipeline parallel|tensor parallel|fsdp|gpu (cluster|schedul|kernel)|"
                r"parameter server|allreduce|mlsys|machine learning system|"
                r"training (system|framework)|quantization.{0,20}(infer|serv)",
                blob, re.I):
                continue
        if cat == "05":
            blob = (p.get("title", "") + " " + p.get("abstract", ""))
            if not re.search(
                r"code generation|program (repair|synthesis)|software (agent|engineering|testing)|"
                r"coding agent|swe-bench|humaneval|unit test|bug (fix|localization|detection)|"
                r"repository-level|issue resol|test generation|vulnerability detection|"
                r"code (llm|search|retrieval|completion)|program analysis|static analysis",
                blob, re.I):
                continue
            if re.search(r"findings of the association|findings of emnlp", blob, re.I):
                continue
        if str(p.get("venue")) in {"NeurIPS", "NIPS"} and int(p.get("year") or 0) >= 2026:
            continue
        seen_title.add(nt)
        rows.append(p)
    def rank(p):
        gh = 1 if p.get("github_hint") else 0
        official = 1 if p.get("source") in {"pmlr", "neurips"} or "pmlr" in (p.get("source") or "") or "neurips" in (p.get("source") or "") else 0
        return (-p.get("score", 0), -official, -gh, -int(p.get("year") or 0), p.get("title", ""))
    rows.sort(key=rank)
    cap = SELECT_CAP.get(cat, {"ICML": 20, "NeurIPS": 20, "ICLR": 16})
    year_cap = {"04": 28, "05": 28, "06": 28, "07": 28}.get(cat)
    counts = {}
    ycounts = {}
    chosen = []
    leftover = []
    for p in rows:
        v = p.get("venue") or ""
        y = p.get("year") or 0
        if counts.get(v, 0) >= cap.get(v, 12):
            leftover.append(p)
            continue
        if year_cap and ycounts.get(y, 0) >= year_cap:
            leftover.append(p)
            continue
        counts[v] = counts.get(v, 0) + 1
        ycounts[y] = ycounts.get(y, 0) + 1
        chosen.append(p)
        if len(chosen) >= target:
            break
    for p in leftover:
        if len(chosen) >= target:
            break
        y = p.get("year") or 0
        if year_cap and ycounts.get(y, 0) >= year_cap:
            continue
        chosen.append(p)
        counts[p.get("venue") or "?"] = counts.get(p.get("venue") or "?", 0) + 1
        ycounts[y] = ycounts.get(y, 0) + 1
    # Prefer github-bearing papers inside the already chosen venue mix (swap within venue).
    by_venue = {}
    for p in rows:
        by_venue.setdefault(p.get("venue"), []).append(p)
    for i, q in enumerate(chosen):
        v = q.get("venue")
        if q.get("github_hint"):
            continue
        alt = next((p for p in by_venue.get(v, []) if p.get("github_hint") and p not in chosen), None)
        if alt and alt.get("score", 0) >= q.get("score", 0) - 4:
            chosen[i] = alt
    for i, p in enumerate(chosen, 1):
        p["sid"] = f"D{cat}-{i:03d}"
        p["selected"] = True
    save(seed_path(cat), chosen)
    save(cand_path(cat), cands)
    gh_n = sum(1 for p in chosen if p.get("github_hint"))
    print(f"{cat}: selected {len(chosen)} (github_hint {gh_n}) venue {counts}")
    append_log(LOG, f"- {cat} 选定 {len(chosen)} 篇写入 {seed_path(cat).name}；标题/摘要含 GitHub 提示 {gh_n} 篇。按场次：{counts}")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "listings":
        cmd_listings()
    elif cmd == "scan":
        cmd_scan(argv[2])
    elif cmd == "arxiv":
        cmd_arxiv(argv[2])
    elif cmd == "enrich":
        lim = int(argv[3]) if len(argv) > 3 else 400
        cmd_enrich(argv[2], lim)
    elif cmd == "select":
        tgt = int(argv[3]) if len(argv) > 3 else 110
        cmd_select(argv[2], tgt)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
