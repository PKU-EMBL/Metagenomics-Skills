---
name: bwa-mem2
description: >
  Architecture-aware faster BWA-MEM for Illumina reads to contigs/genomes.
  Use when a BWA-MEM workflow is required but throughput must improve, or when
  migrating from classic bwa mem. Upstream: https://github.com/bwa-mem2/bwa-mem2.
  Index format is NOT compatible with classic bwa index.
license: MIT
category: analysis-tools
tags: [mapping, alignment, short-read, bwa]
upstream: https://github.com/bwa-mem2/bwa-mem2
stage: mapping
---

# BWA-MEM2

Upstream: [bwa-mem2/bwa-mem2](https://github.com/bwa-mem2/bwa-mem2)

## Citation

Vasimuddin, M., Misra, S., Li, H. & Aluru, S. Efficient architecture-aware
acceleration of BWA-MEM for multicore systems. *IEEE IPDPS* 314–324 (2019).
https://doi.org/10.1109/IPDPS.2019.00041

Classic algorithm context: Li, H. Aligning sequence reads, clone sequences and
assembly contigs with BWA-MEM. *arXiv* (2013).
https://doi.org/10.48550/arXiv.1303.3997

## Analytical thinking

BWA-MEM2 keeps the **MEM mapping model** familiar to BWA users while speeding
alignment on modern CPUs. Critical pitfall: **`bwa-mem2 index` ≠ `bwa index`** —
never point `bwa-mem2 mem` at a classic BWA index (or the reverse).

For new metagenome coverage projects, `strobealign` or `bowtie2` may be simpler;
choose BWA-MEM2 when SOPs/scripts already assume BWA-MEM flags and SAM fields.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Index | From `bwa-mem2 index` | Rebuild if upgrading major version |
| RAM | Index ~ reference size class | Large co-assemblies need big nodes |

## How to run

```bash
conda install -c bioconda bwa-mem2 samtools

bwa-mem2 index contigs.fa
bwa-mem2 mem -t 16 contigs.fa \
  temp/hr/${id}_1.fastq temp/hr/${id}_2.fastq \
  2> temp/map/${id}.bwa-mem2.log \
  | samtools sort -@ 8 -o temp/map/${id}.bam
samtools index temp/map/${id}.bam
```

## Key parameters

| Option | Guidance |
|--------|----------|
| `-t` | Threads |
| `-R` | Read group (`@RG`) when merging multi-lane BAMs |
| `-K` | Process chunk size; raise on huge inputs if supported |

## Decision tree

```text
Need BWA-MEM-like mapping?
├─ Legacy classic bwa only available → bwa
├─ Speed on modern CPUs → bwa-mem2
└─ Greenfield metagenome coverage → strobealign or bowtie2
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Index load errors | Rebuild with `bwa-mem2 index` |
| Divergent SM tags | Set `-R` consistently across lanes |
| Huge unsorted SAM | Stream to `samtools sort` (never dump SAM) |

## Related skills

`bwa` · `bowtie2` · `strobealign` · `samtools` · `coverm` · `metabat2`
