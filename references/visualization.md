# Module G — Comparative statistics and figures

Visualization and statistical comparison for profiling and MAG outputs. Label
every figure with the upstream method (MetaPhlAn, Kraken, HUMAnN, or MAG).

## Read-based composition

Typical analyses:

- Alpha diversity indices and group boxplots
- Beta diversity distances and PCoA
- Hierarchical heatmaps and stacked bar charts
- Venn / upset overlaps across groups
- Differential features: STAMP, LEfSe, MaAsLin2 volcano plots
- Sparse correlation networks (e.g. SparCC) with caution for compositionality

Inspect batch structure in ordinations before biological group testing.

## Functional profiles

- Grouped heatmaps of HUMAnN pathway or gene-family tables
- Keep pathway claims as homology-supported potential, not measured flux

## MAG-focused graphics

- MAG accumulation / rarefaction versus sample effort
- Completeness–contamination scatter plots
- Phylogenetic trees with taxonomy and quality annotations (e.g. iTOL)
- Annotation database overlaps (UpSet)
- Pathway or AMR abundance heatmaps on dereplicated genomes

## Reporting standard

State the abundance metric, rarefaction or normalization rule, statistical test,
and multiple-testing correction with each comparative claim.
