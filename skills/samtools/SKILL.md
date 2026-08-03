---
name: samtools
description: >
  SAM/BAM/CRAM processing for mapping outputs. Use this skill when working with samtools: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/samtools/samtools. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'bam', 'sam']
upstream: https://github.com/samtools/samtools
stage: mapping
---

# Samtools

Upstream: [Samtools](https://github.com/samtools/samtools)

## Citation

Danecek, P. *et al.* Twelve years of SAMtools and BCFtools. *GigaScience* **10**, giab008 (2021). https://doi.org/10.1093/gigascience/giab008

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Always sort+index BAMs before CoverM/MetaBAT depth. Prefer streaming `aligner | samtools sort` to avoid huge unsorted SAM on disk.

## How to run

```bash
conda install -c bioconda samtools  # if packaged; else follow upstream

samtools sort -@ 8 -o out.bam in.sam
samtools index out.bam
samtools flagstat out.bam
samtools coverage out.bam | head
```

## Key parameters

| `sort/index` | required | For random access |
| `flagstat` | QC | Mapping rate |

## Decision notes

- Stage: **mapping** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

bowtie2 · bwa · minimap2 · coverm · `tool-selection` · `metagenomics-workflow`
