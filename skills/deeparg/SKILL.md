---
name: deeparg
description: >
  Deep-learning prediction of antibiotic resistance genes from metagenomic data. Use this skill when working with deeparg: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/gaarangoa/DeepARG. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['AMR', 'ARG', 'genome-mining']
upstream: https://github.com/gaarangoa/DeepARG
stage: mining
---

# DeepARG

Upstream: [DeepARG](https://github.com/gaarangoa/DeepARG)

## Citation

Arango-Argoty, G. *et al.* DeepARG: a deep learning approach for predicting antibiotic resistance genes from metagenomic data. *Microbiome* **6**, 23 (2018). https://doi.org/10.1186/s40168-018-0401-z

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Complement to **RGI/CARD** for ARG mining from reads or genes. Model-based predictions need careful thresholds; always cross-check critical ARGs with RGI and report both DB/model versions.

## How to run

```bash
conda install -c bioconda deeparg  # if packaged; else follow upstream docs

# follow upstream install; example gene mode:
deepARG --align --type prot --genes genes.faa --model LS --out temp/deeparg/${id}
```

## Key parameters

| mode | reads vs genes | |
| model | LS/SS | See docs |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

rgi · genomad · humann · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
