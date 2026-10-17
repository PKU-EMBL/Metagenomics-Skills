---
name: biobakery-databases
description: >
  Install and pin bioBakery reference databases for MetaPhlAn and HUMAnN (ChocoPhlAn
  markers, UniRef gene families, MetaCyc pathways, utility mapping). Use this skill
  when: (1) Downloading MetaPhlAn/HUMAnN databases, (2) Choosing UniRef90 vs UniRef50,
  (3) Aligning MetaPhlAn and HUMAnN DB versions, (4) Troubleshooting missing index
  paths. For Kraken indexes use kraken2. For eggNOG/CARD/GTDB use those skills.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, bioBakery, ChocoPhlAn, UniRef, MetaPhlAn, HUMAnN"
  metagenomics.upstream: "https://github.com/biobakery/biobakery"
---

# bioBakery databases (MetaPhlAn / HUMAnN)

Upstream: [MetaPhlAn](https://github.com/biobakery/MetaPhlAn) ·
[HUMAnN](https://github.com/biobakery/humann) ·
bioBakery: https://huttenhower.sph.harvard.edu/biobakery/

## Analytical thinking

MetaPhlAn and HUMAnN results are **database-version-dominated**. Changing
ChocoPhlAn or UniRef releases can move species/pathway tables more than tweaking
CLI flags.

Keep MetaPhlAn marker DB and HUMAnN nucleotide/protein DBs **compatible** for
the same study when you report both taxonomy and pathways. Record:
software version + DB names + install paths + download date.

UniRef90 vs UniRef50 is a sensitivity/specificity and disk trade-off — state it
explicitly; do not silently switch mid-cohort.

## Prerequisites

| DB | Used by | Notes |
|----|---------|-------|
| MetaPhlAn / ChocoPhlAn markers | `metaphlan` | Species-level marker genes |
| HUMAnN ChocoPhlAn | `humann` | Nucleotide mapping |
| UniRef90 or UniRef50 | `humann` | Translated search / gene families |
| Utility mapping + MetaCyc | `humann` | Pathway aggregation |

Disk: tens to hundreds of GB depending on UniRef choice.

## How to install (HUMAnN helpers)

```bash
# After humann is installed in the env:
mkdir -p db/humann
humann_databases --download chocophlan full db/humann
humann_databases --download uniref uniref90_diamond db/humann
humann_databases --download utility_mapping full db/humann

humann_config --update database_folders nucleotide db/humann/chocophlan
humann_config --update database_folders protein db/humann/uniref
humann_config --update database_folders utility_mapping db/humann/utility_mapping
```

Exact subcommand names can vary by HUMAnN version — verify with
`humann_databases --help` for your install.

## How to install (MetaPhlAn)

```bash
mkdir -p db/metaphlan
# Prefer the install/download path documented for your MetaPhlAn major version
# (metaphlan --install / download utilities). Example pattern:
metaphlan --install --bowtie2db db/metaphlan
```

Confirm the DB build string printed in MetaPhlAn logs and archive it.

## Decision tree

```text
Profiling DB need?
├─ Marker taxonomy only → MetaPhlAn DB (this skill) → metaphlan
├─ Pathways / gene families → HUMAnN DBs (this skill) → humann
├─ Custom / fast k-mer taxonomy → kraken2 indexes (not bioBakery)
└─ Genome taxonomy for MAGs → gtdb / gtdbtk
```

## Verify

```bash
metaphlan --version
humann --version
humann_config --print
ls db/metaphlan db/humann | head
```

## Related skills

`public-databases` · `metaphlan` · `humann` · `kraken2` · `setup`
