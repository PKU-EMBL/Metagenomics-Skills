---
name: drep
description: >
  Dereplicate microbial genomes by ANI to species/strain catalogues. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "dereplication, ANI, MAG"
  metagenomics.upstream: "https://github.com/MrOlm/drep"
---

# dRep

Upstream: [MrOlm/drep](https://github.com/MrOlm/drep)

## Citation

Olm, M. R., Brown, C. T., Brooks, B. & Banfield, J. F. dRep: a tool for fast and accurate genomic comparisons that enables improved genome recovery from metagenomes through de-replication. *ISME J.* **11**, 2864–2868 (2017). https://doi.org/10.1038/ismej.2017.126

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

