---
name: maaslin2
description: >
  MaAsLin2 / MaAsLin3 — multivariable association discovery between metadata and
  meta-omic features (taxonomy, pathways, genes) with filtering, normalization,
  transforms, and FDR control. Use for differential abundance with covariates or
  longitudinal designs. Classic LDA biomarkers → lefse; figure workflows → microeco /
  visualization.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "MaAsLin2, MaAsLin3, differential-abundance, statistics, bioBakery"
  metagenomics.upstream: "https://github.com/biobakery/Maaslin2"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; not executed here"
---

# MaAsLin2 / MaAsLin3

Upstream: [biobakery/Maaslin2](https://github.com/biobakery/Maaslin2) ·
[biobakery/MaAsLin3](https://github.com/biobakery/MaAsLin3)

## Citation

Mallick, H. *et al.* Multivariable association discovery in population-scale
meta-omics studies. *PLoS Comput. Biol.* **17**, e1009442 (2021).
https://doi.org/10.1371/journal.pcbi.1009442

MaAsLin 3: Nickols, W. A. *et al.* MaAsLin 3: refining and extending generalized
multivariable linear models for meta-omic association discovery. *Nat. Methods*
(2025). https://doi.org/10.1038/s41592-025-02923-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Default for **covariate-adjusted** associations on compositional meta-omics
tables (MetaPhlAn, HUMAnN, MAG abundances, …). Pin normalization/transform,
fixed/random effects, and q-value threshold. MaAsLin3 adds prevalence vs
abundance association framing — cite the version you run.

| vs | Prefer MaAsLin when |
|----|---------------------|
| `lefse` | Multiple covariates / mixed models / modern FDR workflow |
| `microeco` | Need model coefficients vs exploratory diversity suite |

## How to run

```r
library(Maaslin2)
x <- read.delim("features.tsv", row.names = 1, check.names = FALSE)
m <- read.delim("metadata.tsv", row.names = 1, check.names = FALSE)
stopifnot(!anyDuplicated(rownames(x)), !anyDuplicated(rownames(m)))
stopifnot(setequal(rownames(x), rownames(m)), all(c("phenotype", "age") %in% names(m)))
x <- x[rownames(m), , drop = FALSE]  # samples × features in this example
fit <- Maaslin2(
  input_data = x, input_metadata = m, output = "result/maaslin2",
  fixed_effects = c("phenotype", "age"), reference = "phenotype,Control",
  normalization = "TSS", transform = "LOG", analysis_method = "LM",
  min_prevalence = 0.10, max_significance = 0.05, standardize = FALSE,
  cores = 4, plot_heatmap = TRUE, plot_scatter = TRUE)
writeLines(capture.output(sessionInfo()), "result/maaslin2/sessionInfo.txt")
```

For repeated measures, add a justified `random_effects` field whose IDs have replication. MaAsLin 3 has a different interface; use its pinned vignette rather than translating arguments mechanically.

## Decision tree

```text
Differential / association analysis?
├─ Covariates / longitudinal → maaslin2 (2 or 3)
├─ Classic two-class LDA biomarkers → lefse
├─ Explore diversity first → microeco
└─ Plot checklist → visualization
```

## Validation, recovery, and provenance

Before fitting, require unique sample/feature IDs, exact metadata overlap, non-negative finite input, adequate group sizes, no perfect confounding, and an explicit feature orientation/scale. Inspect `all_results.tsv`, significant results, model/log warnings, coefficients, standard errors, q-values, prevalence and residual diagnostics; verify the reference level and coefficient direction from a known contrast. Do not select a model after viewing significance without disclosure.

Save the unfiltered input, inclusion/exclusion manifest, factor levels, formula/options, package lockfile and `sessionInfo()`. Report effect, uncertainty, adjusted p-value, tested-feature count and sensitivity analyses—not q-values alone. Associations are conditional statistical estimates and do not establish causality or absolute abundance.

## Related skills

`research-analysis` · `ancombc` · `lefse` · `stamp` · `microeco` ·
`phyloseq` · `visualization` · `metaphlan` · `humann` · `study-design` ·
`tool-selection`
