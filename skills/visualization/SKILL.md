---
name: visualization
description: >
  Statistical visualization checklist for shotgun metagenomics across QC, taxonomy,
  function, and binning outputs. Use when: (1) Choosing alpha/beta and composition
  figure types, (2) Labeling figures by stage and method, (3) Pairing plots with
  MaAsLin2/LEfSe/microeco. For end-to-end R workflows prefer microeco.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "visualization, diversity, statistics, figures, research-analysis"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "figure design and reporting checklist reviewed; rendering is delegated to analysis skills"
---

# Visualization and statistics (checklist)

Route via `research-analysis`. For modular R pipelines prefer `microeco`.

## Rules

1. Label every figure with **stage + method + database release**
2. Inspect batch structure before biological group tests
3. Report normalization, rarefaction (if any), test, and multiple-testing correction
4. Do not plot bins as “high-quality genomes” before `mag-qc` / `checkm2` filters
5. Prefer vector PDF/SVG for journal figures; keep scripts + seed for reproducibility

## Input and figure contract

Require a validated sample/feature table, metadata ID-join report, declared
abundance unit, transform/normalization, taxonomic/functional level, contrast,
statistical result table, and palette/accessibility plan. Every figure must ship
with source data, executable code, session information, fixed random seed where
relevant, and a caption that states `n`, exclusions, uncertainty display, test,
and multiplicity correction.

Use raw points with summaries where feasible; show denominators and missingness.
Keep relative, absolute, coverage, presence/absence, and model-adjusted values in
separate panels or explicit scales. Ordinations require distance and transform;
heatmaps require scaling direction; stacked bars must identify the remainder.
Do not use truncated axes, hidden zeroes, unlabelled smoothing, decorative 3-D,
or network layouts as quantitative evidence.

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

## Figure acceptance

Verify plotted values against source tables, sample counts against the manifest,
legend/category completeness, color-blind and grayscale readability, vector/text
integrity, panel consistency, and export dimensions. Inspect both the rendered
artifact and machine-readable source; a script that exits successfully is not
proof that labels, scales, or biological interpretation are correct.

## Related skills

`research-analysis` · `microeco` · `maaslin2` · `lefse` · `multiqc` ·
`metaphlan` · `kraken2` · `humann` · `coverm` · `gtdbtk` · `basalt` ·
`mag-qc` · `anvio` · `tool-selection`
