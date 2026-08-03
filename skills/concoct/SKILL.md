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

CONCOCT (Alneberg *et al.*, 2014) pioneered joint **composition + multi-sample
coverage** clustering (Gaussian mixture models). It remains a valuable **ensemble
member** because its inductive bias differs from MetaBAT2/MaxBin2/DL binners.

Operational rules:

- Cut long contigs into chunks (commonly ~10 kb) before clustering, then merge
  cutup clusters back to contigs — required by the CONCOCT workflow.
- Multi-coverage inputs matter (Mattock & Watson 2023); single-sample coverage
  weakens the method’s original strength.
- Memory-heavy on complex communities; often optional inside MetaWRAP.


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

- Stage: **binning** — strong ensemble member (composition + multi-coverage)
- Cut contigs (~10 kb) before clustering; prefer multi-coverage inputs
- Feed into `basalt` ★ / `metawrap` / `dastool` for catalogues

## Related skills

metabat2 · maxbin2 · dastool · metawrap · `tool-selection` · `metagenomics-workflow`
