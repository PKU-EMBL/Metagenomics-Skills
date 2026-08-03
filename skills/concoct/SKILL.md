---
name: concoct
description: >
  Composition and coverage binning of metagenomic contigs. Use this skill when working with concoct: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/BinPro/CONCOCT. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'concoct']
upstream: https://github.com/BinPro/CONCOCT
stage: binning
---

# CONCOCT

Upstream: [CONCOCT](https://github.com/BinPro/CONCOCT)

## Citation

Alneberg, J. *et al.* Binning metagenomic contigs by coverage and composition. *Nat. Methods* **11**, 1144–1146 (2014). https://doi.org/10.1038/nmeth.3103

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Strong ensemble member; cut contigs to chunks before clustering per CONCOCT docs. Memory-heavy on complex communities.

## How to run

```bash
conda install -c bioconda concoct  # if packaged; else follow upstream

cut_up_fasta.py contigs.fa -c 10000 -o 0 -m > contigs_10k.fa
# then coverage table + concoct + merge_cutup_clustering.py (see upstream)
```

## Key parameters

| contig cut length | 10 kb common | Required prep |
| coverage | BAM-derived | |

## Decision notes

- Stage: **binning** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

metabat2 · maxbin2 · dastool · metawrap · `tool-selection` · `metagenomics-workflow`
