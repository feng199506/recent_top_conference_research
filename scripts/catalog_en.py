"""Build Chinese catalogs and per-domain progress after a domain is downloaded.

  python3 -I scripts/catalog_en.py domain 01
  python3 -I scripts/catalog_en.py all
"""
import csv
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import (CATS, ROOT, SEEDS, STATE, SEARCH_DATE, WINDOW_END, WINDOW_START,  # noqa: E402
                       cat_dir, cat_label, load)
from venues_en import meeting_date  # noqa: E402

CATALOG_FIELDS = [
    "文献编号", "主方向", "交叉方向", "关系类型", "相关说明", "子主题命中",
    "会议", "会议年份", "轨道", "渠道说明", "是否补充专业会议",
    "正式发表日期", "日期精度", "正式发表依据", "窗口判定", "窗口说明",
    "首次预印本日期", "预印本依据", "下载版本",
    "标题", "作者", "DOI", "arXiv ID", "原始页面", "全文URL",
    "本地PDF", "来源性质", "跨库重复", "SHA256", "页数核验",
    "代码等级", "代码类别", "代码URL", "代码提交", "许可证", "官方归属证据",
    "训练或方法入口", "配置", "依赖", "评测/测试", "子模块", "LFS",
    "代码静态核验级别", "代码缺失项", "选入理由",
]


def seed_path(cat):
    return SEEDS / f"{cat}_{CATS[cat][0]}_seed_cn.json"


def paper_state(cat):
    return STATE / f"papers_{cat}_en.json"


def code_state(cat):
    return STATE / f"code_{cat}_en.json"


def all_verified(cat):
    seeds = {p["sid"]: p for p in load(seed_path(cat), []) if p.get("sid")}
    pst = load(paper_state(cat), {})
    cst = load(code_state(cat), {})
    rows = []
    for sid, p in seeds.items():
        st = pst.get(sid, {})
        if st.get("status") not in {"ok", "pending"}:
            continue
        cd = cst.get(sid, {})
        start, end, note, prec = meeting_date(p.get("venue", ""), p.get("year") or 0)
        rows.append({
            "文献编号": sid,
            "主方向": cat_label(cat),
            "交叉方向": ";".join(p.get("cross") or []),
            "关系类型": p.get("relation", ""),
            "相关说明": "；".join(p.get("hits") or []),
            "子主题命中": ";".join(p.get("hits") or []),
            "会议": p.get("venue", ""),
            "会议年份": p.get("year", ""),
            "轨道": p.get("track", ""),
            "渠道说明": p.get("source", ""),
            "是否补充专业会议": "是" if p.get("venue_rank_note") == "supplement_venue" else "否",
            "正式发表日期": p.get("pub_date") or start,
            "日期精度": p.get("date_precision") or prec,
            "正式发表依据": note,
            "窗口判定": str(p.get("window_ok", "")),
            "窗口说明": p.get("window_note", ""),
            "首次预印本日期": p.get("arxiv_v1", ""),
            "预印本依据": "arXiv v1 提交日" if p.get("arxiv_v1") else "",
            "下载版本": (f"arXiv {p['arxiv']}v{p.get('arxiv_version','')}" if p.get("arxiv")
                       else p.get("downloaded_from") or p.get("pdf_url", "")),
            "标题": p.get("title", ""),
            "作者": "; ".join(p.get("authors") or []),
            "DOI": p.get("doi", ""),
            "arXiv ID": p.get("arxiv", ""),
            "原始页面": p.get("abs_url", ""),
            "全文URL": p.get("pdf_url", ""),
            "本地PDF": st.get("path", ""),
            "来源性质": st.get("source_kind", "新下载"),
            "跨库重复": st.get("reused_lib", ""),
            "SHA256": st.get("sha256", ""),
            "页数核验": st.get("detail", ""),
            "代码等级": cd.get("level", ""),
            "代码类别": cd.get("code_kind", "D"),
            "代码URL": cd.get("url", ""),
            "代码提交": cd.get("commit", ""),
            "许可证": cd.get("license_name", "未发现许可证（不标为可自由复用）" if not cd.get("url") else cd.get("license_name", "")),
            "官方归属证据": cd.get("official_evidence", ""),
            "训练或方法入口": "; ".join(cd.get("entries") or []),
            "配置": "; ".join(cd.get("configs") or []),
            "依赖": "; ".join(cd.get("deps") or []),
            "评测/测试": "; ".join((cd.get("tests") or [])[:6]),
            "子模块": "有 .gitmodules（本轮未拉）" if cd.get("has_gitmodules") else "未见",
            "LFS": "有 LFS 指针（未拉取对象）" if cd.get("has_lfs_pointers") else "未见",
            "代码静态核验级别": cd.get("level", ""),
            "代码缺失项": "; ".join(cd.get("missing") or cd.get("note", "").split("；") if isinstance(cd.get("missing"), list) else [cd.get("note", "")]),
            "选入理由": f"{p.get('relation','')}。命中：{'、'.join(p.get('hits') or [])}。会议 {p.get('venue')} {p.get('year')} {p.get('track')} 轨道。",
        })
    return rows


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


USE_TEXT = {
    "01": "对照现有高斯过程文献库，补充近五年主会中的 GP、共形预测、贝叶斯神经网络与校准方法，以及可静态核验的官方实现入口。",
    "02": "用于空气质量/水文/能源等环境时序与时空预测的方法对照，以及可迁移的概率预测与分布漂移处理。",
    "03": "工业过程监控主会论文稀缺。本方向保留化学过程/智能制造/软测量相关主会工作，并以多变量时序异常检测与因果根因作为可迁移方法，不把视觉巡检或 IT 运维论文充数。",
    "04": "用于大语言模型对齐、检索增强、工具使用与视觉语言模型的方法对照和官方实现入口。",
    "05": "用于代码生成、程序修复、测试生成与软件智能体的方法对照。",
    "06": "用于训练/推理系统设计、并行策略与生产服务的方法对照。",
    "07": "用于无人机、操作机器人与学习控制（含 MPC/安全控制）的方法对照。",
}
GAP_TEXT = {
    "07": [
        "- ICRA/IROS/CDC/ACC 全文多在 IEEE 付费墙；本轮 arXiv API 在方向 7 检索时超时，未把无公开全文的论文计入。",
        "- 主集合来自 RSS 开放proceedings、CoRL 与 L4DC 的 PMLR 主卷。RSS 2025 部分 PDF 为扫描件、无法提取文本，已替换。",
        "- 未运行训练或评测；缺数据、权重和硬件验证。",
    ],
    "06": [
        "- SOSP 不在 USENIX 开放列表（ACM）；ISCA/SC/ASPLOS 主会 PDF 多在付费墙，本轮仅收 arXiv comment 能确认录用且全文公开的条目。",
        "- 已核验约 60 篇（MLSys/OSDI/NSDI 为主），低于 90–120。未把与训练/推理服务无关的网络/体系结构论文凑数。",
        "- 未运行训练或评测；缺数据、权重和硬件验证。",
    ],
    "03": [
        "- 近五年 ICML/NeurIPS/ICLR/KDD/AAAI/IJCAI 主会中，直接面向化工过程监控、软测量、TE 过程的论文很少；该方向文献主要在 IEEE 过程控制/仪表期刊，本轮不把期刊算进主集合。",
        "- 已核验 39 篇（直接工业/制造相关 11 篇，可迁移的多变量时序异常检测与因果根因 28 篇），低于 90–120 目标。**未**用 3D/图/视频/通用视觉异常检测或微服务根因论文凑数。",
        "- 官方代码 A+B 约两成；部分 NeurIPS 2025 工业基准尚未放出完整仓库。",
        "- 未运行训练或评测；缺数据、权重和硬件验证。",
        "- FlowFuse 仓库 clone 需登录，按 D 登记。",
    ],
}
DOMAIN_STATUS = {
    "03": "已完成（主会缺口）",
    "06": "已完成（主会缺口）",
}


def domain_readme(cat, rows):
    pst = load(paper_state(cat), {})
    cst = load(code_state(cat), {})
    n = len(rows)
    venues = Counter((r["会议"], str(r["会议年份"])) for r in rows)
    tracks = Counter(r["轨道"] for r in rows)
    years = Counter(str(r["会议年份"]) for r in rows)
    kinds = Counter(r["代码类别"] for r in rows)
    reuse = sum(1 for r in rows if r["来源性质"] == "已有复用")
    gh_off = sum(1 for r in rows if r["代码类别"] == "A")
    coded = sum(1 for r in rows if r["代码类别"] in {"A", "B", "C"})
    pct = (coded / n * 100) if n else 0
    top = sorted(rows, key=lambda r: (0 if r["代码类别"] == "A" else 1, -len(r.get("子主题命中") or "")))[:10]
    lines = [
        f"# {cat_label(cat)}",
        "",
        f"检索日 {SEARCH_DATE}。窗口 {WINDOW_START} 至 {WINDOW_END}，按正式会议发表日期判断。",
        f"本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。",
        "",
        f"- 已下载并核验全文：**{n}** 篇（目标约 100，参考 90–120）",
        f"- 新下载 {n - reuse}，已有复用 {reuse}",
        f"- 有可获取代码（A/B/C）{coded} 篇（{pct:.1f}%）；官方完整实现（A）{gh_off} 篇",
        f"- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现",
        "",
        "## 年份",
        "",
        "| 年份 | 篇数 |",
        "|---|---|",
    ]
    for y, c in sorted(years.items()):
        lines.append(f"| {y} | {c} |")
    lines += ["", "## 会议与轨道", "", "| 会议 | 年份 | 轨道计数 |", "|---|---|---|"]
    for (v, y), c in sorted(venues.items()):
        lines.append(f"| {v} | {y} | {c} |")
    lines += ["", "轨道合计："]
    for t, c in tracks.items():
        lines.append(f"- {t or '（未标）'}: {c}")
    lines += ["", "## 代码可用性", "", "| 类别 | 含义 | 篇数 |", "|---|---|---|",
              f"| A | 作者官方完整实现（静态） | {kinds.get('A',0)} |",
              f"| B | 作者官方部分实现 | {kinds.get('B',0)} |",
              f"| C | 仅第三方复现 | {kinds.get('C',0)} |",
              f"| D | 无代码、空仓或未找到 | {kinds.get('D',0)} |",
              "",
              f"筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 "
              f"{((kinds.get('A',0)+kinds.get('B',0))/n*100 if n else 0):.1f}%"
              f"（不把第三方算进官方代码，也不把目标写成已达成）。",
              "",
              "## 优先阅读与复现（10 篇）",
              "",
              "只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。",
              ""]
    for i, r in enumerate(top, 1):
        lines.append(f"### {i}. {r['标题']}")
        lines.append("")
        lines.append(f"- 会议：{r['会议']} {r['会议年份']}（{r['轨道']}）")
        lines.append(f"- 关系：{r['关系类型']}；{r['相关说明']}")
        lines.append(f"- 代码：类别 {r['代码类别']}，级别 {r['代码静态核验级别'] or '无'}；许可证 {r['许可证'] or '无'}")
        lines.append(f"- 理由：{r['选入理由']}")
        if r.get("代码类别") in {"A", "B", "C"} and r.get("代码URL"):
            miss = r.get("代码缺失项") or "静态已见入口/配置/依赖，未运行"
        else:
            miss = r.get("代码缺失项") or "本轮未找到可获取代码链接"
        lines.append(f"- 前置条件：{miss}。大型数据、权重未下载；本轮未运行。")
        lines.append("")
    lines += [
        "## 对本任务的用途",
        "",
        USE_TEXT.get(cat, (
            "本方向文献用于对照现有高斯过程文献库与工业/时序工作中的不确定性、核方法、变分推断和校准做法，"
            "提供可迁移的推断算法、评测协议和（若有）官方实现入口。"
        )),
        "",
        "## 缺口",
        "",
    ]
    lines += GAP_TEXT.get(cat, [
        "- 未运行训练或评测；缺数据、权重和硬件验证。",
        "- 付费墙会议论文若无合法公开全文则未计入。",
        "- 边界日期条目若精度只有年份，未计入或在窗口说明中标注。",
    ])
    lines += [
        "",
        f"续跑：`python3 -I scripts/run_en.py domain {cat}`（已完成项会跳过）。",
        "",
        f"生成时间 {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
    ]
    return "\n".join(lines)


def rebuild_all():
    all_rows = []
    progress = []
    code_rows = []
    for cat in CATS:
        sp = seed_path(cat)
        if not sp.exists():
            progress.append({
                "方向": cat_label(cat), "状态": "未开始", "已核验全文": 0,
                "目标": 100, "新下载": 0, "已有复用": 0, "A": 0, "B": 0, "C": 0, "D": 0,
                "官方代码率A+B": "", "备注": "",
            })
            continue
        rows = all_verified(cat)
        all_rows.extend(rows)
        (ROOT / "domains" / cat_dir(cat) / "README_cn.md").write_text(domain_readme(cat, rows), encoding="utf-8")
        kinds = Counter(r["代码类别"] for r in rows)
        reuse = sum(1 for r in rows if r["来源性质"] == "已有复用")
        n = len(rows)
        ab = kinds.get("A", 0) + kinds.get("B", 0)
        if cat in DOMAIN_STATUS:
            status = DOMAIN_STATUS[cat]
        elif n >= 90:
            status = "已完成"
        elif n:
            status = "进行中"
        else:
            status = "未开始"
        extra = ""
        if cat == "03":
            extra = "；主会直接工业论文稀缺，未凑数"
        if cat == "06":
            extra = "；ISCA/SC/ASPLOS 公开全文少，未用不相关系统论文凑数"
        progress.append({
            "方向": cat_label(cat),
            "状态": status,
            "已核验全文": n, "目标": 100, "新下载": n - reuse, "已有复用": reuse,
            "A": kinds.get("A", 0), "B": kinds.get("B", 0), "C": kinds.get("C", 0), "D": kinds.get("D", 0),
            "官方代码率A+B": f"{ab/n*100:.1f}%" if n else "",
            "备注": (f"有代码A/B/C {sum(kinds.get(k,0) for k in 'ABC')}/{n}" if n else "") + extra,
        })
        for r in rows:
            code_rows.append({
                "文献编号": r["文献编号"], "标题": r["标题"], "会议": r["会议"], "年份": r["会议年份"],
                "代码类别": r["代码类别"], "级别": r["代码静态核验级别"], "URL": r["代码URL"],
                "提交": r["代码提交"], "许可证": r["许可证"], "官方归属证据": r["官方归属证据"],
                "入口": r["训练或方法入口"], "配置": r["配置"], "依赖": r["依赖"],
                "子模块": r["子模块"], "LFS": r["LFS"], "缺失": r["代码缺失项"],
            })
    write_csv(ROOT / "catalog_cn.csv", CATALOG_FIELDS, all_rows)
    write_csv(ROOT / "progress_cn.csv",
              ["方向", "状态", "已核验全文", "目标", "新下载", "已有复用", "A", "B", "C", "D", "官方代码率A+B", "备注"],
              progress)
    write_csv(ROOT / "code_availability_cn.csv",
              ["文献编号", "标题", "会议", "年份", "代码类别", "级别", "URL", "提交", "许可证",
               "官方归属证据", "入口", "配置", "依赖", "子模块", "LFS", "缺失"],
              code_rows)
    print(f"catalog {len(all_rows)} rows")
    return all_rows, progress


def main(argv):
    rebuild_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
