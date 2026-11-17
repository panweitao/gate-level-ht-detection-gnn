# Architecture

## End-to-end flow

```text
gate-level Verilog + benchmark metadata
                |
                v
src/preprocessing/netlist_normalize.py
  - remove comments and extra line breaks
  - emit one standard-cell instance per line
  - extract Trojan instance names
                |
                v
src/preprocessing/build_features.py
  - parse cell instances and ports
  - match producer/consumer nets
  - construct directed edges
  - compute 24 node features
  - emit .content and .cites
                |
                v
src/experiments/graphsage_experiments.py
or src/experiments/gcn_experiments.py
  - build a DGL graph
  - leave one netlist out for testing
  - optimize weighted cross entropy
  - write node-classification metrics
```

## Feature order

The `.content` feature columns are expected in this order:

```text
sdff, dff, mux, xnor, oai, oa, nand, nor, and, or,
buf, inv, ao, aoi, dec, hadd, fadd, xor, unknown,
in_degree, out_degree, harmonic, PI, PO
```

The paper describes the same 24 semantic features, although the prose lists PI/PO before harmonic centrality. The implementation order above is the authoritative serialized order in the released preprocessing code.

## Graph construction

Each standard-cell instance is a node. An edge `u -> v` is created when an output net driven by instance `u` is consumed by an input port of instance `v`. Training scripts construct a DGL graph from `.cites`; self loops are removed before message passing.

## Models

`GraphSAGE` stacks DGL `SAGEConv` layers and supports `mean`, `pool`, `lstm`, and `gcn` aggregation. The CLI defaults to 256 hidden units and the paper's three-layer setting. The output has two logits per node.

The GCN experiment driver is retained as a separate baseline. The repository publishes only the latest implementation from the research workspace; older experimental branches remain in the original private workspace.

## Class weighting

For a netlist with `N` nodes and `N_HT` Trojan nodes, the minority-class weight is computed as:

```text
weight_HT = k * N / N_HT
```

`k = 0` selects an unweighted loss. The paper reports `k = 0.3` for the best GraphSAGE SAED configuration. The GCN paper setting uses a smaller penalty scale.
