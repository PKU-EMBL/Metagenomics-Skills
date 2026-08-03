---
name: visualization
description: >
  Statistical visualization for shotgun metagenomics across QC, taxonomy,
  function, and binning outputs. Use this skill when: (1) Alpha/beta diversity,
  (2) Composition heatmaps and stacked bars, (3) Comparative figures
  (STAMP/LEfSe/MaAsLin2), (4) Bin quality and phylogeny plots, (5) Labeling
  figures by stage and method. For generating tables, use the stage skills
  (metaphlan, humann, kraken2, salmon, coverm, gtdbtk, …).
license: MIT
category: evaluation
tags: [visualization, diversity, statistics, figures]
---

# Visualization and Statistics

## Rules

1. Label every figure with **stage + method + database release**
2. Inspect batch structure before biological group tests
3. Report normalization, rarefaction, test, and multiple-testing correction
4. Do not plot bins as “high-quality genomes” before `mag-qc` / `checkm2` filters

## By stage

### Taxonomic annotation (reads)
- Alpha diversity boxplots
- Beta PCoA / distance heatmaps
- Taxon heatmaps and stacked bars
- Differential taxa (STAMP, LEfSe, MaAsLin2)

### Functional annotation
- HUMAnN pathway / gene-family heatmaps
- eggNOG / AMR summary bars (pathway presence ≠ enzymatic activity)

### Binning / genomes
- Rarefaction / accumulation vs sample effort
- Completeness–contamination scatter
- GTDB phylogeny with quality annotations
- Annotation overlaps (UpSet), AMR heatmaps

## Related skills

`metaphlan` · `kraken2` · `humann` · `coverm` · `gtdbtk` · `basalt` · `metawrap` · `mag-qc`
