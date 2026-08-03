---
name: dram
description: >
  Distill microbial metabolism annotations for microbiome genomes/MAGs. Use this skill when working with dram: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/WrightonLabCSU/DRAM. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['metabolism', 'annotation', 'genome-mining']
upstream: https://github.com/WrightonLabCSU/DRAM
stage: mining
---

# DRAM

Upstream: [DRAM](https://github.com/WrightonLabCSU/DRAM)

## Citation

Shaffer, M. *et al.* DRAM for distilling microbial metabolism to automate the curation of microbiome function. *Nucleic Acids Res.* **48**, 8883–8900 (2020). https://doi.org/10.1093/nar/gkaa621

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

DRAM mines **metabolic potential** (KEGG/MEROPS/CAZy/…) into curated distillate tables — ideal for ecological/functional MAG stories. Heavy DB install; pin DRAM DB release.

## How to run

```bash
conda install -c bioconda dram  # if packaged; else follow upstream docs

DRAM.py annotate -i bins/*.fa -o temp/dram/annotate --threads 16
DRAM.py distill -i temp/dram/annotate/annotations.tsv -o temp/dram/distill
```

## Key parameters

| annotate | genomes/MAGs | |
| distill | summary products | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

eggnog-mapper · bakta · antismash · gapseq · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
