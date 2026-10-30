# 06 训练、推理及生产系统

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**60** 篇（目标约 100，参考 90–120）
- 新下载 60，已有复用 0
- 有可获取代码（A/B/C）23 篇（38.3%）；官方完整实现（A）4 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 3 |
| 2023 | 3 |
| 2024 | 9 |
| 2025 | 17 |
| 2026 | 28 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| ASPLOS | 2024 | 1 |
| ASPLOS | 2025 | 2 |
| MLSys | 2022 | 2 |
| MLSys | 2023 | 2 |
| MLSys | 2024 | 4 |
| MLSys | 2025 | 10 |
| MLSys | 2026 | 12 |
| NSDI | 2022 | 1 |
| NSDI | 2025 | 2 |
| NSDI | 2026 | 8 |
| OSDI | 2024 | 4 |
| OSDI | 2025 | 1 |
| OSDI | 2026 | 8 |
| SOSP | 2023 | 1 |
| SOSP | 2025 | 2 |

轨道合计：
- main: 60

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 4 |
| B | 作者官方部分实现 | 1 |
| C | 仅第三方复现 | 18 |
| D | 无代码、空仓或未找到 | 37 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 8.3%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching

- 会议：MLSys 2026（main）
- 关系：直接研究目标任务；推理系统；KV/推理引擎；推理引擎
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：推理系统、KV/推理引擎、推理引擎。会议 MLSys 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 2. LServe: Efficient Long-sequence LLM Serving with Unified Sparse Attention

- 会议：MLSys 2025（main）
- 关系：直接研究目标任务；KV/推理引擎；推理引擎；模型服务
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：KV/推理引擎、推理引擎、模型服务。会议 MLSys 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 3. FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management

- 会议：MLSys 2026（main）
- 关系：可迁移的基础方法；KV/推理引擎
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：可迁移的基础方法。命中：KV/推理引擎。会议 MLSys 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 4. QServe:W4A8KV4 Quantization and System Co-design for Efficient LLM Serving

- 会议：MLSys 2025（main）
- 关系：直接研究目标任务；模型服务
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：模型服务。会议 MLSys 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 5. FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving

- 会议：MLSys 2025（main）
- 关系：直接研究目标任务；推理系统；KV/推理引擎；推理引擎；模型服务
- 代码：类别 C，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：推理系统、KV/推理引擎、推理引擎、模型服务。会议 MLSys 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 6. Efficient Memory Management for Large Language Model Serving with PagedAttention

- 会议：SOSP 2023（main）
- 关系：直接研究目标任务；KV/推理引擎；推理引擎；模型服务
- 代码：类别 C，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：KV/推理引擎、推理引擎、模型服务。会议 SOSP 2023 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 7. vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention

- 会议：ASPLOS 2025（main）
- 关系：直接研究目标任务；KV/推理引擎；推理引擎；模型服务
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：KV/推理引擎、推理引擎、模型服务。会议 ASPLOS 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 8. NEST: Network- and Memory-Aware Device Placement For Distributed Deep Learning

- 会议：MLSys 2026（main）
- 关系：直接研究目标任务；训练系统；分布式；通信；生产系统
- 代码：类别 C，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：训练系统、分布式、通信、生产系统。会议 MLSys 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 9. GhostServe: A Lightweight Checkpointing System in the Shadow for Fault-Tolerant LLM Serving

- 会议：MLSys 2026（main）
- 关系：直接研究目标任务；分布式；KV/推理引擎；模型服务
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：分布式、KV/推理引擎、模型服务。会议 MLSys 2026 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 10. Breaking the Ice: Analyzing Cold Start Latency in vLLM

- 会议：MLSys 2026（main）
- 关系：直接研究目标任务；KV/推理引擎；推理引擎
- 代码：类别 C，级别 L0；许可证 apache license
- 理由：直接研究目标任务。命中：KV/推理引擎、推理引擎。会议 MLSys 2026 main 轨道。
- 前置条件：仅部分实现可见。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

用于训练/推理系统设计、并行策略与生产服务的方法对照。

## 缺口

- SOSP 不在 USENIX 开放列表（ACM）；ISCA/SC/ASPLOS 主会 PDF 多在付费墙，本轮仅收 arXiv comment 能确认录用且全文公开的条目。
- 已核验约 60 篇（MLSys/OSDI/NSDI 为主），低于 90–120。未把与训练/推理服务无关的网络/体系结构论文凑数。
- 未运行训练或评测；缺数据、权重和硬件验证。

续跑：`python3 -I scripts/run_en.py domain 06`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
