# Pipeline concept map

The detector treats every standard-cell instance as a graph node and every signal dependency as a directed edge. Feature extraction combines local gate type, local structure, distance to circuit boundaries, and global harmonic centrality. GraphSAGE or GCN then aggregates neighboring information and outputs a normal/Trojan label for each node.

The public interface between preprocessing and training is the `.content`/`.cites` pair. This boundary is intentionally simple so that the netlist parser, graph model, or framework can be replaced independently while preserving datasets and evaluation.
