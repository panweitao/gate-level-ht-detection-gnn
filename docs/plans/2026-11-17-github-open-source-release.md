# GitHub open-source release plan

Date: 2026-11-17

Goal: turn the 10.67 GiB research workspace into a compact, reviewable GitHub repository without altering the original evidence.

Decisions:

- D1: Create a separate release copy under an ASCII-only path. Selected because the source workspace is not a Git repository and contains large generated artifacts.
- D2: Exclude all raw/processed SAED, LEDA, and Trust-Hub benchmark data by default.
- D3: Publish only the latest experiment drivers; keep older branches in the original private workspace.
- D4: Use Apache-2.0 for code; approval has been confirmed by the relevant rights holders.
- D5: Do not commit, add a remote, or push during cleanup.
- D6: Publish the latest workspace code version only.
- D7: Do not repeat GPU training during repository cleanup because the paper results were reproduced previously.

Checklist:

- [x] Inventory source files and directory sizes.
- [x] Map the paper method to preprocessing, feature extraction, and training code.
- [x] Create the release repository and Git ignore rules.
- [x] Add README, architecture, dataset, reproduction, audit, and citation documentation.
- [x] Add prepared-data validation and dependency-light tests.
- [x] Confirm Apache-2.0 approval from relevant code rights holders.
- [x] Confirm datasets are excluded from the public repository by default.
- [x] Record that the paper results were reproduced previously; no cleanup-time retraining is required.
- [x] Update final publication metadata and DOI.
- [ ] Review, commit, create the GitHub repository, and push after explicit approval.
