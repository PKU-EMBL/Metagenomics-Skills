---
name: skani
description: >
  Fast robust average nucleotide identity (ANI) for metagenomic genomes and
  MAG comparisons. Use for species-level clustering, novelty vs GTDB/UHGG, and
  scalable ANI matrices. Upstream: https://github.com/bluenote-1577/skani.
license: MIT
category: analysis-tools
tags: [ANI, comparative-genomics, MAG]
upstream: https://github.com/bluenote-1577/skani
stage: binning
---

# skani

Upstream: [bluenote-1577/skani](https://github.com/bluenote-1577/skani)

## Citation

Shaw, J. & Yu, Y. W. Fast and robust metagenomic sequence comparison through
sparse chaining with skani. *Nat. Methods* **20**, 1661–1665 (2023).
https://doi.org/10.1038/s41592-023-02018-3

## Analytical thinking

skani estimates **ANI** quickly on incomplete MAGs better than many classic
tools that assume near-complete genomes. Use for:

- Dereplication cross-checks vs `drep`
- Novelty vs GTDB reps / UHGG (`mgnify`)
- All-vs-all MAG similarity heatmaps

95% ANI remains a common species-level heuristic — state your cutoff.

## How to run

```bash
conda install -c bioconda skani

# Sketch + triangle / dist
skani triangle bins_hq/*.fa > temp/ani/skani.triangle
skani dist bins_hq/query.fa bins_hq/*.fa > temp/ani/query_vs_all.tsv
```

## Related skills

`drep` · `gtdb` · `mgnify` · `checkm2` · `gtdbtk` · `mag-qc`
