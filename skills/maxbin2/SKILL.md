---
name: maxbin2
description: >
  Automated multi-metagenome contig binning. Use this skill when working with maxbin2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://sourceforge.net/projects/maxbin2/. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'maxbin']
upstream: https://sourceforge.net/projects/maxbin2/
stage: binning
---

# MaxBin 2

Upstream: [MaxBin 2](https://sourceforge.net/projects/maxbin2/)

## Citation

Wu, Y.-W., Simmons, B. A. & Singer, S. W. MaxBin 2.0: an automated binning algorithm to recover genomes from multiple metagenomic datasets. *Bioinformatics* **32**, 605–607 (2016). https://doi.org/10.1093/bioinformatics/btv638

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Complementary single-binner to MetaBAT2. Needs abundance/coverage inputs; slower on huge contig sets. Best used inside ensemble (MetaWRAP/DAS Tool/BASALT).

## How to run

```bash
conda install -c bioconda maxbin2  # if packaged; else follow upstream

run_MaxBin.pl -contig contigs.fa -abund depth.txt -out temp/bins/maxbin -thread 16
```

## Key parameters

| `-abund` | coverage | Compatible table |
| `-thread` | threads | |

## Decision notes

- Stage: **binning** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

metabat2 · concoct · dastool · metawrap · `tool-selection` · `metagenomics-workflow`
