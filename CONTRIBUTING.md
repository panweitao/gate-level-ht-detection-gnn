# Contributing

Issues and pull requests are welcome after the initial public release.

Before submitting a change:

1. Do not commit benchmark netlists, archives, generated result trees, model checkpoints, or files whose redistribution rights are unclear.
2. Keep algorithmic changes separate from formatting and repository-maintenance changes.
3. Run `python -m unittest discover -s tests -v` and `python -m compileall src tools tests`.
4. Document any change that can alter reported metrics, data splits, class weights, or feature order.
5. Include the dataset name, held-out netlist, random seed, framework versions, and GPU model with new numerical results.

The 24 feature dimensions and label convention are part of the public data contract. Changes to them require corresponding updates to `docs/ARCHITECTURE.md`, `docs/DATASETS.md`, and the validation tests.
