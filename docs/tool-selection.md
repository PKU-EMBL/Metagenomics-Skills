# Tool selection

Guidance mirrored by the `tool-selection` skill.

## Deliverable router

| Deliverable | Primary skill |
|-------------|---------------|
| QC + host-depleted reads | `preprocessing` |
| Taxonomic/functional tables from reads | `read-based` |
| Non-redundant gene catalogue | `gene-catalogue` |
| Classical MAG catalogue | `mag-classical` |
| Refined multi-assembly MAGs | `basalt` |
| Filters / Methods QC language | `mag-qc` |
| Figures | `visualization` |
| Full project plan | `metagenomics-workflow` |

## Classical MAG vs BASALT

| Situation | Prefer |
|-----------|--------|
| MetaWRAP → dRep → CoverM → GTDB baseline | `mag-classical` |
| Cross-assembly refinement + contig retrieval/reassembly | `basalt` |
| Absolute paths / separate work+output dirs | BASALT-Air via `basalt` |
| Resume existing Conda checkpoints | Conda BASALT via `basalt` |

## Profiling method choice

| Need | Prefer |
|------|--------|
| Marker clades | MetaPhlAn4 |
| Pathways / gene families | HUMAnN4 |
| Custom k-mer DB / speed | Kraken2 + Bracken |

Never merge profiler outputs into one unlabeled abundance table.
