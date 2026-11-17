# 基于 GNN 的门级硬件木马检测

本仓库是论文《Hardware Trojan Detection Methods for Gate-Level Netlists Based on Graph Neural Networks》的开源整理版，用于在 gate-level netlist 中进行节点级硬件木马定位。

论文正式发表于 IEEE Transactions on Computers，Vol. 74, No. 5，2025 年 5 月，pp. 1470–1481，DOI：[10.1109/TC.2025.3533085](https://doi.org/10.1109/TC.2025.3533085)。

## 算法流程

1. 规整 gate-level Verilog，并从 benchmark 说明文件中提取 Trojan node 标签。
2. 根据标准单元 output net 与下游 input net 的连接关系构建图。
3. 为每个节点生成 24 维特征：19 类标准单元 one-hot、fan-in、fan-out、到 PI/PO 的距离以及 harmonic centrality。
4. 使用 GraphSAGE（`mean`、`pool`、`lstm`、`gcn` aggregator）或 GCN 完成节点二分类。
5. 使用 class-weighted cross entropy 缓解 normal node 与 HT node 极端不平衡问题。

论文报告的代表性结果：SAED 上 GraphSAGE-LSTM 的平均 F1 为 90.95%；LEDA 组合型网表上 GraphSAGE-POOL 的 F1 为 92.17%；LEDA 时序型网表上 GraphSAGE-LSTM 的 F1 为 98.59%；约 10 万门 EthernetMAC10GE 网表上的 F1 为 85.24%。

## 快速开始

论文实验环境为 Python 3.8、PyTorch 1.12.0 + CUDA 11.3、DGL 0.9.1、NetworkX 3.1 和 scikit-learn 1.3.0。

```bash
conda env create -f environment.yml
conda activate gate-ht-gnn
```

数据集不随仓库分发。取得合法授权的数据后，按 [`docs/DATASETS.md`](docs/DATASETS.md) 放置并生成 `.content`/`.cites`：

```bash
python tools/validate_prepared_data.py data/SAED/aftpro_netfeature
python src/experiments/graphsage_experiments.py --dataset saed --aggregator-type lstm --penalty-scale 0.3 --gpu 0
```

完整目录说明、复现边界和已知差异见：

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/DATASETS.md`](docs/DATASETS.md)
- [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)
- [`docs/WORKSPACE_AUDIT.md`](docs/WORKSPACE_AUDIT.md)
- [`docs/VALIDATION.md`](docs/VALIDATION.md)

## 开源与数据策略

相关代码权利人已同意使用 Apache-2.0 开源。SAED、LEDA、Trust-Hub benchmark、论文 PDF、原始网表、压缩包、模型和完整实验日志默认不随仓库上传。仓库提交当前工作区的最新代码版本；论文结果此前已完成复现，本次开源整理不重复执行 GPU 训练。
