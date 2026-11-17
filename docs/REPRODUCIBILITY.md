# Reproducibility

## Paper environment

- Python 3.8
- PyTorch 1.12.0 + CUDA 11.3
- DGL CUDA 11.3 build 0.9.1
- NetworkX 3.1
- scikit-learn 1.3.0
- NVIDIA GeForce RTX 2060

The release pins the historical stack because DGL and PyTorch graph APIs have changed. Porting to a current framework should be treated as a separate experiment and revalidated numerically.

## Paper model settings

GraphSAGE uses 24 input features, 256 hidden units, three GraphSAGE layers, ReLU, and a two-class output. The paper studies `mean`, `pool`, `lstm`, and `gcn` aggregators. GCN is described with hidden sizes `[128, 64]` and a two-class output.

## Changes made for this release

The cleaned experiment drivers preserve the training loops but add a real CLI, use the paper's 256-unit GraphSAGE default, create result directories automatically, place outputs under `results/`, and move class weights to the active tensor device instead of forcing CUDA.

The original experimental files remain preserved in the private research workspace. The public repository contains only the latest implementation.

The repository publishes the latest implementation from the original experiment workspace. The paper results were reproduced previously in the research workflow. CI is intentionally limited to repository integrity and prepared-data checks because datasets are not distributed and GPU training is not part of routine source validation.

## Known limitations

1. Raw SAED, LEDA, and EthernetMAC10GE benchmark data are intentionally excluded.
2. The repository contains the latest GCN implementation; older experimental variants are retained only in the private research workspace.
3. Random seeds are not consistently fixed in the original training pipeline, and `_split_data` uses a fresh NumPy permutation. Repeated runs can differ.
4. Evaluation is performed repeatedly during training on the held-out netlist in the historical code. This behavior is retained for result traceability but should be reviewed when designing a strictly isolated model-selection protocol.
5. The feature extractor uses NetworkX shortest-path and harmonic-centrality operations that can be expensive on million-gate netlists.

## Verification tiers

Tier 1, repository checks:

```bash
python -m unittest discover -s tests -v
python -m compileall src tools tests
```

Tier 2, data checks:

```bash
python tools/validate_prepared_data.py data/SAED/aftpro_netfeature
```

Tier 3, optional numerical rerun:

The paper results were reproduced previously. If a new environment or implementation is introduced, rerun leave-one-netlist-out experiments, archive the command line and package list, and compare per-netlist TPR/TNR/F1 with the paper rather than checking only the mean.
