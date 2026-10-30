# 02 时间序列、空间时间预测及环境应用

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**110** 篇（目标约 100，参考 90–120）
- 新下载 110，已有复用 0
- 有可获取代码（A/B/C）71 篇（64.5%）；官方完整实现（A）14 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2022 | 3 |
| 2023 | 17 |
| 2024 | 19 |
| 2025 | 30 |
| 2026 | 41 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| AAAI | 2023 | 2 |
| AAAI | 2025 | 3 |
| AAAI | 2026 | 11 |
| ICLR | 2023 | 1 |
| ICLR | 2024 | 6 |
| ICLR | 2025 | 2 |
| ICLR | 2026 | 9 |
| ICML | 2022 | 2 |
| ICML | 2023 | 3 |
| ICML | 2024 | 2 |
| ICML | 2025 | 8 |
| ICML | 2026 | 9 |
| IJCAI | 2023 | 4 |
| IJCAI | 2024 | 1 |
| IJCAI | 2025 | 7 |
| IJCAI | 2026 | 4 |
| KDD | 2023 | 1 |
| KDD | 2024 | 1 |
| KDD | 2025 | 5 |
| KDD | 2026 | 8 |
| NeurIPS | 2022 | 1 |
| NeurIPS | 2023 | 6 |
| NeurIPS | 2024 | 9 |
| NeurIPS | 2025 | 5 |

轨道合计：
- main: 110

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 14 |
| B | 作者官方部分实现 | 12 |
| C | 仅第三方复现 | 45 |
| D | 无代码、空仓或未找到 | 39 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 23.6%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. FSTLLM: Spatio-Temporal LLM for Few Shot Time Series Forecasting

- 会议：ICML 2025（main）
- 关系：直接研究目标任务；时间序列；时空；时序图/点过程；预测
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：时间序列、时空、时序图/点过程、预测。会议 ICML 2025 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 2. Explaining Time Series via Contrastive and Locally Sparse Perturbations

- 会议：ICLR 2024（main）
- 关系：直接研究目标任务；时间序列；分布变化；多变量时序
- 代码：类别 A，级别 L0；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：时间序列、分布变化、多变量时序。会议 ICLR 2024 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 3. SEMPO: Lightweight Foundation Models for Time Series Forecasting

- 会议：NeurIPS 2025（main）
- 关系：直接研究目标任务；时间序列；预测；时序基础模型
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：时间序列、预测、时序基础模型。会议 NeurIPS 2025 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 4. CANDI: Curated Test-Time Adaptation for Multivariate Time-Series Anomaly Detection Under Distribution Shift

- 会议：AAAI 2026（main）
- 关系：直接研究目标任务；时空；分布变化；多变量时序
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：时空、分布变化、多变量时序。会议 AAAI 2026 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 5. Tiny Time Mixers (TTMs): Fast Pre-trained Models for Enhanced Zero/Few-Shot Forecasting of Multivariate Time Series

- 会议：NeurIPS 2024（main）
- 关系：直接研究目标任务；时间序列；预测；多变量时序
- 代码：类别 A，级别 L1；许可证 apache license
- 理由：直接研究目标任务。命中：时间序列、预测、多变量时序。会议 NeurIPS 2024 main 轨道。
- 前置条件：静态已见入口/配置/依赖，未运行。大型数据、权重未下载；本轮未运行。

### 6. Deciphering Spatio-Temporal Graph Forecasting: A Causal Lens and Treatment

- 会议：NeurIPS 2023（main）
- 关系：直接研究目标任务；时空；时序图/点过程；预测
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：时空、时序图/点过程、预测。会议 NeurIPS 2023 main 轨道。
- 前置条件：配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 7. FourierGNN: Rethinking Multivariate Time Series Forecasting from a Pure Graph Perspective

- 会议：NeurIPS 2023（main）
- 关系：直接研究目标任务；时间序列；预测；多变量时序
- 代码：类别 A，级别 L0；许可证 mit license
- 理由：直接研究目标任务。命中：时间序列、预测、多变量时序。会议 NeurIPS 2023 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 8. Online Irregular Multivariate Time Series Forecasting via Uncertainty-Driven Dual-Expert Calibration

- 会议：KDD 2026（main）
- 关系：直接研究目标任务；时间序列；预测；多变量时序
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：时间序列、预测、多变量时序。会议 KDD 2026 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 9. Battling the Non-stationarity in Time Series Forecasting via Test-time Adaptation

- 会议：AAAI 2025（main）
- 关系：直接研究目标任务；时间序列；分布变化；预测
- 代码：类别 A，级别 L0；许可证 mit license
- 理由：直接研究目标任务。命中：时间序列、分布变化、预测。会议 AAAI 2025 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

### 10. Dish-TS: A General Paradigm for Alleviating Distribution Shift in Time Series Forecasting

- 会议：AAAI 2023（main）
- 关系：直接研究目标任务；时间序列；分布变化；预测
- 代码：类别 A，级别 L0；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：时间序列、分布变化、预测。会议 AAAI 2023 main 轨道。
- 前置条件：依赖声明; 配置（可能用 argparse）; 测试。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

用于空气质量/水文/能源等环境时序与时空预测的方法对照，以及可迁移的概率预测与分布漂移处理。

## 缺口

- 未运行训练或评测；缺数据、权重和硬件验证。
- 付费墙会议论文若无合法公开全文则未计入。
- 边界日期条目若精度只有年份，未计入或在窗口说明中标注。

续跑：`python3 -I scripts/run_en.py domain 02`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
