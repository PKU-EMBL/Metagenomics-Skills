---
name: ancombc
description: >
  ANCOM-BC / ANCOM-BC2 — compositionally aware differential abundance with
  sampling-fraction bias correction (Bioconductor ANCOMBC). Use when DA must account for
  compositionality and unequal sampling fractions; complements MaAsLin2/LEfSe.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "ANCOM-BC, ANCOM-BC2, differential-abundance, compositionality, Bioconductor"
  metagenomics.upstream: "https://github.com/FrederickHuangLin/ANCOMBC"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "ANCOM-BC2 R API reviewed against upstream; not executed here"
---

# ANCOM-BC / ANCOM-BC2

Upstream: [FrederickHuangLin/ANCOMBC](https://github.com/FrederickHuangLin/ANCOMBC) ·
Bioconductor: https://bioconductor.org/packages/ANCOMBC/

## Citation

Lin, H. & Peddada, S. D. Analysis of compositions of microbiomes with bias
correction. *Nat. Commun.* **11**, 3514 (2020).
https://doi.org/10.1038/s41467-020-17041-7

ANCOM-BC2: Lin, H. & Peddada, S. D. Multigroup analysis of compositions of
microbiomes with covariate adjustments and repeated measures. *Nat. Methods*
**21**, 83–89 (2024). https://doi.org/10.1038/s41592-023-02092-7

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

ANCOM-BC estimates **sampling fractions**, corrects compositional bias, and
reports taxon-wise effects with CIs and FDR. Prefer when compositionality is a
primary concern. Pin `ancombc` vs `ancombc2`, formula, and prevalence filters.
Often takes phyloseq / TreeSummarizedExperiment-style inputs.

| vs | Prefer ANCOM-BC when |
|----|----------------------|
| `maaslin2` | Explicit sampling-fraction bias correction focus |
| `lefse` | Modern FDR + CI vs classic LDA |
| `stamp` | R/Bioconductor pipeline vs GUI exploratory tests |

## How to run

```r
library(ANCOMBC)
counts <- as.matrix(read.delim("counts.tsv", row.names = 1, check.names = FALSE))
meta <- read.delim("metadata.tsv", row.names = 1, check.names = FALSE)
stopifnot(all(is.finite(counts)), all(counts >= 0), all(counts == floor(counts)))
stopifnot(!anyDuplicated(colnames(counts)), !anyDuplicated(rownames(meta)))
stopifnot(setequal(colnames(counts), rownames(meta)), all(c("group", "age") %in% names(meta)))
meta <- meta[colnames(counts), , drop = FALSE]
meta$group <- relevel(factor(meta$group), ref = "Control")
set.seed(2024)
fit <- ancombc2(
  data = counts, meta_data = meta, fix_formula = "group + age",
  rand_formula = NULL, p_adj_method = "holm", pseudo_sens = TRUE,
  prv_cut = 0.10, lib_cut = 0, s0_perc = 0.05, group = "group",
  struc_zero = TRUE, neg_lb = TRUE, alpha = 0.05, n_cl = 4,
  verbose = TRUE, global = TRUE, pairwise = TRUE,
  dunnet = FALSE, trend = FALSE)
dir.create("result/ancombc2", recursive = TRUE, showWarnings = FALSE)
write.csv(fit$res, "result/ancombc2/coefficients.csv", row.names = FALSE)
write.csv(fit$res_pair, "result/ancombc2/pairwise.csv", row.names = FALSE)
writeLines(capture.output(sessionInfo()), "result/ancombc2/sessionInfo.txt")
```

This matrix route requires raw integer feature counts with taxa as rows and samples as columns. For repeated measures or phyloseq/TreeSummarizedExperiment input, use the pinned ANCOM-BC2 vignette and declare the random-effects formula.

## Decision tree

```text
Differential abundance?
├─ Bias-corrected compositional DA → ancombc
├─ Multivariable / longitudinal meta-omics → maaslin2
├─ Classic LDA → lefse
└─ GUI exploratory → stamp
```

## Validation, recovery, and provenance

Validate sample alignment, integer counts, library sizes, prevalence, group replication, factor references, design rank and confounding before fitting. Inspect convergence/warnings, sensitivity scores, structural-zero calls, effect direction, confidence/standard errors, adjusted p-values, global/pairwise multiplicity families, and taxa removed by filters. Repeat key conclusions under justified prevalence/library thresholds and with/without problematic samples.

Save original counts/metadata, exclusions, exact function call and seed, result objects/tables, Bioconductor lockfile, and `sessionInfo()`. Report estimates and uncertainty with the correction family; do not compare ANCOM-BC log-fold changes directly with ordinary relative-abundance fold changes. Results are model-dependent associations, not causal or absolute-load evidence.

## Related skills

`research-analysis` · `maaslin2` · `lefse` · `phyloseq` · `microeco` ·
`stamp` · `tool-selection`
