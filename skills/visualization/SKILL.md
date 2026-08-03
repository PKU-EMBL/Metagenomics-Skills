---
name: visualization
description: >
  Statistical visualization checklist for shotgun metagenomics across QC,
  taxonomy, function, and binning outputs. Use when: (1) Choosing alpha/beta
  and composition figure types, (2) Labeling figures by stage and method,
  (3) Pairing plots with MaAsLin2/LEfSe/microeco. For end-to-end R workflows
  prefer microeco. Route via research-analysis.
license: MIT
category: evaluation
tags: [visualization, diversity, statistics, figures, research-analysis]
stage: report
---

# Visualization and statistics (checklist)

Route via `research-analysis`. For modular R pipelines prefer `microeco`.

## Rules

1. Label every figure with **stage + method + database release**
2. Inspect batch structure before biological group tests
3. Report normalization, rarefaction (if any), test, and multiple-testing correction
4. Do not plot bins as “high-quality genomes” before `mag-qc` / `checkm2` filters
5. Prefer vector PDF/SVG for journal figures; keep scripts + seed for reproducibility

## By stage

### QC
- Read counts / Q-score summaries → often via `multiqc`
- Host-depletion fractions before/after KneadData

### Taxonomic annotation (reads)
- Alpha diversity boxplots / rarefaction curves
- Beta PCoA / NMDS + distance heatmaps
- Taxon heatmaps and stacked bars (relative abundance)
- Differential taxa: `maaslin2` (default multivariable) · `lefse` (classic LDA)

### Functional annotation
- HUMAnN pathway / gene-family heatmaps
- eggNOG / AMR / element-cycling summary bars (presence ≠ activity)

### Binning / genomes
- Accumulation vs sample effort
- Completeness–contamination scatter (`checkm2`)
- GTDB phylogeny with quality annotations
- Annotation overlaps (UpSet), AMR / defense heatmaps on MAGs

## Pairing

| Plot goal | Prefer |
|-----------|--------|
| Full R exploration suite | `microeco` |
| Multivariable volcano / coefficients | `maaslin2` |
| Cladogram / LDA scores | `lefse` |
| Multi-sample QC HTML | `multiqc` |

## Related skills

`research-analysis` · `microeco` · `maaslin2` · `lefse` · `multiqc` ·
`metaphlan` · `kraken2` · `humann` · `coverm` · `gtdbtk` · `basalt` ·
`mag-qc` · `anvio` · `tool-selection`
