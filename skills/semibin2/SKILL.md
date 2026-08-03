---
name: semibin2
description: >
  Self-supervised contrastive learning binning for short- and long-read assemblies. Use this skill when working with semibin2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/BigDataBiology/SemiBin. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'semibin', 'self-supervised']
upstream: https://github.com/BigDataBiology/SemiBin
stage: binning
---

# SemiBin2

Upstream: [SemiBin2](https://github.com/BigDataBiology/SemiBin)

## Citation

Pan, S., Zhao, X.-M. & Coelho, L. P. SemiBin2: self-supervised contrastive learning leads to better MAGs for short- and long-read sequencing. *Bioinformatics* **39**, i21–i29 (2023). https://doi.org/10.1093/bioinformatics/btad209

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Modern single-binner alternative/ensemble member. Prefer SemiBin2 over SemiBin1. Still combine with ensemble refinement for catalogues when possible.

## How to run

```bash
conda install -c bioconda semibin2  # if packaged; else follow upstream

SemiBin2 single_easy_bin -i contigs.fa -b temp/map/*.bam -o temp/bins/semibin2 -t 16
```

## Key parameters

| `single_easy_bin` | one sample | |
| multi-sample modes | see docs | Related samples |

## Decision notes

- Stage: **binning** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

metabat2 · vamb · dastool · basalt · bowtie2 · `tool-selection` · `metagenomics-workflow`
