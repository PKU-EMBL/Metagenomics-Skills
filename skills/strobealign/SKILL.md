---
name: strobealign
description: >
  Ultra-fast short-read alignment with flexible seed size. Use this skill when working with strobealign: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/ksahlin/strobealign. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'alignment', 'short-read']
upstream: https://github.com/ksahlin/strobealign
stage: mapping
---

# strobealign

Upstream: [strobealign](https://github.com/ksahlin/strobealign)

## Citation

Sahlin, K. Strobealign: flexible seed size enables ultra-fast and accurate read alignment. *Genome Biol.* **23**, 260 (2022). https://doi.org/10.1186/s13059-022-02831-7

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Strong option when mapping many samples to large contig sets for binning coverage — often faster than Bowtie2/BWA at similar accuracy for metagenomes.

## How to run

```bash
conda install -c bioconda strobealign  # if packaged; else follow upstream

strobealign -t 16 contigs.fa clean_1.fq.gz clean_2.fq.gz \
  | samtools sort -@ 8 -o temp/map/${id}.bam
samtools index temp/map/${id}.bam
```

## Key parameters

| `-t` | threads | |
| reference | contigs.fa | Indexed on the fly / cached |

## Decision notes

- Stage: **mapping** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

bowtie2 · bwa · coverm · metabat2 · `tool-selection` · `metagenomics-workflow`
