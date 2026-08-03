---
name: drep
description: >
  Dereplicate microbial genomes by ANI to species/strain catalogues. Use this skill when working with drep: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/MrOlm/drep. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['dereplication', 'ANI', 'MAG']
upstream: https://github.com/MrOlm/drep
---

# dRep

Upstream: [MrOlm/drep](https://github.com/MrOlm/drep)

## Analytical thinking

dRep collapses redundant MAGs into representatives. **`-sa 0.95`** ≈ species;
**`-sa 0.99`** ≈ strain-level. Quality filters (`-comp/-con`) silently drop
genomes—align them with `checkm2` / `mag-qc` policy.

For >~20k genomes, `--ignoreGenomeQuality` may be needed; then run CheckM2
separately.

## How to run

```bash
dRep dereplicate temp/drep95/ -g bins/*.fa \
  -sa 0.95 -nc 0.30 -comp 50 -con 10 -p 16
```

## Related skills

`metawrap` · `basalt` · `checkm2` · `coverm` · `gtdbtk`

