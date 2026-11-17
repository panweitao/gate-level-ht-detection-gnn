# Project wiki

## Start here

- `concepts/pipeline.md`: algorithm and code map
- `../docs/ARCHITECTURE.md`: serialized features and module boundaries
- `../docs/REPRODUCIBILITY.md`: exact environment and known gaps
- `../docs/WORKSPACE_AUDIT.md`: source-to-release selection record
- `../docs/VALIDATION.md`: repository and dataset validation evidence
- `devlog/2026-11.md`: append-only release log

## Engineering rules

- Do not commit raw benchmark data or generated result trees.
- Every reported number must identify its paper table or regenerated log.
- Algorithm changes require a separate plan and a numerical comparison against the preserved implementation.
- Publish only the latest code version; historical variants remain in the private research workspace.
