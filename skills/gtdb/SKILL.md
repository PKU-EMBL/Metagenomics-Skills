---
name: gtdb
description: >
  Use the Genome Taxonomy Database (GTDB) public releases — taxonomy tables, trees,
  metadata, and representative genomes. Use this skill when: (1) Choosing or citing a
  GTDB release, (2) Downloading bac120/ar53 taxonomy or reps, (3) Distinguishing GTDB
  data files from the GTDB-Tk runtime package, (4) Preparing reference sets for MAG
  comparison. For classifying your MAGs, use gtdbtk. For biome catalogues, use mgnify.
  For routing, use public-databases.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, GTDB, taxonomy, genomes"
  metagenomics.upstream: "https://gtdb.ecogenomic.org/"
  metagenomics.stage: "taxonomy"
---

# GTDB (Genome Taxonomy Database)

Portal: https://gtdb.ecogenomic.org/ ·
Downloads: https://gtdb.ecogenomic.org/downloads ·
Data: https://data.gtdb.ecogenomic.org/releases/ ·
Toolkit: [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk)

## Citation

Parks, D. H. *et al.* A complete domain-to-species taxonomy for Bacteria and Archaea. *Nat. Biotechnol.* **38**, 1079–1086 (2020). https://doi.org/10.1038/s41587-020-0501-8

Parks, D. H. *et al.* GTDB release 10: a complete and systematic taxonomy for 715 230 bacterial and 17 245 archaeal genomes. *Nucleic Acids Res.* **54**, D743–D754 (2026). https://doi.org/10.1093/nar/gkaf1040

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

GTDB provides a **rank-normalized prokaryotic taxonomy**. Your MAG labels from
binning are **not** taxonomy — GTDB assignment is a separate claim layer.

Distinguish three packages people confuse:

| Package | What it is | Typical use |
|---------|------------|-------------|
| GTDB release files (`bac120_taxonomy.tsv`, trees, metadata, genome reps) | Public taxonomy/genome release | Cite taxonomy; build custom refs |
| `GTDBTK_DATA_PATH` / `gtdbtk_data.tar.gz` | Runtime DB for GTDB-Tk | Classify genomes with `gtdbtk` |
| MGnify biome catalogues | Biome MAG catalogues (often GTDB-annotated) | Novelty / habitat context (`mgnify`) |

Always pin the **GTDB release ID** (e.g. R10-RS226 from `VERSION.txt` / release notes) next to GTDB-Tk software version.

## GTDB release 10 (R10-RS226) notes

From Parks *et al.* (*Nucleic Acids Res.* 2026):

- ~715k bacterial + ~17k archaeal genomes; ~137k bacterial / ~7k archaeal **species clusters**
- Major new deep lineages are rarer each release (diversity saturation signal), but **species discovery continues** (>95% species still ungenomed under their projections) — do not claim “GTDB is complete”
- Website / ANI methodology updates (e.g. skani in recent releases) — match GTDB-Tk data package to the release you cite
- Prefer `releases/<release>/` over assuming `latest/` stays frozen mid-study

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

For GTDB-Tk classification, install its complete release-coupled reference bundle—not an ad-hoc genome tarball—and apply the checks in `$gtdbtk`.

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

`gtdbtk` · `public-databases` · `mgnify` · `progenomes` · `cami` · `checkm2` · `drep` · `mag-qc` · `visualization`
