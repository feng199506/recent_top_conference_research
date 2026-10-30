"""Orchestrate one domain at a time.

  python3 -I scripts/run_en.py listings
  python3 -I scripts/run_en.py domain 01
  python3 -I scripts/run_en.py catalog
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog_en  # noqa: E402
import code_en  # noqa: E402
import discover_en  # noqa: E402
import download_en  # noqa: E402
from common_en import CATS, ROOT, SEARCH_DATE, WINDOW_END, WINDOW_START, append_log  # noqa: E402

LOG = ROOT / "search_log_cn.md"


def ensure_log():
    if LOG.exists():
        return
    LOG.write_text(
        f"""# 检索日志

检索日：{SEARCH_DATE}（UTC+9 当日）。滚动五年窗口：正式会议论文发表日期 {WINDOW_START} 至 {WINDOW_END}。

## 规则（本轮）

- 只收集整理：不运行代码、不训练、不部署、不上传 GitHub。
- 主集合只收已正式录用且全文已公开的主会研究论文。Workshop / Findings / Demo / 短论文 / 竞赛报告 / 纯预印本不计入主集合。
- 日期按会议正式发表日；同时记录 arXiv v1。只能核实到年份时标注精度，边界条目待核实后再计数。
- 不自行编造 CCF 等级。AISTATS、UAI、MLSys、L4DC/CDC/ACC 等作为补充专业会议单独标注。
- 代码：实际 clone 快照并静态核对。L0=已下载；L1=入口/配置/依赖已静态核对。不产生“已复现”结论。
- 不绕过访问限制。不下载大型数据集、模型权重、依赖缓存或构建产物。不额外做整库 SHA256 扫描。

## 已有文献库（核验后复制，不移动原件）

| 资料库 | 路径 | 对本任务 |
|---|---|---|
| 高斯过程 | `/root/gaussian_process_literature` | 方向 1 可能复用 PDF |
| 工业过程监控 | `/root/industrial_process_monitoring_literature` | 方向 3 可能复用；多数为期刊，需核实是否主会 |
| 人工智能课程 | `/root/ai_undergraduate_graduate_curriculum_literature` | 可能复用少量 PDF |
| 概率统计课程 | `/root/probability_statistics_curriculum_literature` | 可能复用少量 PDF |
| 时间序列 / 机器学习深度学习 / 大模型多模态 | 本机源目录不在 `/root` | 未复用 |

## 可用渠道实测

| 渠道 | 结果 |
|---|---|
| DBLP API | Cloudflare 机器人验证，未使用 |
| Semantic Scholar / OpenAlex | 429，未使用，未代申请 API key |
| Papers with Code API | 返回 HTML 登录页，未使用 |
| OpenReview API | 返回 HTML，未当作 JSON API 使用 |
| PMLR 主会 HTML | 可用，作 ICML/AISTATS/COLT/UAI/CoRL/L4DC 主列表 |
| NeurIPS papers.nips.cc | 可用，主会与 Datasets and Benchmarks 分轨道 |
| arXiv API | 可用；用 comment/journal_ref 确认 ICLR 等录用，排除 workshop/tiny/under review |
| Crossref | 可用作日期核对 |
| GitHub git clone | 用于代码快照（depth 1，跳过 LFS 与子模块） |

""",
        encoding="utf-8",
    )


def run_domain(cat):
    ensure_log()
    append_log(LOG, f"\n## 方向 {cat} {CATS[cat][1]}\n")
    print("=== listings ===")
    discover_en.cmd_listings()
    print("=== scan ===")
    discover_en.cmd_scan(cat)
    print("=== arxiv ===")
    discover_en.cmd_arxiv(cat)
    print("=== enrich ===")
    discover_en.cmd_enrich(cat, 250)
    print("=== select ===")
    discover_en.cmd_select(cat, 110)
    print("=== download papers ===")
    download_en.cmd_papers(cat)
    print("=== fetch code ===")
    code_en.cmd_fetch(cat)
    print("=== catalog ===")
    catalog_en.rebuild_all()
    print(f"domain {cat} pass done")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "listings":
        ensure_log()
        discover_en.cmd_listings()
    elif cmd == "domain":
        run_domain(argv[2])
    elif cmd == "catalog":
        catalog_en.rebuild_all()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
