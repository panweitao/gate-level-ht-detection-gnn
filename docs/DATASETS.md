# Datasets

## Distribution policy

This code release intentionally excludes raw and processed SAED, LEDA, and Trust-Hub benchmark data. Users should obtain benchmark files from the original providers. Generated result trees and local model artifacts are also excluded from Git.

Trust-Hub: <https://www.trust-hub.org/>

## Expected directory layout

```text
data/
|-- SAED/
|   |-- initial_netlist/<benchmark>/
|   |-- aftprocess_netlist/<benchmark>/
|   `-- aftpro_netfeature/<benchmark>/
|       |-- <benchmark>.content
|       `-- <benchmark>.cites
|-- LEDA/
|   |-- initial_netlist/{com,seq}/<benchmark>/
|   |-- aftprocess_netlist/{com,seq}/<benchmark>/
|   `-- aftpro_netfeature/{com,seq}/<benchmark>/
|       |-- <benchmark>.content
|       `-- <benchmark>.cites
`-- large_netlist/
    |-- initial_netlist/<benchmark>/
    |-- aftprocess_netlist/<benchmark>/
    `-- aftpro_netfeature/<benchmark>/
        |-- <benchmark>.content
        `-- <benchmark>.cites
```

## Prepared formats

`.content` uses whitespace-separated fields:

```text
node_id f01 f02 ... f24 label
```

- `node_id` must be unique within one benchmark.
- Exactly 24 numeric feature values are required.
- `label` must be `0` for a normal node or `1` for a Trojan node.

`.cites` contains two node identifiers per line:

```text
source_node_id destination_node_id
```

Every endpoint must appear in the corresponding `.content` file.

## Validation

Validate a single benchmark directory:

```bash
python tools/validate_prepared_data.py data/SAED/aftpro_netfeature/RS232-T1000
```

Validate all benchmark directories recursively:

```bash
python tools/validate_prepared_data.py data/SAED/aftpro_netfeature
```

## Paper dataset counts

- LEDA combinational set: 95,070 normal nodes and 280 Trojan nodes across 40 netlists.
- LEDA sequential set: 124,710 normal nodes and 1,574 Trojan nodes across 40 netlists.
- EthernetMAC10GE evaluation: four netlists, each with 102,047 normal nodes and 13 Trojan nodes.

These counts are paper-reported reference values and should be checked against locally prepared data.
