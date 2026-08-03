---
name: rgi
description: >
  Antibiotic resistance gene annotation against CARD. Use this skill when working with rgi: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/arpcard/rgi. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['AMR', 'CARD', 'resistance']
upstream: https://github.com/arpcard/rgi
---

# RGI (CARD)

Upstream: [arpcard/rgi](https://github.com/arpcard/rgi) · CARD database

## Analytical thinking

RGI predicts AMR genes from proteins or contigs. Hits are **sequence homology /
model matches**, not phenotypic resistance. Prefer protein mode on NR or MAG
proteomes; record CARD DB version.

## How to run

```bash
# load CARD JSON per RGI docs, then:
rgi main -i proteins.faa -t protein -n 8 -a DIAMOND --clean \
  -o result/card/protein
```

## Related skills

`eggnog-mapper` · `prodigal` · `visualization`

