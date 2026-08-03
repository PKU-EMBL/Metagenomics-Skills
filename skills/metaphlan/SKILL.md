---
name: metaphlan
description: >
  Marker-gene taxonomic profiling of metagenomes. Use this skill when working with metaphlan: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/biobakery/MetaPhlAn. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'marker', 'profiling']
upstream: https://github.com/biobakery/MetaPhlAn
---

# MetaPhlAn

Upstream: [biobakery/MetaPhlAn](https://github.com/biobakery/MetaPhlAn)

## Analytical thinking

MetaPhlAn estimates clade abundances from **clade-specific marker genes**. It is
usually more specific than naive k-mer classification on host-depleted short
reads, but it cannot report taxa lacking markers in the database.

Do **not** average MetaPhlAn and Kraken tables. They answer different questions.

Often invoked inside HUMAnN; use this skill when you need MetaPhlAn outputs or
parameters explicitly.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Dehosted PE/SE FASTQ | From `kneaddata` |
| Database | MetaPhlAn DB matching software version | Pinned release |
| RAM | 16–32 GB | 64 GB |

## How to run

```bash
# typical bioconda / biobakery stack
metaphlan \
  temp/hr/${id}_1.fastq,temp/hr/${id}_2.fastq \
  --input_type fastq \
  --bowtie2out temp/metaphlan/${id}.bowtie2.bz2 \
  -o result/metaphlan/${id}_profile.txt \
  --nproc 8
```

Merge profiles across samples with MetaPhlAn utility scripts / HUMAnN join tools.

## Interpretation

| Output | Means | Does not mean |
|--------|-------|---------------|
| Relative abundance | Marker-supported composition | Absolute CFU/load |
| Unclassified | No markers hit | Community is empty |

## Decision tree

```text
Need marker-based species/clades?
├─ Yes → metaphlan (alone or via humann)
├─ Need pathways too → humann (includes MetaPhlAn step)
└─ Custom large DB / speed → kraken2 (+ bracken)
```

## Related skills

`humann` · `kraken2` · `visualization` · `tool-selection`

