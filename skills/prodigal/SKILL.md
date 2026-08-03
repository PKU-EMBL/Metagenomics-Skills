---
name: prodigal
description: >
  Protein-coding gene prediction; use -p meta for metagenomes. Use this skill when working with prodigal: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/hyattpd/Prodigal. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['genes', 'orf']
upstream: https://github.com/hyattpd/Prodigal
---

# Prodigal

Upstream: [hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)

## Analytical thinking

For metagenomes always use **`-p meta`**. Gene catalogues inherit assembly
errors—garbage contigs produce garbage ORFs. Optionally keep only complete genes
(`partial=00`) when catalogs are huge.

## How to run

```bash
prodigal -i contigs.fa \
  -d genes.fna -a genes.faa \
  -o genes.gff -p meta -f gff
```

## Decision tree

```text
Have contigs?
├─ Build gene catalogue → prodigal → cd-hit → salmon → eggnog-mapper
└─ Only MAGs → predict genes per MAG later for annotation
```

## Related skills

`megahit` · `cd-hit` · `salmon` · `eggnog-mapper`

