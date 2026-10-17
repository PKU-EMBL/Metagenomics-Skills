---
name: singlem
description: >
  SingleM — species-level metagenome profiling from conserved windows in universal
  marker genes, including lineages without genomic representation; Sandpiper aggregates
  public SingleM profiles. Use when: (1) Profiling environmental communities rich in
  unknowns, (2) Feeding Bin Chicken coassembly targeting, (3) GTDB-linked marker OTUs
  from short reads, (4) Comparing to MetaPhlAn/mOTUs/sylph.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "SingleM, taxonomy, markers, Sandpiper, low-abundance"
  metagenomics.upstream: "https://github.com/wwood/singlem"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.21.4"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against current pipe documentation; not executed here"
---

# SingleM (+ Sandpiper)

Upstream: [wwood/singlem](https://github.com/wwood/singlem) ·
Sandpiper: https://sandpiper.qut.edu.au

## Citation

Woodcroft, B. J. *et al.* Comprehensive taxonomic identification of microbial
species in metagenomic data using SingleM and Sandpiper. *Nat. Biotechnol.*
(2025). https://doi.org/10.1038/s41587-025-02738-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Most profilers under-count **species without reference genomes**. SingleM
recruits reads covering short conserved windows in universal markers (AA-aware
via DIAMOND), clusters 60-bp windows into OTUs, then assigns taxonomy with
GTDB-oriented alignment (`smafa`). Unknown species can dominate environmental
communities in SingleM/Sandpiper analyses — state that as a profiling result,
not as MAG recovery.

| Tool | Role |
|------|------|
| `singlem` | Profile your metagenomes (incl. novel lineages) |
| `binchicken` | Uses SingleM-style marker sharing to plan coassemblies |
| `metaphlan` / `motus` | Marker packs / SCGs — complementary, different unknown handling |
| Sandpiper | Browse 248k+ public SingleM profiles |

## How to run

```bash
set -euo pipefail
command -v singlem >/dev/null
singlem --version
mkdir -p temp/singlem
[[ -s clean_1.fq.gz && -s clean_2.fq.gz ]] || exit 2
singlem pipe -1 clean_1.fq.gz -2 clean_2.fq.gz \
  --otu-table "temp/singlem/${id}.otu_table.csv" \
  --taxonomic-profile "temp/singlem/${id}.profile.tsv" --threads 16 \
  >"temp/singlem/${id}.stdout.log" 2>"temp/singlem/${id}.stderr.log"
```

This contract targets SingleM 0.21.4; run `singlem pipe --help` as the installed-version preflight. Pin the SingleM metapackage/GTDB-linked database version in Methods.

## Decision tree

```text
Taxonomic profiling need?
├─ Environment with many unknowns → singlem
├─ Targeted coassembly of rare lineages → singlem → binchicken
├─ Named SGB marker packs / pathways → metaphlan (± humann)
├─ Sketch containment vs genomes → sylph
└─ MAG taxonomy → gtdbtk
```

## Validation, recovery, and provenance

Require a non-empty OTU table or an explicit zero-hit result with completed logs. Validate sample labels, marker-package/window columns, non-negative coverage/read counts, taxonomy fields, and expected paired-input accounting; summarize across samples only after schemas and metapackages match. Inspect microbial fraction and novel/unassigned lineages rather than dropping them as missing data.

Record SingleM/dependency versions, complete command, metapackage and GTDB release/checksum, read checksums, output checksum, and any `summarise`/filter command. Rerun in a clean prefix when changing package or inputs. Marker OTUs support taxonomic profiles, not recovered genomes, viability, or cultured species identity.

## Related skills

`binchicken` · `metaphlan` · `motus` · `sylph` · `gtdb` · `study-design` ·
`tool-selection`
