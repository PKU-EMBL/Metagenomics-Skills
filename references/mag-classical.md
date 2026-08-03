# Module E — Classical MAG recovery

Multi-binner MAG catalogues using MetaWRAP-style workflows, followed by
dereplication, abundance estimation, and GTDB taxonomy. For PKU-EMBL refined
multi-assembly recovery, use Module F ([basalt-cli.md](basalt-cli.md)).

## Depth guidance

- Typical MAG mining: ≥ ~6 Gb per sample.
- Complex soils: often ≥ ~30 Gb per sample.
- Under-sequenced demonstration sets rarely yield usable MAGs.

## Workflow

| Step | Default | Key parameters |
|---|---|---|
| Binning | MetaWRAP `binning` | `--metabat2 --maxbin2` (± CONCOCT; costly) |
| Refinement | MetaWRAP `bin_refinement` | `-c 50 -x 10` |
| Organization | mixed / single-sample / subgroup | keep provenance prefixes |
| Dereplication | dRep | species `-sa 0.95 -nc 0.30 -comp 50 -con 10`; strain `-sa 0.99` |
| QC refresh | CheckM2 | especially if quality screening was skipped in dRep |
| Abundance | CoverM `genome --coupled` | relative abundance table |
| Taxonomy | GTDB-Tk `classify_wf` | set `GTDBTK_DATA_PATH` |
| Phylogeny | GTDB-Tk `infer` + tree annotation | merge taxonomy, quality, abundance |

## Assembly modes

- **Mixed (co-assembly) binning:** one contig set + all related PE libraries.
- **Single-sample binning:** assemble and bin per sample when hardware or time
  preclude mixed runs; often retains sample-restricted populations.
- **Subgroup binning:** when samples > ~30 or data > ~300 Gb, partition by
  similar condition or site and process each subgroup separately.

## Minimal manual alternative

1. Map reads and compute contig depths.
2. Bin with MetaBAT 2 / SemiBin 2 / CONCOCT / MaxBin / VAMB.
3. Aggregate (e.g. DAS Tool) if combining manually; filter with CheckM2.

This alternative lacks MetaWRAP refinement automation and lacks BASALT
cross-assembly selection, contig screening, retrieval, and reassembly.

## Hand-off to Module F

When assemblies and paired-end (± long) reads are available and the scientific
goal is cross-assembly refined MAGs, prefer BASALT / BASALT-Air.
