# 近五年顶会主会文献库（整理完毕）

根目录：[`/root/recent_top_conference_research`](./)  
检索日：2026-10-30（UTC+9）。收录窗口：正式会议发表日 **2021-10-30 至 2026-10-30**。  
本轮只收集整理：不运行代码、不训练、不部署、不上传 GitHub。代码核验最高到 **L1**（静态入口/配置/依赖），**不声称已复现**。

## 规模

| 方向 | 状态 | 已核验全文 | 目标 | A | B | C | D | 官方 A+B | 有代码 A/B/C |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 01 高斯过程、概率机器学习与不确定性 | 已完成 | 110 | 100 | 9 | 13 | 27 | 61 | 20.0% | 49/110 |
| 02 时间序列、空间时间预测及环境应用 | 已完成 | 110 | 100 | 14 | 12 | 45 | 39 | 23.6% | 71/110 |
| 03 工业过程监控 | 已完成（主会缺口） | 39 | 100 | 6 | 2 | 6 | 25 | 20.5% | 14/39 |
| 04 大语言模型与多模态 | 已完成 | 110 | 100 | 22 | 11 | 41 | 36 | 30.0% | 74/110 |
| 05 Coding 与软件智能体 | 已完成 | 110 | 100 | 6 | 8 | 44 | 52 | 12.7% | 58/110 |
| 06 训练、推理及生产系统 | 已完成（主会缺口） | 60 | 100 | 4 | 1 | 18 | 37 | 8.3% | 23/60 |
| 07 机器人、无人机与学习控制 | 已完成 | 110 | 100 | 2 | 0 | 7 | 101 | 1.8% | 9/110 |
| **合计** | | **649** | 700 | **63** | **47** | **188** | **351** | **16.9%** | **298/649** |

筛选目标「每方向 ≥70% 官方可获取代码」**未达成**。未用低相关、有代码论文替换关键理论文或凑数。第三方复现记为 C，不计入官方率。

全文 PDF：[`papers/`](papers/)（约 642 个文件；少量因文件名碰撞覆盖）。代码快照：[`code/`](code/)（298 个仓库，`git clone --depth 1`，跳过 LFS 与子模块，未下数据集/权重）。目录：[`catalog_cn.csv`](catalog_cn.csv)、[`code_availability_cn.csv`](code_availability_cn.csv)、[`progress_cn.csv`](progress_cn.csv)。分方向说明：`domains/*/README_cn.md`。

## 会议与渠道（能用的才用）

- PMLR 主卷：ICML / AISTATS / COLT / UAI / CoRL / L4DC  
- NeurIPS：papers.nips.cc 主会与 Datasets and Benchmarks  
- ICLR、KDD、AAAI：arXiv comment / journal_ref 确认录用 + arXiv PDF  
- IJCAI：ijcai.org 主会轨道  
- ACL / EMNLP：Anthology **long / main** 卷（不含 Findings、short、workshop）  
- CVPR / ICCV：CVF Open Access；ECCV：ECVA（2022/2024；2026 列表未上线）  
- MLSys：proceedings.mlsys.org  
- OSDI / NSDI：USENIX technical-sessions 开放 PDF  
- RSS：roboticsproceedings.org  

不可用、未绕过：DBLP Cloudflare、Semantic Scholar / OpenAlex 429、Papers with Code / OpenReview API 返回 HTML。IEEE/ACM 付费墙论文若无合法公开全文则不计入主集合。不编造 CCF 等级。AISTATS、UAI、MLSys、L4DC、CDC、ACC 标为补充专业会议。

## 方向摘要与优先阅读（各 10 篇）

排序只反映与该方向的直接相关性和代码完整度，不是方法优劣判断。前置条件见各方向 README。

### 01 高斯过程 / 概率 ML / 不确定性

ICML 30、NeurIPS 26、ICLR 22、AISTATS 16、UAI 12、COLT 4。保留 COLT 理论文。  
用途：对照已有高斯过程文献库中的核方法、变分推断、共形预测与校准。

1. A Study of Bayesian Neural Network Surrogates for Bayesian Optimization  
2. Self-Attention through Kernel-Eigen Pair Sparse Variational Gaussian Processes  
3. Weakly-Supervised Residual Evidential Learning for Multi-Instance Uncertainty Estimation  
4. Label-wise Aleatoric and Epistemic Uncertainty Quantification  
5. Offline Bayesian Aleatoric and Epistemic Uncertainty Quantification and Posterior Value Optimisation in Finite-State MDPs  
6. Meta-learning Adaptive Deep Kernel Gaussian Processes for Molecular Property Prediction  
7. Physics-Informed Variational State-Space Gaussian Processes  
8. Improving Linear System Solvers for Hyperparameter Optimisation in Iterative Gaussian Processes  
9. Improving TabPFN's Synthetic Data Generation by Integrating Causal Structure  
10. PFNs4BO: In-Context Learning for Bayesian Optimization  

缺口：官方代码不足 70%；3 篇作者姓氏变音符号标 pending。

### 02 时间序列 / 时空 / 环境

ICML 24、NeurIPS 21、ICLR 18、IJCAI 16、AAAI 16、KDD 15。  
用途：空气质量/水文/能源预测与分布漂移处理。

1. FSTLLM: Spatio-Temporal LLM for Few Shot Time Series Forecasting  
2. Explaining Time Series via Contrastive and Locally Sparse Perturbations  
3. SEMPO: Lightweight Foundation Models for Time Series Forecasting  
4. CANDI: Curated Test-Time Adaptation for Multivariate Time-Series Anomaly Detection Under Distribution Shift  
5. Tiny Time Mixers (TTMs)  
6. Deciphering Spatio-Temporal Graph Forecasting: A Causal Lens and Treatment  
7. FourierGNN  
8. Online Irregular Multivariate Time Series Forecasting via Uncertainty-Driven Dual-Expert Calibration  
9. Battling the Non-stationarity in Time Series Forecasting via Test-time Adaptation  
10. Dish-TS  

曾替换：视频显著性论文、2 页 PyPOTS 短文。

### 03 工业过程监控（主会缺口，未凑数）

NeurIPS 13、IJCAI 9、ICML 8、AAAI 4、KDD 3、ICLR 2。直接工业/制造 11 篇，可迁移多变量时序异常检测与因果根因 28 篇。  
用途：化工过程、智能制造、软测量对照；时序异常/根因可迁移。

1. Harnessing Vision-Language Models for Time Series Anomaly Detection  
2. ADPretrain: Advancing Industrial Anomaly Detection via Anomaly Representation Pretraining  
3. Nominality Score Conditioned Time Series Anomaly Detection by Point/Sequential Reconstruction  
4. CrossAD  
5. CATCH  
6. CausalTrace: A Neurosymbolic Causal Analysis Agent for Smart Manufacturing  
7. NoBOOM: Chemical Process Datasets for Industrial Anomaly Detection  
8. Fault Diagnosis in REDNet Model Space  
9. POND  
10. DSPR  

缺口：该方向文献主要在 IEEE 过程控制期刊，指定主会很少。未用 3D/图/视频异常或微服务根因凑到 90 篇。`FlowFuse` 仓需登录，按 D。

### 04 大语言模型与多模态

EMNLP 16、ICML 16、ICLR 16、ACL 16、NeurIPS 14、CVPR 12、ICCV 10、ECCV 10。  
用途：对齐、RAG、工具使用、VLM。

1. Mario: Multimodal Graph Reasoning with Large Language Models  
2. Fusion in Your Way（图像融合 + DPO，偏可迁移）  
3. M4-RAG  
4. Unveiling Typographic Deceptions  
5. VLMaterial  
6. GraphVLM  
7. AGFT  
8. NavGPT-2  
9. Emotion-LLaMA  
10. MMed-RAG  

曾误克隆 `acl-org/acl-anthology` 整库 17 次，已删除并加入黑名单。

### 05 Coding 与软件智能体

ICSE 27、ICML 15、ASE 14、EMNLP 13、NeurIPS 12、ACL 12、FSE 8、ICLR 6、ISSTA 3。ICSE 等靠 arXiv 录用标注 + arXiv PDF。  
用途：代码生成、程序修复、仓库级 issue、测试生成。

1. AST-T5  
2. CodeRL  
3. CodeChain  
4. ROCODE  
5. Contextualized Data-Wrangling Code Generation in Computational Notebooks  
6. LEVER  
7. Nemotron-CORTEXA  
8. Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents  
9. daVinci-Dev  
10. SWE-rebench  

剔除：QR 码、BIM 建筑、chart-to-code、表格 QA 等。researchr.org 仅为前端壳，未解析出论文列表。

### 06 训练 / 推理 / 生产系统（主会缺口）

MLSys 30（补充会议）、OSDI 13、NSDI 11、SOSP 3、ASPLOS 3。ISCA/SC 无合法公开全文条目。  
用途：LLM serving、KV cache、流水线并行、集群调度。

1. BatchLLM  
2. LServe  
3. FlexiCache  
4. QServe  
5. FlashInfer  
6. Efficient Memory Management for Large Language Model Serving with PagedAttention  
7. vAttention  
8. NEST  
9. GhostServe  
10. Breaking the Ice: Analyzing Cold Start Latency in vLLM  

MLSys 2023 *Breadth-First Pipeline Parallelism* PDF 404，未计入。未把与训练/推理无关的网络论文凑数。

### 07 机器人 / 无人机 / 学习控制

CoRL 72、RSS 24、L4DC 14。ICRA/IROS/CDC/ACC：IEEE 付费墙，且本轮后期 arXiv API 超时，未计入。  
用途：四旋翼、操作、仿人/腿式、MPC 与控制障碍函数、sim-to-real。

1. Sequence Modeling for Time-Optimal Quadrotor Trajectory Optimization with Sampling-based Robustness Analysis  
2. DATT: Deep Adaptive Trajectory Tracking for Quadrotor Control  
3. Sim-to-Real Reinforcement Learning for Vision-Based Dexterous Manipulation on Humanoids  
4. Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching  
5. Sampling-based System Identification with Active Exploration for Legged Sim2Real Learning  
6. i-Sim2Real  
7. HAIC  
8. Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning  
9. Safe Exploration in Reinforcement Learning: Training Backup Control Barrier Functions  
10. Efficient imitation learning with conservative world models  

RSS 2025 部分 PDF 为扫描件（0 可提取字符），已替换。

## 失败与排除（主集合未计入或已替换）

见 [`download_failures_cn.csv`](download_failures_cn.csv)。主要包括：历史核验脚本 `chars` 未定义（随后已修，论文已重新核验入集）、PyPOTS 短文、MLSys 2023 一篇 404、RSS 2025 扫描 PDF（已换文）。误克隆的 `mlresearch/vXXX` 整卷与 `acl-org/acl-anthology` 已删。NeurIPS 2026、ICML Position 论文不收录。

## 路径

| 内容 | 路径 |
|---|---|
| 库根 | [`/root/recent_top_conference_research`](./) |
| 全文 | [`/root/recent_top_conference_research/papers`](papers/) |
| 代码快照 | [`/root/recent_top_conference_research/code`](code/) |
| 总目录 | [`/root/recent_top_conference_research/catalog_cn.csv`](catalog_cn.csv) |
| 进度 | [`/root/recent_top_conference_research/progress_cn.csv`](progress_cn.csv) |
| 检索日志 | [`/root/recent_top_conference_research/search_log_cn.md`](search_log_cn.md) |
| 续跑 | [`/root/recent_top_conference_research/guides/resume_cn.md`](guides/resume_cn.md) |
| 列表缓存 | `/root/.cache/rtcr_lit/listings` |

已有文献库仅核验后复制、未移动：`/root/gaussian_process_literature` 等。本轮 PDF 均为新下载，复用计数为 0。

## 续跑

七个方向均已跑完。若只补目录：

```bash
python3 -I scripts/catalog_en.py all
```

补某一方向的代码或 PDF（已成功的 sid 会跳过）：

```bash
python3 -I scripts/download_en.py papers 03
python3 -I scripts/code_en.py fetch 03
```

不要扩大年份或把补充材料算进主集合。
