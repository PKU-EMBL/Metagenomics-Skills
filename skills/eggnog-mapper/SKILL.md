---
name: eggnog-mapper
description: >
  Orthology-based functional annotation (COG/KEGG/CAZy via eggNOG). Use this skill when working with eggnog-mapper: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/eggnogdb/eggnog-mapper. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['annotation', 'orthology', 'function']
upstream: https://github.com/eggnogdb/eggnog-mapper
---

# eggNOG-mapper

Upstream: [eggnogdb/eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper)

## Analytical thinking

Annotate **proteins** from the NR catalogue (or MAG proteomes). DIAMOND mode is
the common metagenome default. Functional tables should be combined with salmon
abundances carefully (sum TPM of genes mapping to a KO/COG).

## How to run

```bash
emapper.py --data_dir ${db}/eggnog \
  -i NR/protein.fa --cpu 16 -m diamond --override \
  -o temp/eggnog/output
```

## Related skills

`prodigal` · `salmon` · `rgi` · `visualization`

