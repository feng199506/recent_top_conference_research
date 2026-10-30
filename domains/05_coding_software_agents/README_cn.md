# 05 Coding 与软件智能体

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**110** 篇（目标约 100，参考 90–120）
- 新下载 110，已有复用 0
- 有可获取代码（A/B/C）58 篇（52.7%）；官方完整实现（A）6 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 5 |
| 2023 | 15 |
| 2024 | 30 |
| 2025 | 30 |
| 2026 | 30 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| ACL | 2022 | 1 |
| ACL | 2024 | 4 |
| ACL | 2025 | 4 |
| ACL | 2026 | 3 |
| ASE | 2023 | 2 |
| ASE | 2024 | 7 |
| ASE | 2025 | 5 |
| EMNLP | 2023 | 1 |
| EMNLP | 2024 | 2 |
| EMNLP | 2025 | 1 |
| EMNLP | 2026 | 9 |
| FSE | 2022 | 2 |
| FSE | 2023 | 3 |
| FSE | 2024 | 3 |
| ICLR | 2024 | 2 |
| ICLR | 2025 | 1 |
| ICLR | 2026 | 3 |
| ICML | 2023 | 5 |
| ICML | 2024 | 1 |
| ICML | 2025 | 5 |
| ICML | 2026 | 4 |
| ICSE | 2022 | 1 |
| ICSE | 2023 | 1 |
| ICSE | 2024 | 6 |
| ICSE | 2025 | 8 |
| ICSE | 2026 | 11 |
| ISSTA | 2023 | 1 |
| ISSTA | 2024 | 1 |
| ISSTA | 2025 | 1 |
| NeurIPS | 2022 | 1 |
| NeurIPS | 2023 | 2 |
| NeurIPS | 2024 | 4 |
| NeurIPS | 2025 | 5 |

轨道合计：
- main: 104
- long: 4
- datasets_and_benchmarks: 2

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 6 |
| B | 作者官方部分实现 | 8 |
| C | 仅第三方复现 | 44 |
| D | 无代码、空仓或未找到 | 52 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 12.7%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. AST-T5: Structure-Aware Pretraining for Code Generation and Understanding

- 会议：ICML 2024（main）
- 关系：直接研究目标任务；代码生成；代码评测
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：代码生成、代码评测。会议 ICML 2024 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 2. CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning

- 会议：NeurIPS 2022（main）
- 关系：直接研究目标任务；代码生成；代码评测
- 代码：类别 A，级别 L1；许可证 bsd 3
- 理由：直接研究目标任务。命中：代码生成、代码评测。会议 NeurIPS 2022 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 3. CodeChain: Towards Modular Code Generation Through Chain of Self-revisions with Representative Sub-modules

- 会议：ICLR 2024（main）
- 关系：直接研究目标任务；代码生成；代码评测
- 代码：类别 A，级别 L0；许可证 apache license
- 理由：直接研究目标任务。命中：代码生成、代码评测。会议 ICLR 2024 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 4. ROCODE: Integrating Backtracking Mechanism and Program Analysis in Large Language Models for Code Generation

- 会议：ICSE 2025（main）
- 关系：直接研究目标任务；代码生成；程序分析
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：代码生成、程序分析。会议 ICSE 2025 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 5. Contextualized Data-Wrangling Code Generation in Computational Notebooks

- 会议：ASE 2024（main）
- 关系：直接研究目标任务；代码生成
- 代码：类别 A，级别 L1；许可证 bsd 3
- 理由：直接研究目标任务。命中：代码生成。会议 ASE 2024 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 6. LEVER: Learning to Verify Language-to-Code Generation with Execution

- 会议：ICML 2023（main）
- 关系：直接研究目标任务；代码生成
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：代码生成。会议 ICML 2023 main 轨道。
- 前置条件：测试。大型数据、权重未下载；本轮未运行。

### 7. Nemotron-CORTEXA: Enhancing LLM Agents for Software Engineering Tasks via Improved Localization and Solution Diversity

- 会议：ICML 2025（main）
- 关系：直接研究目标任务；代码生成；软件工程/智能体；仓库级；代码评测；issue 解决
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：代码生成、软件工程/智能体、仓库级、代码评测、issue 解决。会议 ICML 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 8. Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents

- 会议：ICSE 2026（main）
- 关系：直接研究目标任务；软件工程/智能体；仓库级；代码评测；issue 解决
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：软件工程/智能体、仓库级、代码评测、issue 解决。会议 ICSE 2026 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 9. daVinci-Dev: Agent-native Mid-training for Software Engineering

- 会议：ICML 2026（main）
- 关系：直接研究目标任务；代码生成；软件工程/智能体；编码智能体；代码评测
- 代码：类别 C，级别 L0；许可证 apache license
- 理由：直接研究目标任务。命中：代码生成、软件工程/智能体、编码智能体、代码评测。会议 ICML 2026 main 轨道。
- 前置条件：仅部分实现可见。大型数据、权重未下载；本轮未运行。

### 10. SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents

- 会议：NeurIPS 2025（main）
- 关系：直接研究目标任务；代码生成；软件工程/智能体；编码智能体；代码评测
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：代码生成、软件工程/智能体、编码智能体、代码评测。会议 NeurIPS 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

用于代码生成、程序修复、测试生成与软件智能体的方法对照。

## 缺口

- 未运行训练或评测；缺数据、权重和硬件验证。
- 付费墙会议论文若无合法公开全文则未计入。
- 边界日期条目若精度只有年份，未计入或在窗口说明中标注。

续跑：`python3 -I scripts/run_en.py domain 05`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
