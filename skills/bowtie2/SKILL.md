---
name: bowtie2
description: >
  Gapped short-read alignment to contigs/genomes (coverage for binning). Use this skill when working with bowtie2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/BenLangmead/bowtie2. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'alignment', 'short-read']
upstream: https://github.com/BenLangmead/bowtie2
stage: mapping
---

# Bowtie 2

Upstream: [Bowtie 2](https://github.com/BenLangmead/bowtie2)

## Citation

Langmead, B. & Salzberg, S. L. Fast gapped-read alignment with Bowtie 2. *Nat. Methods* **9**, 357–359 (2012). https://doi.org/10.1038/nmeth.1923

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Default short-read mapper for **assembly→coverage→binning**. Index once per assembly; keep BAM sorted+indexed for CoverM/MetaBAT.

## How to run

```bash
conda install -c bioconda bowtie2  # if packaged; else follow upstream

bowtie2-build contigs.fa temp/map/contigs
bowtie2 -x temp/map/contigs -1 clean_1.fq.gz -2 clean_2.fq.gz \
  -p 16 --very-sensitive-local | samtools sort -@ 8 -o temp/map/${id}.bam
samtools index temp/map/${id}.bam
```

## Key parameters

| `-x` | index | From `bowtie2-build` |
| `-1/-2` | PE reads | Cleaned |
| `--very-sensitive-local` | optional | Soft-clip friendly |

## Decision notes

- Stage: **mapping** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

samtools · coverm · metabat2 · basalt · bwa · `tool-selection` · `metagenomics-workflow`
