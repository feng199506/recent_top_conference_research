"""Relevance scoring. Title+abstract only; not used as a sole inclusion rule.
A paper is kept only if the score and a short written reason both support it.
"""
import re

def _rx(words):
    return [(re.compile(p, re.I), w, pts) for p, w, pts in words]


# Domain 1: Gaussian processes, probabilistic ML, uncertainty.
D01_POS = _rx([
    (r"gaussian processes?", "高斯过程", 6),
    (r"\bgps?\b.{0,20}(regression|classif|posterior|prior|kernel|inducing|variational|sparse)", "GP 方法", 5),
    (r"deep gaussian process", "深度高斯过程", 6),
    (r"neural processes?", "Neural Process", 5),
    (r"convolutional neural process", "卷积 Neural Process", 6),
    (r"bayesian neural", "贝叶斯神经网络", 5),
    (r"bayesian deep learning", "贝叶斯深度学习", 5),
    (r"conformal (prediction|inference|risk)", "共形预测", 6),
    (r"conformaliz", "共形化", 5),
    (r"uncertainty quantification", "不确定性量化", 5),
    (r"predictive uncertainty", "预测不确定性", 5),
    (r"epistemic uncertainty", "认知不确定性", 5),
    (r"aleatoric", "偶然不确定性", 4),
    (r"evidential (deep|learning|regression|classif)", "证据深度学习", 5),
    (r"posterior network", "后验网络", 5),
    (r"laplace (approximation|redux|ggn)", "Laplace 近似", 5),
    (r"last[- ]layer laplace", "末层 Laplace", 6),
    (r"pac[- ]bayes", "PAC-Bayes", 5),
    (r"deep kernel", "深度核", 4),
    (r"inducing (points?|variables?)", "诱导点", 4),
    (r"variational gaussian process", "变分 GP", 6),
    (r"sparse (variational )?gaussian", "稀疏 GP", 6),
    (r"student-?t process", "Student-t 过程", 5),
    (r"gplvm", "GPLVM", 5),
    (r"nngp|neural network gaussian process", "NNGP", 5),
    (r"prior-data fitted|tabpfn|\bpfn[s]?\b", "PFN/TabPFN", 5),
    (r"function[- ]space (variational|inference)", "函数空间推断", 5),
    (r"stein variational", "Stein 变分", 4),
    (r"stochastic gradient langevin|\bsgld\b", "SGLD", 4),
    (r"hamiltonian monte carlo|\bhmc\b|no-?u-?turn", "HMC/NUTS", 4),
    (r"(confidence|model|probability) calibration", "概率校准", 4),
    (r"temperature scaling", "温度缩放", 4),
    (r"expected calibration error|\bece\b", "ECE", 3),
    (r"deep ensembles?", "深度集成", 3),
    (r"gpytorch|gpflow", "GP 软件方法", 5),
    (r"iterative gaussian process", "迭代 GP", 6),
    (r"computation-aware gaussian", "计算感知 GP", 6),
    (r"vecchia", "Vecchia", 4),
    (r"kriging", "Kriging", 4),
    (r"mat[eé]rn", "Matérn", 3),
    (r"spectral mixture", "谱混合核", 4),
    (r"random fourier features?", "随机傅里叶特征", 3),
    (r"bayesian optimisation|bayesian optimization", "贝叶斯优化", 4),
    (r"gaussian process bandit", "GP bandit", 5),
    (r"distribution-free (uncertainty|inference|prediction)", "无分布推断", 4),
    (r"jackknife\+|cv\+", "Jackknife+/CV+", 4),
    (r"selective (classification|prediction)", "选择性预测", 3),
    (r"uncertainty estimat", "不确定性估计", 4),
    (r"uncertainty-aware", "不确定性感知", 3),
    (r"predictive distribution", "预测分布", 3),
    (r"posterior predictive", "后验预测", 4),
    (r"multi-?output gaussian", "多输出 GP", 6),
    (r"coregionalization", "协同区域化", 4),
    (r"pathwise condition", "路径条件", 5),
    (r"variational inference", "变分推断", 2),
    (r"marginal likelihood", "边际似然", 3),
    (r"bayesian model selection", "贝叶斯模型选择", 4),
    (r"linearized laplace", "线性化 Laplace", 5),
    (r"spectral-normalized neural gaussian|\bsngp\b", "SNGP", 5),
    (r"deterministic uncertainty", "确定性不确定性", 4),
    (r"dirichlet prior network|prior networks?", "先验网络", 4),
    (r"expectation propagation", "期望传播", 3),
    (r"heteroscedastic", "异方差", 2),
    (r"in-context.{0,30}bayesian|transformers can do bayesian", "上下文贝叶斯推断", 5),
    (r"probabilistic (machine learning|forecast|prediction|model)", "概率机器学习", 3),
    (r"well-calibrated", "校准", 2),
    (r"out-of-distribution.{0,20}(uncert|detect)", "OOD 不确定性", 3),
    (r"kernel (ridge|method|learning)", "核方法", 2),
    (r"variational bayes", "变分贝叶斯", 3),
    (r"bayesian inference", "贝叶斯推断", 2),
    (r"gaussian copula process", "高斯 copula 过程", 5),
    (r"sparse spectrum", "稀疏谱", 3),
    (r"whitened (gp|gaussian)", "whitened GP", 4),
    (r"hilbert[- ]space.{0,20}(gp|gaussian)", "Hilbert 空间 GP", 5),
    (r"state[- ]space.{0,20}gaussian process", "状态空间 GP", 5),
    (r"natural gradient.{0,20}variational", "自然梯度变分", 3),
    (r"assumed density", "假设密度滤波", 3),
    (r"swag\b", "SWAG", 4),
    (r"subnetwork inference", "子网络推断", 4),
    (r"energy score|continuous ranked probability|\bcrps\b", "概率评分", 3),
    (r"proper scoring", "真评分规则", 3),
])

D01_NEG = _rx([
    (r"workshop", "workshop", -8),
    (r"tiny paper|tiny papers", "短论文轨道", -8),
    (r"findings of", "Findings", -8),
    (r"demonstration|demo paper", "Demo", -6),
    (r"competition (track|report)", "竞赛报告", -8),
    (r"under review|submitted to", "未录用投稿", -10),
    (r"withdraw", "撤稿", -8),
    (r"gaussian splatting|3d gaussian", "3D Gaussian Splatting（非 GP）", -8),
    (r"gaussian noise|additive gaussian", "仅高斯噪声", -2),
])

# Domain 2: time series, spatiotemporal, environment.
D02_POS = _rx([
    (r"time series", "时间序列", 5),
    (r"spatio-?temporal|spatial-temporal", "时空", 5),
    (r"probabilistic forecast", "概率预测", 6),
    (r"distribution (shift|change|drift)|concept drift", "分布变化", 5),
    (r"air quality", "空气质量", 6),
    (r"water quality", "水质", 6),
    (r"hydrolog", "水文", 5),
    (r"energy (forecast|load|price|demand)", "能源预测", 5),
    (r"nowcast", "临近预报", 4),
    (r"weather forecast|precipitation|wind power|solar power", "气象/能源", 4),
    (r"traffic (forecast|flow|prediction)", "交通预测", 4),
    (r"temporal (graph|point process)", "时序图/点过程", 4),
    (r"forecasting", "预测", 3),
    (r"multivariate time", "多变量时序", 4),
    (r"irregular (time|sampled)", "不规则采样", 4),
    (r"neural (ode|cde|sde)", "神经微分方程", 3),
    (r"state space model|kalman", "状态空间", 3),
    (r"conformal.{0,20}time series", "时序共形", 5),
    (r"diffusion.{0,20}(time series|forecast)", "扩散时序", 4),
    (r"foundation model.{0,20}(time series|forecast)", "时序基础模型", 5),
    (r"climate", "气候", 3),
    (r"remote sensing", "遥感", 3),
    (r"pm2\.5|pm10|no2|o3 concentration", "大气污染物", 5),
])
D02_NEG = _rx([
    (r"workshop", "workshop", -8),
    (r"language model.{0,20}time", "仅 LLM 时间提及", -2),
    (r"gaussian splatting", "3DGS", -6),
])

# Domain 3: industrial process monitoring.
D03_POS = _rx([
    (r"soft sensor", "软测量", 6),
    (r"process (monitoring|control|industry|fault)", "过程监控", 5),
    (r"fault (detection|diagnosis|prognos)", "故障检测诊断", 5),
    (r"root cause", "根因", 5),
    (r"anomaly detection", "异常检测", 4),
    (r"industrial (process|time series|control|plant)", "工业过程", 5),
    (r"multivariate (process|statistical process)", "多变量过程", 4),
    (r"tennessee eastman|\btep\b", "TE 过程", 6),
    (r"predictive maintenance", "预测性维护", 4),
    (r"remaining useful life|\brul\b", "剩余寿命", 4),
    (r"quality prediction", "质量预测", 4),
    (r"batch process", "批次过程", 4),
    (r"digital twin", "数字孪生", 3),
    (r"sensor (fusion|drift|fault)", "传感器", 3),
    (r"chemical process|petrochemical|steel|semiconductor manufacturing", "过程工业", 4),
    (r"incipient fault", "早期故障", 5),
    (r"alarm flood", "报警", 4),
    (r"condition monitoring", "状态监控", 4),
])
D03_NEG = _rx([
    (r"workshop", "workshop", -8),
    (r"intrusion detection|cyber[- ]attack", "网络安全（非过程监控）", -3),
    (r"video anomal", "视频异常", -3),
    (r"medical anomal|chest x-ray", "医学影像异常", -4),
])

# Domain 4: LLM + multimodal.
D04_POS = _rx([
    (r"large language model|\bllms?\b", "大语言模型", 4),
    (r"pretrain|pre-train", "预训练", 3),
    (r"instruction tun|alignment|rlhf|dpo\b|ppo\b", "对齐", 4),
    (r"retrieval-augmented|\brag\b", "RAG", 5),
    (r"tool (use|calling|learning)|function calling", "工具使用", 4),
    (r"multimodal|vision-language|vlm\b", "多模态", 4),
    (r"in-context learning", "上下文学习", 4),
    (r"chain-of-thought|reasoning", "推理", 3),
    (r"mixture of experts|\bmoe\b", "MoE", 3),
    (r"tokenizer|tokenization", "分词", 3),
    (r"multilingual", "多语言", 4),
    (r"evaluation|benchmark", "评测", 2),
    (r"preference (optimization|tuning)", "偏好优化", 4),
    (r"constitutional ai|self-instruct", "对齐数据", 4),
    (r"diffusion transformer|latent diffusion", "扩散多模态", 3),
    (r"visual question|image caption|text-to-image", "视觉语言", 3),
])
D04_NEG = _rx([
    (r"workshop", "workshop", -8),
    (r"findings of", "Findings", -8),
    (r"tiny paper", "短论文", -8),
])

# Domain 5: coding / software agents.
D05_POS = _rx([
    (r"code generation|program synthesis|code llm", "代码生成", 6),
    (r"software (agent|engineering|testing|repair)", "软件工程/智能体", 5),
    (r"program repair|bug (fix|detection|localization)", "程序修复", 5),
    (r"github copilot|coding assistant", "编码助手", 5),
    (r"agent(ic)? (software|coding|programming)", "编码智能体", 6),
    (r"unit test generation|test generation", "测试生成", 5),
    (r"static analysis", "静态分析", 4),
    (r"vulnerability detection", "漏洞检测", 4),
    (r"code search|code retrieval", "代码检索", 4),
    (r"repository[- ]level", "仓库级", 4),
    (r"swe-bench|humaneval|mbpp", "代码评测", 5),
    (r"compiler|program analysis", "程序分析", 3),
    (r"issue resol", "issue 解决", 4),
    (r"multi-agent.{0,20}(software|code)", "多软件智能体", 4),
])
D05_NEG = _rx([
    (r"workshop", "workshop", -8),
    (r"findings of", "Findings", -8),
])

# Domain 6: systems.
D06_POS = _rx([
    (r"inference (serving|engine|system|optim)", "推理系统", 5),
    (r"training (system|framework|parallel)", "训练系统", 5),
    (r"gpu (cluster|scheduling|kernel)", "GPU 系统", 4),
    (r"distributed (training|serving)", "分布式", 4),
    (r"kv cache|pagedattention|vllm", "KV/推理引擎", 6),
    (r"compiler.{0,20}(ml|tensor|tpu|gpu)", "ML 编译", 4),
    (r"parameter server|allreduce|collective", "通信", 4),
    (r"spot instance|cluster schedul", "集群调度", 4),
    (r"quantization.{0,20}(inference|serving)", "量化推理", 4),
    (r"memory (management|offload).{0,20}(train|infer)", "显存管理", 4),
    (r"pipeline parallel|tensor parallel|fsdp|zero-?offload", "并行训练", 5),
    (r"datacenter|production.{0,20}ml", "生产系统", 3),
    (r"mlsys|machine learning system", "ML 系统", 4),
])
D06_NEG = _rx([
    (r"workshop", "workshop", -8),
])

# Domain 7: robotics / UAV / learning control.
D07_POS = _rx([
    (r"quadrotor|quadcopter|uav\b|unmanned aerial|drone", "无人机", 6),
    (r"robot (learning|control|manipul|navigat)", "机器人", 5),
    (r"reinforcement learning.{0,20}(control|robot)", "学习控制", 4),
    (r"model predictive control|\bmpc\b", "MPC", 4),
    (r"learning[- ]based control", "学习控制", 5),
    (r"imitation learning", "模仿学习", 4),
    (r"visuomotor|manipulation", "操作", 3),
    (r"sim-to-real|sim2real", "仿真到真实", 4),
    (r"legged|humanoid", "腿式/人形", 4),
    (r"trajectory (optimization|tracking)", "轨迹", 3),
    (r"safe control|control barrier", "安全控制", 4),
    (r"gaussian process.{0,20}control|gp-mpc", "GP 控制", 5),
    (r"world model", "世界模型", 3),
    (r"policy (search|gradient).{0,20}(control|robot)", "策略控制", 3),
])
D07_NEG = _rx([
    (r"workshop", "workshop", -8),
])

DOMAIN_RULES = {
    "01": (D01_POS, D01_NEG, 5, "高斯过程/概率ML/不确定性"),
    "02": (D02_POS, D02_NEG, 5, "时间序列/时空/环境"),
    "03": (D03_POS, D03_NEG, 5, "工业过程监控"),
    "04": (D04_POS, D04_NEG, 5, "LLM/多模态"),
    "05": (D05_POS, D05_NEG, 5, "编码与软件智能体"),
    "06": (D06_POS, D06_NEG, 5, "训练推理系统"),
    "07": (D07_POS, D07_NEG, 5, "机器人无人机控制"),
}


def score_text(cat, title, abstract=""):
    pos, neg, thresh, _ = DOMAIN_RULES[cat]
    blob = f"{title or ''}\n{abstract or ''}"
    score = 0
    hits = []
    for rx, lab, pts in pos:
        if rx.search(blob):
            score += pts
            hits.append(lab)
    pens = []
    for rx, lab, pts in neg:
        if rx.search(blob):
            score += pts
            pens.append(lab)
    hits = list(dict.fromkeys(hits))
    pens = list(dict.fromkeys(pens))
    return score, thresh, hits, pens


def relation_label(hits):
    """Map hit labels to 直接 / 可迁移 / 支撑."""
    direct = {"高斯过程", "GP 方法", "深度高斯过程", "变分 GP", "稀疏 GP", "多输出 GP",
              "共形预测", "不确定性量化", "贝叶斯神经网络", "贝叶斯深度学习",
              "软测量", "过程监控", "故障检测诊断", "根因", "时间序列", "时空",
              "空气质量", "水质", "水文", "概率预测", "大语言模型", "多模态", "RAG",
              "代码生成", "编码智能体", "软件工程/智能体", "推理系统", "训练系统",
              "无人机", "机器人", "学习控制", "GP 控制", "Neural Process", "PFN/TabPFN"}
    support = {"GP 软件方法", "评测", "代码评测", "概率评分", "ECE", "温度缩放"}
    if any(h in direct for h in hits):
        return "直接研究目标任务"
    if any(h in support for h in hits):
        return "训练、评测或部署支撑"
    return "可迁移的基础方法"
