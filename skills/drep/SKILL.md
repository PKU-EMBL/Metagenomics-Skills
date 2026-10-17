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
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
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

## Validation, recovery, and provenance

Require non-empty `dereplicated_genomes`, `data_tables/Cdb.csv`, `data_tables/Wdb.csv`, and a genome-information/quality table appropriate to the release. Reconcile every input genome as retained, clustered, or excluded with a reason; verify representative FASTAs and cluster IDs. Inspect primary/secondary clustering, minimum aligned fraction (`-nc`), representative scores, and threshold sensitivity—95% and 99% ANI do not universally equal species and strain.

Use a fresh work directory after changing genomes, quality source, ANI or coverage thresholds. Record dRep and ANI-engine versions, full command, input/checksum manifest, CheckM/CheckM2 source, clusters, representatives, exclusions, and output checksums. Dereplication chooses operational representatives; it does not prove taxonomic rank.

## Related skills

`metawrap` · `basalt` · `checkm2` · `coverm` · `gtdbtk`

