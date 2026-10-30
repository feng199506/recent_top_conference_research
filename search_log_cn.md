# 检索日志

检索日：2026-10-30（UTC+9 当日）。滚动五年窗口：正式会议论文发表日期 2021-10-30 至 2026-10-30。

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


## 列表抓取 2026-10-29
PMLR 主会卷与 NeurIPS [2021, 2022, 2023, 2024, 2025] 已缓存到 listings。
- 01 列表扫描：来源论文 36539，标题预筛 1125，候选池 1125
- arXiv `all:"gaussian process"` 命中 5452，取回 120
- arXiv `all:"gaussian processes"` 命中 5453，取回 120
- arXiv `ti:"neural process"` 命中 137，取回 120
- arXiv `ti:"conformal prediction"` 命中 682，取回 120
- arXiv `all:"bayesian neural"` 命中 714，取回 120
- arXiv `all:"uncertainty quantification"` 命中 4895，取回 120
- arXiv `all:"laplace approximation"` 命中 370，取回 120
- arXiv `all:"pac-bayes" OR all:"pac-bayesian"` 命中 332，取回 120
- arXiv `all:"variational gaussian process"` 命中 62，取回 62
- arXiv `all:"deep kernel learning"` 命中 74，取回 74
- arXiv `ti:"tabpfn" OR all:"prior-data fitted"` 命中 143，取回 120
- arXiv `all:"evidential deep"` 命中 142，取回 120
- arXiv `all:"inducing points" AND all:gaussian` 命中 83，取回 83
- 01 选定 110 篇写入 01_gp_probml_uncertainty_seed_cn.json；标题/摘要含 GitHub 提示 110 篇。按场次：{'ICML': 67, 'UAI': 11, 'AISTATS': 19, 'NeurIPS': 3, 'ICLR': 10}
- 01 选定 110 篇写入 01_gp_probml_uncertainty_seed_cn.json；标题/摘要含 GitHub 提示 67 篇。按场次：{'ICML': 30, 'ICLR': 22, 'UAI': 12, 'AISTATS': 16, 'NeurIPS': 26, 'COLT': 4}

## 方向 01 完成（2026-10-30）

- 全文核验通过 110 篇（ok 107，pending 3：作者姓氏变音符号）。新下载 110，已有复用 0。
- 排除：ICML 2026 Position 论文 1 篇；arXiv 标注 NeurIPS 2026（检索日后、全文未按正式会议收录）2 篇，已替换为 NeurIPS 2025/2024 与 ICML 2023 主会论文。
- 代码：克隆并静态核对 49 个仓库（A 22 / B 27 / D 61）。误把 PMLR `mlresearch/vXXX` 整卷仓库当论文代码的快照已删除并加入黑名单。
- 官方代码（A+B）44.5%，未达到每方向 70% 的筛选目标；COLT 理论文与部分无公开实现的 GP/UQ 论文保留，不用低质量有代码论文填数。
- 本轮最高核验级别 L1，不声称已复现。

## 列表抓取 2026-10-30
PMLR 主会卷、NeurIPS [2021, 2022, 2023, 2024, 2025]、IJCAI [2022, 2023, 2024, 2025, 2026] 已缓存到 listings。
- 02 列表扫描：来源论文 31718，标题预筛 888，候选池 888
- 02 列表扫描：来源论文 35517，标题预筛 1075，候选池 1075
- arXiv `all:"time series" AND (all:forecast OR all:probabilistic)` 命中 4688，取回 120
- arXiv `all:"spatio-temporal" OR all:spatiotemporal` 命中 12714，取回 120
- arXiv `all:"air quality"` 命中 597，取回 120
- arXiv `all:"water quality" OR all:hydrology` 命中 725，取回 120
- arXiv `all:"distribution shift" AND (all:forecast OR all:"time series")` 命中 341，取回 120
- arXiv `ti:"time series" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD OR co:AAAI OR co:IJCAI)` 命中 599，取回 120
- arXiv `all:"probabilistic forecast" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD)` 命中 32，取回 32
- arXiv `all:"energy forecasting" OR all:"load forecasting" OR all:"wind power" OR all:"solar power"` 命中 1028，取回 120
- arXiv `all:"time series" AND (all:forecast OR all:probabilistic)` 命中 4688，取回 120
- arXiv `all:"spatio-temporal" OR all:spatiotemporal` 命中 12714，取回 120
- arXiv `all:"air quality"` 命中 597，取回 120
- arXiv `all:"water quality" OR all:hydrology` 命中 725，取回 120
- arXiv `all:"distribution shift" AND (all:forecast OR all:"time series")` 命中 341，取回 120
- arXiv `ti:"time series" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD OR co:AAAI OR co:IJCAI)` 命中 599，取回 120
- arXiv `all:"probabilistic forecast" AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:KDD)` 命中 32，取回 32
- arXiv `all:"energy forecasting" OR all:"load forecasting" OR all:"wind power" OR all:"solar power"` 命中 1028，取回 120
- 02 选定 110 篇写入 02_timeseries_spatiotemporal_env_seed_cn.json；标题/摘要含 GitHub 提示 66 篇。按场次：{'KDD': 16, 'ICLR': 18, 'NeurIPS': 22, 'IJCAI': 16, 'ICML': 22, 'AAAI': 16}

## 方向 02 完成（2026-10-30）

- 列表扫描 35517 篇（含 IJCAI 主会 2022–2026），标题预筛后候选约 1075，arXiv 补 ICLR/KDD/AAAI 后池 1161。
- 选定并核验全文 110 篇：ICML 22、NeurIPS 22、ICLR 18、KDD 16、AAAI 16、IJCAI 16。新下载 110。
- 替换：视频显著性论文 1 篇、2 页 PyPOTS 短文 1 篇 → ICML 2022 时序共形预测、ICML 2024 BayOTIDE。
- 代码快照 71 个。按官方归属重分类后：A 14 / B 12 / C 45 / D 39。官方 A+B 23.6%，有代码 64.5%，未达 70% 官方代码目标。
- KDD/AAAI 主要来自 arXiv comment 录用标注 + arXiv PDF；IJCAI 来自 ijcai.org 主会 PDF。

- 03 列表扫描：来源论文 35517，标题预筛 174，候选池 174
- arXiv `all:"soft sensor"` 命中 71，取回 71
- arXiv `all:"fault detection" AND all:industrial` 命中 170，取回 120
- arXiv `all:"anomaly detection" AND all:industrial` 命中 1002，取回 120
- arXiv `all:"tennessee eastman"` 命中 67，取回 67
- arXiv `all:"root cause" AND (all:process OR all:industrial)` 命中 518，取回 120
- arXiv `(all:"soft sensor" OR all:"process monitoring" OR all:"fault diagnosis") AND (co:ICML OR co:NeurIPS OR co:ICLR OR co:AAAI OR co:IJCAI OR co:KDD)` 命中 6，取回 6
- arXiv `all:"predictive maintenance" OR all:"remaining useful life"` 命中 613，取回 120
- arXiv `all:"multivariate time series" AND all:"anomaly detection"` 命中 240，取回 120

## 方向 03 完成（2026-10-30）

- 近五年指定主会中直接工业过程监控/软测量/TE 论文稀缺（IEEE 期刊为主）。未用 3D/图/视频/微服务异常检测凑数。
- 严格筛选后核验全文 **39** 篇（目标 90–120，记为缺口）：直接工业/制造相关 11 篇，可迁移多变量时序异常检测与因果根因 28 篇。
- 会议：NeurIPS 13、IJCAI 8、ICML 8、AAAI 4、KDD 3、ICLR 2。新下载 39。
- 代码：A 6 / B 2 / C 6 / D 25。官方 A+B 20.5%，有代码 14/39=35.9%。`decisionintelligence/FlowFuse` clone 需登录，按 D。
- 本轮最高核验级别 L1，不声称已复现。续跑从方向 04 开始。


## 列表抓取 2026-10-30
PMLR 主会卷、NeurIPS [2021, 2022, 2023, 2024, 2025]、IJCAI [2022, 2023, 2024, 2025, 2026]、ACL/EMNLP 主卷、CVF、ECCV 已缓存到 listings。
- 04 列表扫描：来源论文 68768，标题预筛 14769，候选池 14769
- arXiv `all:"large language model" AND (all:alignment OR all:retrieval)` 命中 23996，取回 120
- arXiv `all:"vision-language" OR all:multimodal` 命中 44163，取回 120
- arXiv `all:RAG AND all:"language model"` 命中 4058，取回 120
- arXiv `(all:"instruction tuning" OR all:RLHF OR all:DPO) AND (co:ICLR OR co:ICML OR co:NeurIPS OR co:ACL OR co:EMNLP)` 命中 1015，取回 120
- arXiv `all:"tool use" AND all:"language model"` 命中 1332，取回 120
- arXiv `ti:"multilingual" AND all:"language model" AND (co:ACL OR co:EMNLP OR co:ICLR)` 命中 290，取回 120
- arXiv `ti:"large language model" AND (co:ACL OR co:EMNLP OR co:ICLR OR co:ICML OR co:NeurIPS)` 命中 2386，取回 120
- arXiv `all:"vision-language model" AND (co:CVPR OR co:ICCV OR co:ECCV OR co:ICLR)` 命中 1164，取回 120
- arXiv `all:"retrieval-augmented generation"` 命中 6218，取回 120
- arXiv `all:"direct preference optimization" OR all:RLHF` 命中 2528，取回 120
- arXiv `all:"mixture of experts" AND all:"language model"` 命中 1368，取回 120
- 04 选定 110 篇写入 04_llm_multimodal_seed_cn.json；标题/摘要含 GitHub 提示 93 篇。按场次：{'EMNLP': 16, 'ICCV': 10, 'ICML': 16, 'CVPR': 12, 'ICLR': 16, 'ECCV': 10, 'NeurIPS': 14, 'ACL': 16}
- 04 选定 110 篇写入 04_llm_multimodal_seed_cn.json；标题/摘要含 GitHub 提示 92 篇。按场次：{'EMNLP': 16, 'ICCV': 10, 'ICML': 16, 'CVPR': 12, 'ICLR': 16, 'ECCV': 10, 'NeurIPS': 14, 'ACL': 16}
- 04 选定 110 篇写入 04_llm_multimodal_seed_cn.json；标题/摘要含 GitHub 提示 93 篇。按场次：{'EMNLP': 16, 'ICCV': 10, 'ICML': 16, 'CVPR': 12, 'ICLR': 16, 'ECCV': 10, 'NeurIPS': 14, 'ACL': 16}
- 04 选定 110 篇写入 04_llm_multimodal_seed_cn.json；标题/摘要含 GitHub 提示 93 篇。按场次：{'EMNLP': 16, 'ICCV': 10, 'ICML': 16, 'CVPR': 12, 'ICLR': 16, 'ECCV': 10, 'NeurIPS': 14, 'ACL': 16}
- 04 选定 110 篇写入 04_llm_multimodal_seed_cn.json；标题/摘要含 GitHub 提示 93 篇。按场次：{'EMNLP': 16, 'ICCV': 10, 'ICML': 16, 'CVPR': 12, 'ICLR': 16, 'ECCV': 10, 'NeurIPS': 14, 'ACL': 16}

## 方向 04 完成（2026-10-30）

- 新增渠道：ACL Anthology 主卷 BibTeX（long/main，不含 Findings/short）、CVF Open Access（CVPR/ICCV）、ECVA（ECCV 2022/2024；ECCV 2026 列表尚未上线）。
- 补录会议日期：ACL 2026（2026-07-02 至 2026-07-07，San Diego）；EMNLP 2026（2026-10-24 至 2026-10-29，Budapest）。
- 选定并核验全文 **110** 篇：EMNLP 16、ICML 16、ICLR 16、ACL 16、NeurIPS 14、CVPR 12、ICCV 10、ECCV 10。年份 2022–2026。新下载 110。
- 排除：ACL Anthology 页脚 `acl-org/acl-anthology` 整库误克隆 17 个，已删除并加入黑名单；Endpoint Detection 论文 1 篇。
- 代码：有快照约 74 个。官方 A+B 见 progress_cn.csv。本轮最高 L1，不声称已复现。
- 续跑从方向 05 开始。

- 05 列表扫描：来源论文 46423，标题预筛 261，候选池 261
- arXiv `all:"code generation" OR all:"program repair"` 命中 5175，取回 120
- arXiv `all:"software engineering" AND all:"language model"` 命中 6405，取回 120
- arXiv `all:swe-bench OR all:humaneval` 命中 1360，取回 120
- arXiv `all:"autonomous software agent" OR all:"coding agent"` 命中 1643，取回 120
- arXiv `(all:"unit test generation" OR all:"bug localization") AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL)` 命中 26，取回 26
- arXiv `all:"repository-level" AND all:code` 命中 409，取回 120
- arXiv `ti:"code generation" AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL OR co:ICLR OR co:ICML OR co:NeurIPS)` 命中 151，取回 120
- arXiv `all:"program repair" AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA OR co:ACL)` 命中 53，取回 53
- arXiv `all:"language model" AND all:"software engineering" AND (co:ICSE OR co:FSE OR co:ASE OR co:ICLR)` 命中 489，取回 120
- arXiv `all:"issue resolution" OR all:"swe-agent" OR all:"coding agent"` 命中 1850，取回 120
- arXiv `all:"test generation" AND (all:llm OR all:"language model")` 命中 391，取回 120
- arXiv `all:"vulnerability detection" AND (all:code OR all:software) AND (co:ICSE OR co:FSE OR co:ASE OR co:ISSTA)` 命中 51，取回 51
- 05 选定 110 篇写入 05_coding_software_agents_seed_cn.json；标题/摘要含 GitHub 提示 64 篇。按场次：{'ICML': 15, 'NeurIPS': 14, 'ICLR': 6, 'ICSE': 20, 'EMNLP': 14, 'ACL': 15, 'ASE': 14, 'ISSTA': 4, 'FSE': 8}
- 05 选定 110 篇写入 05_coding_software_agents_seed_cn.json；标题/摘要含 GitHub 提示 64 篇。按场次：{'ICML': 15, 'NeurIPS': 14, 'ICLR': 6, 'ICSE': 20, 'EMNLP': 14, 'ACL': 15, 'ASE': 14, 'ISSTA': 4, 'FSE': 8}

## 方向 05 完成（2026-10-30）

- ICSE/FSE/ASE/ISSTA 无开放全文目录（researchr 为前端壳、ACM/IEEE 付费墙）；主会录用靠 arXiv comment/journal_ref 确认，PDF 用 arXiv 合法公开版。ACL/EMNLP 主卷与 ICML/NeurIPS 列表可用。
- 选定并核验全文 **110** 篇：ICSE 27、ICML 15、ASE 14、EMNLP 13、NeurIPS 12、ACL 12、FSE 8、ICLR 6、ISSTA 3。新下载 110。
- 剔除：QR 码生成、BIM 建筑布局、chart-to-code、表格 QA、事件结构 code 表示、LLM 安全评测等非软件智能体论文。
- 代码快照约 58 个。最高 L1，不声称已复现。
- 续跑从方向 06 开始。


## 列表抓取 2026-10-30
PMLR 主会卷、NeurIPS [2021, 2022, 2023, 2024, 2025]、IJCAI [2022, 2023, 2024, 2025, 2026]、ACL/EMNLP 主卷、CVF、ECCV 已缓存到 listings。
- 06 列表扫描：来源论文 1146，标题预筛 108，候选池 108
- 06 列表扫描：来源论文 1146，标题预筛 108，候选池 108
- arXiv `all:"inference serving" OR all:vllm OR all:pagedattention` 命中 0，取回 0
- arXiv `all:"distributed training"` 命中 817，取回 120
- arXiv `all:"inference serving" OR all:vllm OR all:pagedattention` 命中 810，取回 120
- arXiv `all:"machine learning system"` 命中 883，取回 120
- arXiv `all:"distributed training"` 命中 817，取回 120
- arXiv `(all:"inference engine" OR all:"GPU scheduling") AND (co:SOSP OR co:OSDI OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 5，取回 5
- arXiv `all:"machine learning system"` 命中 883，取回 120
- arXiv `all:mlsys OR all:"MLSys"` 命中 146，取回 120
- arXiv `(all:"inference engine" OR all:"GPU scheduling") AND (co:SOSP OR co:OSDI OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 5，取回 5
- arXiv `all:"pipeline parallelism" OR all:FSDP OR all:"zero redundancy"` 命中 327，取回 120
- arXiv `all:mlsys OR all:"MLSys"` 命中 146，取回 120
- arXiv `all:"kv cache" OR all:pagedattention OR all:vllm` 命中 2739，取回 120
- arXiv `all:"pipeline parallelism" OR all:FSDP OR all:"zero redundancy"` 命中 327，取回 120
- arXiv `(all:"distributed training" OR all:"inference serving") AND (co:OSDI OR co:SOSP OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 16，取回 16
- arXiv `all:"kv cache" OR all:pagedattention OR all:vllm` 命中 2739，取回 120
- arXiv `all:"gpu kernel" OR all:"cluster scheduling" AND (all:training OR all:inference)` 命中 397，取回 120
- arXiv `(all:"distributed training" OR all:"inference serving") AND (co:OSDI OR co:SOSP OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 16，取回 16
- arXiv `ti:"serving" AND (all:llm OR all:"language model") AND (co:OSDI OR co:SOSP OR co:MLSys OR co:NSDI)` 命中 22，取回 22
- arXiv `all:"gpu kernel" OR all:"cluster scheduling" AND (all:training OR all:inference)` 命中 397，取回 120
- arXiv `ti:"serving" AND (all:llm OR all:"language model") AND (co:OSDI OR co:SOSP OR co:MLSys OR co:NSDI)` 命中 22，取回 22
- arXiv `all:"inference serving" OR all:vllm OR all:pagedattention` 命中 0，取回 0
- arXiv `all:"distributed training"` 命中 817，取回 120
- arXiv `all:"machine learning system"` 命中 883，取回 120
- arXiv `(all:"inference engine" OR all:"GPU scheduling") AND (co:SOSP OR co:OSDI OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 5，取回 5
- arXiv `all:mlsys OR all:"MLSys"` 命中 146，取回 120
- arXiv `all:"pipeline parallelism" OR all:FSDP OR all:"zero redundancy"` 命中 327，取回 120
- arXiv `all:"kv cache" OR all:pagedattention OR all:vllm` 命中 2739，取回 120
- arXiv `(all:"distributed training" OR all:"inference serving") AND (co:OSDI OR co:SOSP OR co:NSDI OR co:ASPLOS OR co:MLSys)` 命中 16，取回 16
- arXiv `all:"gpu kernel" OR all:"cluster scheduling" AND (all:training OR all:inference)` 命中 397，取回 120
- arXiv `ti:"serving" AND (all:llm OR all:"language model") AND (co:OSDI OR co:SOSP OR co:MLSys OR co:NSDI)` 命中 22，取回 22
- 06 选定 61 篇写入 06_systems_mlsys_seed_cn.json；标题/摘要含 GitHub 提示 8 篇。按场次：{'MLSys': 31, 'SOSP': 3, 'ASPLOS': 3, 'OSDI': 13, 'NSDI': 11}

## 方向 06 完成（2026-10-30）

- 新增渠道：MLSys proceedings.mlsys.org；USENIX OSDI/NSDI technical-sessions（SOSP 不在 USENIX）。ASPLOS/ISCA/SC 付费墙，仅 arXiv 录用标注。
- 核验全文 **60** 篇（1 篇 MLSys 2023 PDF 404 未计入）。MLSys 31、OSDI 13、NSDI 11、SOSP 3、ASPLOS 3。低于 90–120，未用不相关网络论文凑数。
- 代码快照 23 个。vLLM 官方仓按页面链接克隆（depth 1，未拉权重）。最高 L1，不声称已复现。
- 续跑从方向 07 开始。

- 07 列表扫描：来源论文 2354，标题预筛 642，候选池 642
- arXiv `all:quadrotor OR all:uav OR all:quadcopter` 命中 0，取回 0
- arXiv `all:"learning-based control" OR all:"model predictive control"` 命中 0，取回 0
- 07 选定 110 篇写入 07_robotics_uav_control_seed_cn.json；标题/摘要含 GitHub 提示 0 篇。按场次：{'RSS': 30, 'CoRL': 66, 'L4DC': 14}

## 方向 07 完成（2026-10-30）

- RSS roboticsproceedings.org 开放全文（2022–2026）；CoRL/L4DC 来自 PMLR 主卷。
- ICRA/IROS/CDC/ACC：IEEE 付费墙；本轮 arXiv API 超时，未计入无公开全文论文。
- 选定并核验全文 **110** 篇：CoRL 66、RSS 30、L4DC 14。RSS 2025 扫描 PDF（0 字符）6 篇已替换。
- 代码快照 9 个（PDF 首页 GitHub 链接少）。最高 L1，不声称已复现。

## 全库完成

七个方向均已跑完。方向 03、06 因主会公开全文不足记为缺口，未凑数。未上传 GitHub，未运行训练。

