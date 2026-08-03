---
name: deepurify
description: >
  Deepurify — multi-modal deep language model for MAG decontamination by
  matching contigs to taxonomic lineages and splitting chimeric bins into
  higher-quality sub-MAGs. Use when: (1) Cleaning contaminated MAGs after
  binning, (2) Rescuing near-threshold contaminated bins, (3) Complementing
  CheckM2/GUNC (detection vs contig removal). Upstream:
  https://github.com/ericcombiolab/Deepurify.
license: MIT
category: analysis-tools
tags: [decontamination, MAG, Deepurify, QC]
upstream: https://github.com/ericcombiolab/Deepurify
stage: assessment
---

# Deepurify

Upstream: [ericcombiolab/Deepurify](https://github.com/ericcombiolab/Deepurify)

## Citation

Zou, B. *et al.* A multi-modal deep language model for contaminant removal from
metagenome-assembled genomes. *Nat. Mach. Intell.* **6**, 1245–1255 (2024).
https://doi.org/10.1038/s42256-024-00908-5

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

CheckM2/GUNC **score** contamination; Deepurify aims to **remove contaminant
contigs** and split chimeras into sub-MAGs using sequence↔taxonomy multimodal
embeddings. Paper reports substantial gains in high-quality MAG counts across
soil, ocean, plant, freshwater, and human faecal sets — treat as
benchmark-conditioned.

Recommended order:

```text
bins → checkm2 (± gunc)
    → deepurify on contaminated / borderline bins
    → re-QC with checkm2 / gunc
    → drep / gtdbtk
```

Do not skip re-QC after decontamination. Model errors can drop true contigs —
inspect high-value novel lineages manually (`anvio`).

## How to run

```bash
# verify CLI in upstream README for your version
deepurify \
  -i bins/ \
  -o temp/deepurify \
  # model / DB paths per docs
```

## Decision tree

```text
MAG contamination problem?
├─ Detect / filter only → checkm2 / gunc / mag-qc
├─ Remove contigs / split chimeras → deepurify
├─ Interactive contig surgery → anvio
└─ Prevent upstream → multi-coverage binning + ensemble (basalt ★)
```

## Related skills

`checkm2` · `gunc` · `mag-qc` · `anvio` · `basalt` · `drep` · `tool-selection`
