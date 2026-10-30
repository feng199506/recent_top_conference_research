# 03 工业过程监控

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**39** 篇（目标约 100，参考 90–120）
- 新下载 39，已有复用 0
- 有可获取代码（A/B/C）14 篇（35.9%）；官方完整实现（A）6 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 4 |
| 2023 | 4 |
| 2024 | 4 |
| 2025 | 18 |
| 2026 | 9 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| AAAI | 2025 | 2 |
| AAAI | 2026 | 2 |
| ICLR | 2025 | 2 |
| ICML | 2022 | 3 |
| ICML | 2025 | 1 |
| ICML | 2026 | 4 |
| IJCAI | 2022 | 1 |
| IJCAI | 2024 | 3 |
| IJCAI | 2025 | 3 |
| IJCAI | 2026 | 2 |
| KDD | 2023 | 1 |
| KDD | 2024 | 1 |
| KDD | 2026 | 1 |
| NeurIPS | 2023 | 3 |
| NeurIPS | 2025 | 10 |

轨道合计：
- datasets_and_benchmarks: 3
- main: 36

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 6 |
| B | 作者官方部分实现 | 2 |
| C | 仅第三方复现 | 6 |
| D | 无代码、空仓或未找到 | 25 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 20.5%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. Harnessing Vision-Language Models for Time Series Anomaly Detection

- 会议：AAAI 2026（main）
- 关系：可迁移的基础方法；异常检测；状态监控
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：异常检测、状态监控。会议 AAAI 2026 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 2. ADPretrain: Advancing Industrial Anomaly Detection via Anomaly Representation Pretraining

- 会议：NeurIPS 2025（main）
- 关系：直接研究目标任务；异常检测
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：异常检测。会议 NeurIPS 2025 main 轨道。
- 前置条件：测试。大型数据、权重未下载；本轮未运行。

### 3. Nominality Score Conditioned Time Series Anomaly Detection by Point/Sequential Reconstruction

- 会议：NeurIPS 2023（main）
- 关系：可迁移的基础方法；异常检测
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：异常检测。会议 NeurIPS 2023 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 4. CrossAD: Time Series Anomaly Detection with Cross-scale Associations and Cross-window Modeling

- 会议：NeurIPS 2025（main）
- 关系：可迁移的基础方法；异常检测
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：异常检测。会议 NeurIPS 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 5. CATCH: Channel-Aware multivariate Time Series Anomaly Detection via Frequency Patching

- 会议：ICLR 2025（main）
- 关系：可迁移的基础方法；异常检测
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：异常检测。会议 ICLR 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 6. CausalTrace: A Neurosymbolic Causal Analysis Agent for Smart Manufacturing

- 会议：AAAI 2026（main）
- 关系：直接研究目标任务；根因
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：根因。会议 AAAI 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 7. NoBOOM: Chemical Process Datasets for Industrial Anomaly Detection

- 会议：NeurIPS 2025（datasets_and_benchmarks）
- 关系：直接研究目标任务；异常检测；过程工业
- 代码：类别 B，级别 L0；许可证 mit license
- 理由：直接研究目标任务。命中：异常检测、过程工业。会议 NeurIPS 2025 datasets_and_benchmarks 轨道。
- 前置条件：仅部分实现可见。大型数据、权重未下载；本轮未运行。

### 8. Fault Diagnosis in REDNet Model Space

- 会议：IJCAI 2025（main）
- 关系：直接研究目标任务；故障检测诊断
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：故障检测诊断。会议 IJCAI 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 9. POND: Multi-Source Time Series Domain Adaptation with Information-Aware Prompt Tuning

- 会议：KDD 2024（main）
- 关系：直接研究目标任务；故障检测诊断
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：故障检测诊断。会议 KDD 2024 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 10. DSPR: Dual-Stream Physics-Residual Networks for Trustworthy Industrial Time Series Forecasting

- 会议：KDD 2026（main）
- 关系：直接研究目标任务；工业过程
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：工业过程。会议 KDD 2026 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

工业过程监控主会论文稀缺。本方向保留化学过程/智能制造/软测量相关主会工作，并以多变量时序异常检测与因果根因作为可迁移方法，不把视觉巡检或 IT 运维论文充数。

## 缺口

- 近五年 ICML/NeurIPS/ICLR/KDD/AAAI/IJCAI 主会中，直接面向化工过程监控、软测量、TE 过程的论文很少；该方向文献主要在 IEEE 过程控制/仪表期刊，本轮不把期刊算进主集合。
- 已核验 39 篇（直接工业/制造相关 11 篇，可迁移的多变量时序异常检测与因果根因 28 篇），低于 90–120 目标。**未**用 3D/图/视频/通用视觉异常检测或微服务根因论文凑数。
- 官方代码 A+B 约两成；部分 NeurIPS 2025 工业基准尚未放出完整仓库。
- 未运行训练或评测；缺数据、权重和硬件验证。
- FlowFuse 仓库 clone 需登录，按 D 登记。

续跑：`python3 -I scripts/run_en.py domain 03`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
