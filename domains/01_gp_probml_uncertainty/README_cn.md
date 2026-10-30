# 01 高斯过程、概率机器学习与不确定性

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**110** 篇（目标约 100，参考 90–120）
- 新下载 110，已有复用 0
- 有可获取代码（A/B/C）49 篇（44.5%）；官方完整实现（A）9 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 11 |
| 2023 | 26 |
| 2024 | 26 |
| 2025 | 27 |
| 2026 | 20 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| AISTATS | 2022 | 3 |
| AISTATS | 2023 | 4 |
| AISTATS | 2024 | 2 |
| AISTATS | 2025 | 4 |
| AISTATS | 2026 | 3 |
| COLT | 2022 | 1 |
| COLT | 2023 | 1 |
| COLT | 2024 | 2 |
| ICLR | 2022 | 1 |
| ICLR | 2023 | 3 |
| ICLR | 2024 | 5 |
| ICLR | 2025 | 8 |
| ICLR | 2026 | 5 |
| ICML | 2022 | 3 |
| ICML | 2023 | 7 |
| ICML | 2024 | 7 |
| ICML | 2025 | 6 |
| ICML | 2026 | 7 |
| NeurIPS | 2022 | 3 |
| NeurIPS | 2023 | 10 |
| NeurIPS | 2024 | 7 |
| NeurIPS | 2025 | 6 |
| UAI | 2023 | 1 |
| UAI | 2024 | 3 |
| UAI | 2025 | 3 |
| UAI | 2026 | 5 |

轨道合计：
- main: 110

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 9 |
| B | 作者官方部分实现 | 13 |
| C | 仅第三方复现 | 27 |
| D | 无代码、空仓或未找到 | 61 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 20.0%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. A Study of Bayesian Neural Network Surrogates for Bayesian Optimization

- 会议：ICLR 2024（main）
- 关系：直接研究目标任务；贝叶斯神经网络；Laplace 近似；深度核；HMC/NUTS；深度集成；贝叶斯优化；线性化 Laplace；核方法
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：贝叶斯神经网络、Laplace 近似、深度核、HMC/NUTS、深度集成、贝叶斯优化、线性化 Laplace、核方法。会议 ICLR 2024 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 2. Self-Attention through Kernel-Eigen Pair Sparse Variational Gaussian Processes

- 会议：ICML 2024（main）
- 关系：直接研究目标任务；高斯过程；GP 方法；变分 GP；稀疏 GP；不确定性估计；不确定性感知；变分推断
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：高斯过程、GP 方法、变分 GP、稀疏 GP、不确定性估计、不确定性感知、变分推断。会议 ICML 2024 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 3. Weakly-Supervised Residual Evidential Learning for Multi-Instance Uncertainty Estimation

- 会议：ICML 2024（main）
- 关系：可迁移的基础方法；预测不确定性；证据深度学习；不确定性估计；预测分布
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：可迁移的基础方法。命中：预测不确定性、证据深度学习、不确定性估计、预测分布。会议 ICML 2024 main 轨道。
- 前置条件：依赖声明; 测试。大型数据、权重未下载；本轮未运行。

### 4. Label-wise Aleatoric and Epistemic Uncertainty Quantification

- 会议：UAI 2024（main）
- 关系：直接研究目标任务；不确定性量化；认知不确定性；偶然不确定性
- 代码：类别 A，级别 L1；许可证 有 LICENSE 文件但未识别 SPDX/常用名称
- 理由：直接研究目标任务。命中：不确定性量化、认知不确定性、偶然不确定性。会议 UAI 2024 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 5. Offline Bayesian Aleatoric and Epistemic Uncertainty Quantification and Posterior Value Optimisation in Finite-State MDPs

- 会议：UAI 2024（main）
- 关系：直接研究目标任务；不确定性量化；认知不确定性；偶然不确定性
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：不确定性量化、认知不确定性、偶然不确定性。会议 UAI 2024 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 6. Meta-learning Adaptive Deep Kernel Gaussian Processes for Molecular Property Prediction

- 会议：ICLR 2023（main）
- 关系：直接研究目标任务；高斯过程；深度核；核方法
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：高斯过程、深度核、核方法。会议 ICLR 2023 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 7. Physics-Informed Variational State-Space Gaussian Processes

- 会议：NeurIPS 2024（main）
- 关系：直接研究目标任务；高斯过程；状态空间 GP
- 代码：类别 A，级别 L1；许可证 有 LICENSE 文件但未识别 SPDX/常用名称
- 理由：直接研究目标任务。命中：高斯过程、状态空间 GP。会议 NeurIPS 2024 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 8. Improving Linear System Solvers for Hyperparameter Optimisation in Iterative Gaussian Processes

- 会议：NeurIPS 2024（main）
- 关系：直接研究目标任务；高斯过程；迭代 GP
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：高斯过程、迭代 GP。会议 NeurIPS 2024 main 轨道。
- 前置条件：依赖声明; 测试。大型数据、权重未下载；本轮未运行。

### 9. Improving TabPFN's Synthetic Data Generation by Integrating Causal Structure

- 会议：UAI 2026（main）
- 关系：直接研究目标任务；PFN/TabPFN
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：PFN/TabPFN。会议 UAI 2026 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 10. PFNs4BO: In-Context Learning for Bayesian Optimization

- 会议：ICML 2023（main）
- 关系：直接研究目标任务；Neural Process；贝叶斯神经网络；PFN/TabPFN；贝叶斯优化；预测分布；后验预测；上下文贝叶斯推断
- 代码：类别 C，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：Neural Process、贝叶斯神经网络、PFN/TabPFN、贝叶斯优化、预测分布、后验预测、上下文贝叶斯推断。会议 ICML 2023 main 轨道。
- 前置条件：测试; 官方归属未证实，按第三方实现登记。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

对照现有高斯过程文献库，补充近五年主会中的 GP、共形预测、贝叶斯神经网络与校准方法，以及可静态核验的官方实现入口。

## 缺口

- 未运行训练或评测；缺数据、权重和硬件验证。
- 付费墙会议论文若无合法公开全文则未计入。
- 边界日期条目若精度只有年份，未计入或在窗口说明中标注。

续跑：`python3 -I scripts/run_en.py domain 01`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
