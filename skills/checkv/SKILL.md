---
name: checkv
description: >
  Quality assessment of metagenome-assembled viral genomes. Use this skill when working with checkv: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://bitbucket.org/berkeleylab/checkv. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['virus', 'qc', 'genome-mining']
upstream: https://bitbucket.org/berkeleylab/checkv
stage: mining
---

# CheckV

Upstream: [CheckV](https://bitbucket.org/berkeleylab/checkv)

## Citation

Nayfach, S. *et al.* CheckV assesses the quality and completeness of metagenome-assembled viral genomes. *Nat. Biotechnol.* **39**, 578–585 (2021). https://doi.org/10.1038/s41587-020-00774-7

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Analogous to CheckM2 but for **viruses**. Completeness/contamination estimates guide which viral bins to trust. Always report CheckV DB version.

## How to run

```bash
conda install -c bioconda checkv  # if packaged; else follow upstream docs

checkv end_to_end viral_contigs.fa temp/checkv -t 16 -d $CHECKVDB
```

## Key parameters

| `$CHECKVDB` | required | Pin |
| input | putative viral seqs | From VirSorter2/geNomad |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

virsorter2 · genomad · mag-qc · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
