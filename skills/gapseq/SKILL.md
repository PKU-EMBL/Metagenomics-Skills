---
name: gapseq
description: >
  Predict bacterial metabolic pathways and reconstruct genome-scale metabolic models. Use this skill when working with gapseq: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/jotech/gapseq. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['metabolism', 'GEMs', 'genome-mining']
upstream: https://github.com/jotech/gapseq
stage: mining
---

# gapseq

Upstream: [gapseq](https://github.com/jotech/gapseq)

## Citation

Zimmermann, J., Kaleta, C. & Waschina, S. gapseq: informed prediction of bacterial metabolic pathways and reconstruction of accurate metabolic models. *Genome Biol.* **22**, 81 (2021). https://doi.org/10.1186/s13059-021-02295-1

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Downstream of genome annotation for **pathway/model mining**. Needs reasonably complete MAGs; low-completeness bins produce hollow models.

## How to run

```bash
conda install -c bioconda gapseq  # if packaged; else follow upstream docs

gapseq find -p all genome.fa
gapseq draft -r genome -c genome-draft.RDS -p genome-all-Reactions.tbl -b 136
gapseq fill -m genome-draft.RDS -n genome-Medium.csv -c genome-rxnWeights.RDS -n genome-rxnXgenes.RDS
```

## Key parameters

| completeness | prefer high-quality MAGs | |
| pathways | `-p all` costly | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

dram · bakta · checkm2 · eggnog-mapper · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
