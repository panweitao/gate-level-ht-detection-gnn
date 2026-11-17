"""Validate prepared .content/.cites benchmark pairs without importing DGL."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


FEATURE_COUNT = 24


@dataclass(frozen=True)
class DatasetStats:
    name: str
    nodes: int
    edges: int
    trojan_nodes: int


def validate_pair(content_path: Path, cites_path: Path) -> DatasetStats:
    node_ids: set[str] = set()
    trojan_nodes = 0

    with content_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            fields = line.split()
            if not fields:
                continue
            expected_fields = FEATURE_COUNT + 2
            if len(fields) != expected_fields:
                raise ValueError(
                    f"{content_path}:{line_number}: expected {expected_fields} fields "
                    f"(node + {FEATURE_COUNT} features + label), got {len(fields)}"
                )
            node_id, feature_fields, label = fields[0], fields[1:-1], fields[-1]
            if node_id in node_ids:
                raise ValueError(f"{content_path}:{line_number}: duplicate node id {node_id!r}")
            node_ids.add(node_id)
            try:
                [float(value) for value in feature_fields]
            except ValueError as exc:
                raise ValueError(f"{content_path}:{line_number}: non-numeric feature") from exc
            if label not in {"0", "1"}:
                raise ValueError(f"{content_path}:{line_number}: label must be 0 or 1, got {label!r}")
            trojan_nodes += label == "1"

    if not node_ids:
        raise ValueError(f"{content_path}: no nodes found")

    edge_count = 0
    with cites_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            fields = line.split()
            if not fields:
                continue
            if len(fields) != 2:
                raise ValueError(f"{cites_path}:{line_number}: expected two edge endpoints")
            missing = [node_id for node_id in fields if node_id not in node_ids]
            if missing:
                raise ValueError(
                    f"{cites_path}:{line_number}: edge references unknown node(s): {', '.join(missing)}"
                )
            edge_count += 1

    return DatasetStats(content_path.stem, len(node_ids), edge_count, trojan_nodes)


def discover_pairs(root: Path) -> list[tuple[Path, Path]]:
    if root.is_file():
        if root.suffix != ".content":
            raise ValueError("A file argument must have the .content suffix")
        content_files = [root]
    else:
        content_files = sorted(root.rglob("*.content"))

    if not content_files:
        raise ValueError(f"No .content files found below {root}")

    pairs: list[tuple[Path, Path]] = []
    for content_path in content_files:
        cites_path = content_path.with_suffix(".cites")
        if not cites_path.is_file():
            raise ValueError(f"Missing matching edge file: {cites_path}")
        pairs.append((content_path, cites_path))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="A .content file or a directory searched recursively")
    args = parser.parse_args()

    pairs = discover_pairs(args.path)
    total_nodes = total_edges = total_trojans = 0
    for content_path, cites_path in pairs:
        stats = validate_pair(content_path, cites_path)
        total_nodes += stats.nodes
        total_edges += stats.edges
        total_trojans += stats.trojan_nodes
        print(
            f"OK {stats.name}: nodes={stats.nodes}, edges={stats.edges}, "
            f"trojan_nodes={stats.trojan_nodes}"
        )

    print(
        f"Validated {len(pairs)} dataset(s): "
        f"nodes={total_nodes}, edges={total_edges}, trojan_nodes={total_trojans}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
