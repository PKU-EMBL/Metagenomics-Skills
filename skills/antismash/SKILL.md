---
name: antismash
description: >
  Detect and annotate biosynthetic gene clusters (BGCs) in genomes and MAGs. Use this skill when working with antismash: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/antismash/antismash. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['BGC', 'secondary-metabolite', 'genome-mining']
upstream: https://github.com/antismash/antismash
stage: mining
---

# antiSMASH

Upstream: [antiSMASH](https://github.com/antismash/antismash)

## Citation

Blin, K. *et al.* antiSMASH 7.0: new and improved predictions for detection, regulation, chemical structures and visualisation. *Nucleic Acids Res.* **51**, W46–W50 (2023). https://doi.org/10.1093/nar/gkad344

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

antiSMASH is the default **natural-product / BGC mining** tool on assembled genomes or MAGs. Run after binning QC — fragmented bins yield truncated clusters. Predictions are gene-cluster hypotheses, not validated compounds.

## How to run

```bash
conda install -c bioconda antismash  # if packaged; else follow upstream docs

antismash genome.fa --output-dir temp/antismash/${id} --cpus 16 --genefinding-tool prodigal
```

## Key parameters

| `--genefinding-tool` | prodigal | Metagenome/MAG friendly |
| taxon | bacteria/fungi | Match organism |
| databases | install once | Large |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

prodigal · bakta · dram · genomad · basalt · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
