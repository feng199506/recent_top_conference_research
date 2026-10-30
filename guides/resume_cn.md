# 续跑说明

工作目录：[`/root/recent_top_conference_research`](../)  
缓存：`/root/.cache/rtcr_lit`（listings、staging、pypdf、锁）

**七个方向均已完成**（03、06 为主会公开全文缺口，未凑数）。状态见 [`progress_cn.csv`](../progress_cn.csv)。

按方向顺序（已完成项会跳过已核验 PDF / 已有代码快照）：

```bash
python3 -I scripts/run_en.py domain 01
python3 -I scripts/run_en.py catalog
```

分步：

```bash
python3 -I scripts/discover_en.py listings
python3 -I scripts/discover_en.py scan 01
python3 -I scripts/discover_en.py arxiv 01
python3 -I scripts/discover_en.py enrich 01
python3 -I scripts/discover_en.py select 01
python3 -I scripts/download_en.py papers 01
python3 -I scripts/code_en.py fetch 01
python3 -I scripts/catalog_en.py
```

状态：`scripts/state/papers_NN_en.json`、`scripts/state/code_NN_en.json`。  
种子：`scripts/seeds/NN_*_seed_cn.json`。

已知限制：arXiv API 后期易长时间无响应（与 `/root/.cache/ipm_lit/locks/arxiv.org` 共享锁）；IEEE/ACM 付费墙不绕过。
