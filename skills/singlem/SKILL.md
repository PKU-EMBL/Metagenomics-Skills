---
name: singlem
description: >
  SingleM — species-level metagenome profiling from conserved windows in
  universal marker genes, including lineages without genomic representation;
  Sandpiper aggregates public SingleM profiles. Use when: (1) Profiling
  environmental communities rich in unknowns, (2) Feeding Bin Chicken
  coassembly targeting, (3) GTDB-linked marker OTUs from short reads,
  (4) Comparing to MetaPhlAn/mOTUs/sylph. Upstream:
  https://github.com/wwood/singlem. Sandpiper: https://sandpiper.qut.edu.au.
license: MIT
category: analysis-tools
tags: [SingleM, taxonomy, markers, Sandpiper, low-abundance]
upstream: https://github.com/wwood/singlem
stage: taxonomy
---

# SingleM (+ Sandpiper)

Upstream: [wwood/singlem](https://github.com/wwood/singlem) ·
Sandpiper: https://sandpiper.qut.edu.au

## Citation

Woodcroft, B. J. *et al.* Comprehensive taxonomic identification of microbial
species in metagenomic data using SingleM and Sandpiper. *Nat. Biotechnol.*
(2025). https://doi.org/10.1038/s41587-025-02738-1

See also [docs/references.md](../../docs/references.md).

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
# verify subcommands for your SingleM version
singlem pipe -1 clean_1.fq.gz -2 clean_2.fq.gz -o temp/singlem/${id} --threads 16
# singlem summarise / microbial_fraction etc. per upstream docs
```

Pin SingleM metapackage / GTDB-linked DB version in Methods.

## Decision tree

```text
Taxonomic profiling need?
├─ Environment with many unknowns → singlem
├─ Targeted coassembly of rare lineages → singlem → binchicken
├─ Named SGB marker packs / pathways → metaphlan (± humann)
├─ Sketch containment vs genomes → sylph
└─ MAG taxonomy → gtdbtk
```

## Related skills

`binchicken` · `metaphlan` · `motus` · `sylph` · `gtdb` · `study-design` ·
`tool-selection`
