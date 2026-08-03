---
name: gtdb
description: >
  Use the Genome Taxonomy Database (GTDB) public releases — taxonomy tables,
  trees, metadata, and representative genomes. Use this skill when: (1) Choosing
  or citing a GTDB release, (2) Downloading bac120/ar53 taxonomy or reps,
  (3) Distinguishing GTDB data files from the GTDB-Tk runtime package,
  (4) Preparing reference sets for MAG comparison. Upstream:
  https://gtdb.ecogenomic.org/ and https://github.com/Ecogenomics/GTDBTk.
  For classifying your MAGs, use gtdbtk. For biome catalogues, use mgnify.
  For routing, use public-databases.
license: MIT
category: utilities
tags: [database, GTDB, taxonomy, genomes]
upstream: https://gtdb.ecogenomic.org/
---

# GTDB (Genome Taxonomy Database)

Portal: https://gtdb.ecogenomic.org/ ·
Downloads: https://gtdb.ecogenomic.org/downloads ·
Data: https://data.gtdb.ecogenomic.org/releases/ ·
Toolkit: [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk)

## Citation

Parks, D. H. *et al.* A complete domain-to-species taxonomy for Bacteria and Archaea. *Nat. Biotechnol.* **38**, 1079–1086 (2020). https://doi.org/10.1038/s41587-020-0501-8

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

GTDB provides a **rank-normalized prokaryotic taxonomy**. Your MAG labels from
binning are **not** taxonomy — GTDB assignment is a separate claim layer.

Distinguish three packages people confuse:

| Package | What it is | Typical use |
|---------|------------|-------------|
| GTDB release files (`bac120_taxonomy.tsv`, trees, metadata, genome reps) | Public taxonomy/genome release | Cite taxonomy; build custom refs |
| `GTDBTK_DATA_PATH` / `gtdbtk_data.tar.gz` | Runtime DB for GTDB-Tk | Classify genomes with `gtdbtk` |
| MGnify biome catalogues | Biome MAG catalogues (often GTDB-annotated) | Novelty / habitat context (`mgnify`) |

Always pin the **GTDB release ID** (e.g. from `VERSION.txt` / release notes) next
to GTDB-Tk software version.

## Prerequisites

| Need | Resource |
|------|----------|
| Taxonomy tables / trees | `https://data.gtdb.ecogenomic.org/releases/latest/` |
| Representative genomes | `genomic_files_reps/` (very large) |
| Classify MAGs | GTDB-Tk data package → `gtdbtk` skill |

## How to fetch release metadata

```bash
mkdir -p db/gtdb && cd db/gtdb
wget -c https://data.gtdb.ecogenomic.org/releases/latest/VERSION.txt
wget -c https://data.gtdb.ecogenomic.org/releases/latest/RELEASE_NOTES.txt
wget -c https://data.gtdb.ecogenomic.org/releases/latest/bac120_taxonomy.tsv.gz
wget -c https://data.gtdb.ecogenomic.org/releases/latest/ar53_taxonomy.tsv.gz
# Mirror choice: see https://gtdb.ecogenomic.org/downloads for regional mirrors
```

For GTDB-Tk classification DB, follow the official GTDB-Tk data install docs
(not ad-hoc genome tarballs) — see `gtdbtk` skill.

## Key files (thinking)

| File | Use |
|------|-----|
| `bac120_taxonomy.tsv` / `ar53_taxonomy.tsv` | Map genome → GTDB lineage |
| `*_metadata.tsv.gz` | Quality / NCBI cross-refs / stats |
| `bac120.tree` / `ar53.tree` | Reference phylogeny |
| `genomic_files_reps/` | Species-rep FASTA/proteins (huge) |

## Decision tree

```text
GTDB-related task?
├─ Classify my MAGs → gtdbtk (needs GTDB-Tk data package)
├─ Cite / parse taxonomy release tables → gtdb (this skill)
├─ Compare to human-gut species catalogue → mgnify (UHGG) ± gtdb labels
└─ Read-based species tables only → metaphlan / kraken2 (not GTDB placement)
```

## Related skills

`gtdbtk` · `public-databases` · `mgnify` · `checkm2` · `drep` · `mag-qc` · `visualization`
