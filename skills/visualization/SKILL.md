---
name: visualization
description: >
  Statistical visualization for metagenomic profiles and MAG catalogues.
  Use this skill when: (1) Alpha/beta diversity plots,
  (2) Composition heatmaps and stacked bars,
  (3) STAMP/LEfSe/MaAsLin2 comparative figures,
  (4) MAG quality and phylogeny plots,
  (5) Labeling figures by method (MetaPhlAn vs Kraken vs MAG).

  For generating tables, use metaphlan/humann/kraken2, salmon, or coverm.
license: MIT
category: evaluation
tags: [visualization, diversity, statistics, figures]
---

# Visualization and Statistics

## Rules

1. Label every figure with the upstream method and database release
2. Inspect batch structure before biological group tests
3. Report normalization, rarefaction, test, and multiple-testing correction

## Read-based figures

- Alpha diversity boxplots
- Beta PCoA / distance heatmaps
- Taxon heatmaps and stacked bars
- Differential features (STAMP, LEfSe, MaAsLin2)
- Optional SparCC networks (compositionality caution)

## Functional figures

- Grouped HUMAnN pathway/gene-family heatmaps
- Pathway presence ≠ enzymatic activity

## MAG figures

- Rarefaction / accumulation vs sample effort
- Completeness–contamination scatter
- GTDB phylogeny with quality annotations
- Annotation overlaps (UpSet), AMR heatmaps

## Related skills

- `metaphlan` / `humann` / `kraken2` / `coverm` / `basalt` — data sources
- `mag-qc` — filter before plotting catalogue claims
