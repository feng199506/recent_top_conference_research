# 07 机器人、无人机与学习控制

检索日 2026-10-30。窗口 2021-10-30 至 2026-10-30，按正式会议发表日期判断。
本方向只收主会研究论文；AISTATS/UAI 等补充会议单独标注，不与 ICML/NeurIPS/ICLR/COLT 混称同一排名。

- 已下载并核验全文：**110** 篇（目标约 100，参考 90–120）
- 新下载 110，已有复用 0
- 有可获取代码（A/B/C）9 篇（8.2%）；官方完整实现（A）2 篇
- 本轮代码核验最高到 L1，**不**声称运行验证通过或已复现

## 年份

| 年份 | 篇数 |
|---|---|
| 2021 | 6 |
| 2022 | 12 |
| 2023 | 19 |
| 2024 | 27 |
| 2025 | 28 |
| 2026 | 18 |

## 会议与轨道

| 会议 | 年份 | 轨道计数 |
|---|---|---|
| CoRL | 2021 | 6 |
| CoRL | 2022 | 11 |
| CoRL | 2023 | 14 |
| CoRL | 2024 | 16 |
| CoRL | 2025 | 25 |
| L4DC | 2022 | 1 |
| L4DC | 2023 | 3 |
| L4DC | 2024 | 4 |
| L4DC | 2025 | 3 |
| L4DC | 2026 | 3 |
| RSS | 2023 | 2 |
| RSS | 2024 | 7 |
| RSS | 2026 | 15 |

轨道合计：
- main: 110

## 代码可用性

| 类别 | 含义 | 篇数 |
|---|---|---|
| A | 作者官方完整实现（静态） | 2 |
| B | 作者官方部分实现 | 0 |
| C | 仅第三方复现 | 7 |
| D | 无代码、空仓或未找到 | 101 |

筛选目标是每方向至少 70% 已下载论文有官方可获取代码。本方向实际 A+B 比例 1.8%（不把第三方算进官方代码，也不把目标写成已达成）。

## 优先阅读与复现（10 篇）

只根据与本方向的直接相关性和代码完整度排序，不是对方法优劣的判断。前置条件见代码列。

### 1. Sequence Modeling for Time-Optimal Quadrotor Trajectory Optimization with Sampling-based Robustness Analysis

- 会议：CoRL 2025（main）
- 关系：直接研究目标任务；无人机；轨迹
- 代码：类别 A，级别 L1；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：无人机、轨迹。会议 CoRL 2025 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 2. DATT: Deep Adaptive Trajectory Tracking for Quadrotor Control

- 会议：CoRL 2023（main）
- 关系：直接研究目标任务；无人机；轨迹
- 代码：类别 A，级别 L1；许可证 mit license
- 理由：直接研究目标任务。命中：无人机、轨迹。会议 CoRL 2023 main 轨道。
- 前置条件：配置（可能用 argparse）。大型数据、权重未下载；本轮未运行。

### 3. Sim-to-Real Reinforcement Learning for Vision-Based Dexterous Manipulation on Humanoids

- 会议：CoRL 2025（main）
- 关系：可迁移的基础方法；操作；仿真到真实；腿式/人形
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：操作、仿真到真实、腿式/人形。会议 CoRL 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 4. Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching

- 会议：RSS 2026（main）
- 关系：直接研究目标任务；机器人；操作；仿真到真实
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：机器人、操作、仿真到真实。会议 RSS 2026 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 5. Sampling-based System Identification with Active Exploration for Legged Sim2Real Learning

- 会议：CoRL 2025（main）
- 关系：可迁移的基础方法；仿真到真实；腿式/人形
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：仿真到真实、腿式/人形。会议 CoRL 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 6. i-Sim2Real: Reinforcement Learning of Robotic Policies in Tight Human-Robot Interaction Loops

- 会议：CoRL 2022（main）
- 关系：直接研究目标任务；学习控制；仿真到真实
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：学习控制、仿真到真实。会议 CoRL 2022 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 7. HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model

- 会议：RSS 2026（main）
- 关系：可迁移的基础方法；腿式/人形；世界模型
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：腿式/人形、世界模型。会议 RSS 2026 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 8. Advancing Humanoid Locomotion: Mastering Challenging Terrains with Denoising World Model Learning

- 会议：RSS 2024（main）
- 关系：可迁移的基础方法；腿式/人形；世界模型
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：腿式/人形、世界模型。会议 RSS 2024 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 9. Safe Exploration in Reinforcement Learning: Training Backup Control Barrier Functions with Zero Training-Time Safety Violations

- 会议：L4DC 2025（main）
- 关系：直接研究目标任务；学习控制；安全控制
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：直接研究目标任务。命中：学习控制、安全控制。会议 L4DC 2025 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

### 10. Efficient imitation learning with conservative world models

- 会议：L4DC 2024（main）
- 关系：可迁移的基础方法；模仿学习；世界模型
- 代码：类别 D，级别 无；许可证 未发现许可证（不标为可自由复用）
- 理由：可迁移的基础方法。命中：模仿学习、世界模型。会议 L4DC 2024 main 轨道。
- 前置条件：未在摘要/评论/PDF 首页发现代码链接；未声称已检索穷尽第三方复现。大型数据、权重未下载；本轮未运行。

## 对本任务的用途

用于无人机、操作机器人与学习控制（含 MPC/安全控制）的方法对照。

## 缺口

- ICRA/IROS/CDC/ACC 全文多在 IEEE 付费墙；本轮 arXiv API 在方向 7 检索时超时，未把无公开全文的论文计入。
- 主集合来自 RSS 开放proceedings、CoRL 与 L4DC 的 PMLR 主卷。RSS 2025 部分 PDF 为扫描件、无法提取文本，已替换。
- 未运行训练或评测；缺数据、权重和硬件验证。

续跑：`python3 -I scripts/run_en.py domain 07`（已完成项会跳过）。

生成时间 2026-10-30 01:41 UTC
