---
name: permanova
description: >-
  Test multivariate community differences with PERMANOVA using vegan::adonis2, while aligning metadata, constraining permutations, testing multivariate dispersion, and reporting effect sizes. Use for beta-diversity hypotheses with defensible exchangeability; not as a substitute for dispersion checks or causal inference.
license: MIT
compatibility: Requires R with vegan and permute, a distance matrix or feature table, and matched sample metadata.
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "permanova,adonis2,beta-diversity,vegan,dispersion,permutations"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "vegan 2.7 API"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; template not executed here"
---

# PERMANOVA

PERMANOVA partitions variation in a distance matrix. Valid inference depends on the distance, model, dispersion, and permutation design.

## Inputs and design

Require a symmetric, finite distance matrix with zero diagonal and unique sample IDs, plus metadata whose row names match exactly. Predeclare primary exposure, confounders, interactions, permutation blocks (subject/site/plot), permutation count, and term-testing mode.

Do not permute repeated measures freely. Do not include a variable perfectly confounded with batch. Filter/transform the feature table before computing distances and keep that recipe.

## Reproducible `adonis2` template

The example tests `group` after adjusting for `batch`, with optional blocking by `subject`:

```bash
cat > run_permanova.R <<'RS'
suppressPackageStartupMessages({library(vegan); library(permute)})
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 3)
D <- as.matrix(read.delim(args[1], row.names=1, check.names=FALSE))
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(nrow(D)==ncol(D), identical(rownames(D), colnames(D)))
stopifnot(!anyDuplicated(rownames(D)), all(is.finite(D)))
stopifnot(max(abs(D-t(D))) < 1e-10, max(abs(diag(D))) < 1e-10)
stopifnot(setequal(rownames(D), rownames(meta)))
meta <- meta[rownames(D), , drop=FALSE]
stopifnot(all(c("group", "batch") %in% colnames(meta)))
meta$group <- factor(meta$group); meta$batch <- factor(meta$batch)
stopifnot(nlevels(meta$group) >= 2)
ctrl <- how(nperm=9999)
if ("subject" %in% colnames(meta)) setBlocks(ctrl) <- factor(meta$subject)
set.seed(20261018)
d <- as.dist(D)
fit <- adonis2(d ~ batch + group, data=meta, permutations=ctrl,
              by="margin", sqrt.dist=FALSE, add=FALSE)
disp <- betadisper(d, meta$group, type="median", bias.adjust=TRUE)
disp_test <- permutest(disp, permutations=ctrl)
sink(args[3]); cat("PERMANOVA\n"); print(fit)
cat("\nDISPERSION\n"); print(anova(disp)); print(disp_test); sink()
saveRDS(list(adonis2=fit, dispersion=disp, dispersion_test=disp_test,
             permutation=ctrl, seed=.Random.seed), sub("\\.txt$", ".rds", args[3]))
RS
Rscript run_permanova.R distance.tsv metadata.tsv permanova.txt \
  >permanova.stdout.log 2>permanova.stderr.log
[[ -s permanova.txt && -s permanova.rds ]] || exit 3
```

Edit the formula and blocking only according to the study design. `by="margin"` tests marginal terms; sequential (`by="terms"`) tests depend on term order. Document the choice.

## Validate and report

- inspect ordination and distances for outliers and batch structure;
- report pseudo-F, R², permutation p-value, number/type of permutations, distance, preprocessing, and sample size;
- report `betadisper`/permutation result and group dispersions;
- perform planned pairwise contrasts with multiplicity correction if the omnibus test supports them;
- run sensitivity analyses for outliers, distance choice, and confounder specification.

If dispersion differs, location and dispersion effects may be entangled; do not state a centroid shift without qualification.

## Analytical thinking

A significant PERMANOVA does not show which taxa drive differences and is not causal. R² conveys magnitude but is design-dependent. Restricted permutations preserve exchangeability; adding more invalid permutations does not improve inference.

## Sources

- vegan: https://github.com/vegandevs/vegan
- `adonis2`: https://vegandevs.github.io/vegan/reference/adonis.html
