# Workspace audit

Audit date: 2026-11-17

## Original workspace

- 11,238 files
- approximately 10.67 GiB
- not previously initialized as a Git repository
- no README, license, dependency manifest, CI, or project wiki

Largest top-level groups included approximately 4.76 GiB of `result_LEDA1`, 1.87 GiB of `Dataset`, 1.01 GiB of `data_largenetlist`, and more than 2 GiB across SAED result variants. Most of this content is generated output, duplicate experiment branches, raw netlists, archives, figures, spreadsheets, and Office lock files.

## Release decision

A separate ASCII-only release directory was created instead of moving or deleting the research workspace. This preserves the original evidence while keeping the Git repository small and reviewable.

Included:

- final GraphSAGE and GCN experiment drivers;
- netlist normalization and 24-feature extraction scripts;
- only the latest preprocessing and experiment code;
- compact paper-reported metrics;
- data validators, documentation, citation metadata, and CI.

Excluded:

- raw SAED, LEDA, and large-netlist benchmark files;
- `.rar` archives and embedded benchmark PDFs;
- generated feature arrays, `.content`/`.cites` corpora, and model outputs;
- multi-gigabyte result trees;
- spreadsheets, Word documents, figures, caches, and Office lock files.
- historical code variants, which remain preserved in the original private workspace.

GitHub blocks ordinary Git objects larger than 100 MiB and recommends keeping repositories small. The source workspace is therefore unsuitable for direct upload even if individual files happen to remain below the hard object limit.

## Confirmed release decisions

1. Apache-2.0 has been approved by the relevant code rights holders.
2. SAED, LEDA, and Trust-Hub data are excluded from the public repository by default.
3. The final article is IEEE Transactions on Computers 74(5), 1470-1481 (2025), DOI `10.1109/TC.2025.3533085`.
4. The repository publishes the latest code version from the research workspace.
5. The paper results were reproduced previously; a new training run is not required for source publication.
