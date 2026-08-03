---
name: bwa-mem2
description: >
  Architecture-aware faster BWA-MEM for short-read mapping. Use this skill when working with bwa-mem2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/bwa-mem2/bwa-mem2. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'alignment', 'short-read']
upstream: https://github.com/bwa-mem2/bwa-mem2
stage: mapping
---

# BWA-MEM2

Upstream: [BWA-MEM2](https://github.com/bwa-mem2/bwa-mem2)

## Citation

Vasimuddin, M., Misra, S., Li, H. & Aluru, S. Efficient architecture-aware acceleration of BWA-MEM for multicore systems. *IEEE IPDPS* 314–324 (2019). https://doi.org/10.1109/IPDPS.2019.00041

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Drop-in faster MEM for large multi-sample coverage maps. Index format differs from classic BWA — do not mix indexes.

## How to run

```bash
conda install -c bioconda bwa-mem2  # if packaged; else follow upstream

bwa-mem2 index contigs.fa
bwa-mem2 mem -t 16 contigs.fa clean_1.fq.gz clean_2.fq.gz \
  | samtools sort -@ 8 -o temp/map/${id}.bam
```

## Key parameters

| index | `bwa-mem2 index` | Incompatible with `bwa index` |

## Decision notes

- Stage: **mapping** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

bwa · bowtie2 · samtools · `tool-selection` · `metagenomics-workflow`
