---
name: instrain
description: >
  Strain-level microdiversity and shared-strain detection from metagenomes. Use this skill when working with instrain: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/MrOlm/inStrain. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['strain', 'microdiversity', 'snp']
upstream: https://github.com/MrOlm/inStrain
stage: strain
---

# inStrain

Upstream: [inStrain](https://github.com/MrOlm/inStrain)

## Citation

Olm, M. R. *et al.* inStrain profiles population microdiversity from metagenomic data and sensitively detects shared microbial strains. *Nat. Biotechnol.* **39**, 727–736 (2021). https://doi.org/10.1038/s41587-020-00797-0

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Requires high-quality mapping to genomes/MAGs. Run after binning+dRep; not a replacement for species profiling.

## How to run

```bash
conda install -c bioconda instrain  # if packaged; else follow upstream

inStrain profile temp/map/${id}.bam genomes.fa -o temp/instrain/${id} -p 16
```

## Key parameters

| BAM | to dereplicated genomes | |
| coverage filters | see docs | |

## Decision notes

- Stage: **strain** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

bowtie2 · drep · coverm · metaphlan · `tool-selection` · `metagenomics-workflow`
