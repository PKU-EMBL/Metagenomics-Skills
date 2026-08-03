---
name: cd-hit
description: >
  Cluster genes/proteins to build non-redundant catalogues. Use this skill when working with cd-hit: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/weizhongli/cdhit. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['clustering', 'dereplication']
upstream: https://github.com/weizhongli/cdhit
---

# CD-HIT

Upstream: [weizhongli/cdhit](https://github.com/weizhongli/cdhit)

## Analytical thinking

`cd-hit-est` collapses redundant nucleotide ORFs into a non-redundant catalogue.
Defaults used widely in shotgun catalogues: identity **0.95**, alignment coverage
**0.9** (`-c 0.95 -aS 0.9`). Changing thresholds changes biological interpretation
of “a gene”—report them.

## How to run

```bash
cd-hit-est -i genes.fna -o NR/nucleotide.fa \
  -aS 0.9 -c 0.95 -G 0 -g 0 -T 0 -M 0
seqkit translate --trim NR/nucleotide.fa > NR/protein.fa
```

## Related skills

`prodigal` · `salmon` · `eggnog-mapper`

