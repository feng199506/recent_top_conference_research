# 04 大语言模型与多模态

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**110** 篇（目标约 100，参考 90–120）
- 新下载 110，已有复用 0
- 有可获取代码（A/B/C）74 篇（67.3%）；官方完整实现（A）22 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 2 |
| 2023 | 11 |
| 2024 | 32 |
| 2025 | 37 |
| 2026 | 28 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| ACL | 2022 | 1 |
| ACL | 2023 | 4 |
| ACL | 2024 | 4 |
| ACL | 2025 | 3 |
| ACL | 2026 | 4 |
| CVPR | 2025 | 4 |
| CVPR | 2026 | 8 |
| ECCV | 2024 | 9 |
| ECCV | 2026 | 1 |
| EMNLP | 2022 | 1 |
| EMNLP | 2023 | 5 |
| EMNLP | 2024 | 7 |
| EMNLP | 2025 | 3 |
| ICCV | 2025 | 10 |
| ICLR | 2024 | 4 |
| ICLR | 2025 | 6 |
| ICLR | 2026 | 6 |
| ICML | 2024 | 4 |
| ICML | 2025 | 3 |
| ICML | 2026 | 9 |
| NeurIPS | 2023 | 2 |
| NeurIPS | 2024 | 4 |
| NeurIPS | 2025 | 8 |

轨道合计：
- main: 103
- long: 4
- datasets_and_benchmarks: 3

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 22 |
| B | 作者官方部分实现 | 11 |
| C | 仅第三方复现 | 41 |
| D | 无代码、空仓或未找到 | 36 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 30.0%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. Mario: Multimodal Graph Reasoning with Large Language Models

- 会议：CVPR 2026（main）
- 关系：直接研究目标任务；大语言模型；预训练；对齐；多模态；视觉语言模型；推理；评测
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：大语言模型、预训练、对齐、多模态、视觉语言模型、推理、评测。会议 CVPR 2026 main 轨道。
- 前置条件：测试。大型数据、权重未下载；本轮未运行。

### 2. Fusion in Your Way: Aligning Image Fusion with Heterogeneous Demands via Direct Preference Optimization

- 会议：CVPR 2026（main）
- 关系：直接研究目标任务；对齐；多模态；视觉语言模型；评测；偏好优化；扩散多模态
- 代码：类别 A，级别 L1；许可证 有 LICENSE 文件但未识别 SPDX/常用名称
- 理由：直接研究目标任务。命中：对齐、多模态、视觉语言模型、评测、偏好优化、扩散多模态。会议 CVPR 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 3. M4-RAG: A Massive-Scale Multilingual Multi-Cultural Multimodal RAG

- 会议：CVPR 2026（main）
- 关系：直接研究目标任务；RAG；多模态；视觉语言模型；多语言；评测；视觉语言
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：RAG、多模态、视觉语言模型、多语言、评测、视觉语言。会议 CVPR 2026 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 4. Unveiling Typographic Deceptions: Insights of the Typographic Vulnerability in Large Vision-Language Model

- 会议：ECCV 2024（main）
- 关系：直接研究目标任务；大语言模型；预训练；多模态；视觉语言模型；评测
- 代码：类别 A，级别 L0；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：大语言模型、预训练、多模态、视觉语言模型、评测。会议 ECCV 2024 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 5. VLMaterial: Procedural Material Generation with Large Vision-Language Models

- 会议：ICLR 2025（main）
- 关系：直接研究目标任务；大语言模型；预训练；多模态；视觉语言模型；评测
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：大语言模型、预训练、多模态、视觉语言模型、评测。会议 ICLR 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 6. GraphVLM: Benchmarking Vision Language Models for Multimodal Graph Learning

- 会议：CVPR 2026（main）
- 关系：直接研究目标任务；大语言模型；多模态；视觉语言模型；推理；评测
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：大语言模型、多模态、视觉语言模型、推理、评测。会议 CVPR 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 7. AGFT: Alignment-Guided Fine-Tuning for Zero-Shot Adversarial Robustness of Vision-Language Models

- 会议：CVPR 2026（main）
- 关系：直接研究目标任务；预训练；对齐；多模态；视觉语言模型；评测
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：预训练、对齐、多模态、视觉语言模型、评测。会议 CVPR 2026 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 8. NavGPT-2: Unleashing Navigational Reasoning Capability for Large Vision-Language Models

- 会议：ECCV 2024（main）
- 关系：直接研究目标任务；大语言模型；多模态；视觉语言模型；推理
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：大语言模型、多模态、视觉语言模型、推理。会议 ECCV 2024 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 9. Emotion-LLaMA: Multimodal Emotion Recognition and Reasoning with Instruction Tuning

- 会议：NeurIPS 2024（main）
- 关系：直接研究目标任务；大语言模型；对齐；多模态；推理；评测
- 代码：类别 A，级别 L1；许可证 有 LICENSE 文件但未识别 SPDX/常用名称
- 理由：直接研究目标任务。命中：大语言模型、对齐、多模态、推理、评测。会议 NeurIPS 2024 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 10. MMed-RAG: Versatile Multimodal RAG System for Medical Vision Language Models

- 会议：ICLR 2025（main）
- 关系：直接研究目标任务；对齐；RAG；多模态；视觉语言模型
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：对齐、RAG、多模态、视觉语言模型。会议 ICLR 2025 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

用于大语言模型对齐、检索增强、工具使用与视觉语言模型的方法对照和官方实现入口。

## 缺口

- 未运行训练或评测；缺数据、权重和硬件验证。
- 付费墙会议论文若无合法公开全文则未计入。
- 边界日期条目若精度只有年份，未计入或在窗口说明中标注。

续跑：`python3 -I scripts/run_en.py domain 04`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
