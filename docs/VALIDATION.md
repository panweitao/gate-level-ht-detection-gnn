# Validation evidence

Validation date: 2026-11-17

## Repository checks

- `python -m compileall -q src tools tests`: passed.
- `python -m unittest discover -s tests -v`: 3 tests passed.
- `CITATION.cff`: valid against Citation File Format schema 1.2.0.
- Markdown internal links: no missing targets.
- release tree excluding `.git` and caches: 39 files, approximately 216 KiB.
- Git ignore checks confirmed raw Verilog, prepared graph data, generated results, and checkpoints are excluded.
- secret/path scan found no credentials in release documentation or active code; historical absolute-path comments were removed from active sources.

## Prepared-data structural validation

The dependency-light validator checked field counts, numeric features, binary labels, unique node IDs, matching `.content/.cites` pairs, and valid edge endpoints against the original workspace.

| Group | Dataset pairs | Nodes | Edges | Trojan nodes | Result |
|---|---:|---:|---:|---:|---|
| SAED | 17 | 56,702 | 177,729 | 1,064 | PASS |
| LEDA | 80 | 221,634 | 529,180 | 1,854 | PASS |
| EthernetMAC10GE | 4 | 408,240 | 1,076,341 | 52 | PASS |

The LEDA total decomposes exactly into the paper-reported 95,070 normal + 280 Trojan combinational nodes and 124,710 normal + 1,574 Trojan sequential nodes. The four EthernetMAC10GE datasets contain 408,188 normal nodes and 52 Trojan nodes, also matching the paper.

## Validation scope

- This cleanup pass did not reinstall PyTorch 1.12.0/DGL 0.9.1 or repeat GPU training.
- Paper metrics had already been reproduced in the original research workflow.
- The public repository contains the latest workspace code and excludes benchmark datasets by policy.
