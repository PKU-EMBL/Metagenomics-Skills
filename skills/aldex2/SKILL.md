---
name: aldex2
description: >-
  Perform compositional differential-abundance analysis with ALDEx2 using Dirichlet Monte Carlo sampling, log-ratio transforms, expected tests, and effect sizes. Use for two-group or model-matrix microbiome count comparisons when denominator and scale assumptions are explicit.
license: MIT
compatibility: Requires R/Bioconductor ALDEx2 and an integer feature-by-sample count matrix with matched metadata.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "aldex2,differential-abundance,compositional,clr,effect-size,r"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "upstream snapshot 1.35.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; template not executed here"
---

# ALDEx2

ALDEx2 models sampling uncertainty with Dirichlet Monte Carlo instances and performs log-ratio analysis. Denominator/scale assumptions define the estimand.

## Input contract

- raw, non-negative integer counts with features as rows and samples as columns;
- metadata with exact sample IDs and a predeclared two-group contrast or design matrix;
- removal/reporting of all-zero features and a defensible prevalence/abundance filter;
- explicit denominator (`all`, `iqlr`, `zero`, or validated feature set) and optional scale model.

Do not feed relative abundances, rarefied values, CLR values, or arbitrary pseudocount-transformed data.

## Two-group analysis

```bash
cat > run_aldex2.R <<'RS'
suppressPackageStartupMessages(library(ALDEx2))
args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==3)
counts <- read.delim(args[1], row.names=1, check.names=FALSE)
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(setequal(colnames(counts), rownames(meta)), "group" %in% names(meta))
meta <- meta[colnames(counts),,drop=FALSE]
stopifnot(all(is.finite(as.matrix(counts))), all(counts >= 0),
          all(abs(as.matrix(counts)-round(as.matrix(counts))) < 1e-8))
keep <- rowSums(counts) > 0
writeLines(rownames(counts)[!keep], "aldex2_all_zero_removed.txt")
counts <- counts[keep,,drop=FALSE]
group <- droplevels(factor(meta$group)); stopifnot(nlevels(group)==2)
set.seed(20261018)
clr <- aldex.clr(counts, group, mc.samples=128, denom="all", verbose=FALSE)
test <- aldex.ttest(clr, paired.test=FALSE, verbose=FALSE)
effect <- aldex.effect(clr, CI=TRUE, verbose=FALSE)
res <- cbind(feature_id=rownames(test), test, effect)
write.table(res, args[3], sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(list(result=res, group=group, denom="all", mc.samples=128),
        sub("\\.tsv$", ".rds", args[3]))
stopifnot(nrow(res)==nrow(counts), all(c("we.eBH", "effect") %in% names(res)))
RS
Rscript run_aldex2.R counts.tsv metadata.tsv aldex2_results.tsv \
  >aldex2.stdout.log 2>aldex2.stderr.log
[[ -s aldex2_results.tsv && -s aldex2_results.rds ]] || exit 3
```

Use `paired.test=TRUE` only for a valid paired design. For covariates/complex designs, construct a full-rank model matrix and use `aldex.clr` with `aldex.glm` plus `aldex.glm.effect`; do not reduce a confounded study to two groups.

## Validation and interpretation

- check sample matching, library-size distributions, sparsity, and denominator stability;
- increase Monte Carlo samples and confirm high-priority findings are stable;
- report `diff.btw`, `diff.win`, `effect` with intervals, and expected adjusted p-values;
- inspect MA/MW plots and sample-level CLR values for outlier-driven effects;
- compare `all` with `iqlr` or a justified scale model when asymmetry is plausible.

ALDEx2 results can vary near thresholds because of Monte Carlo sampling. Store the seed and RDS object.

## Analytical thinking

Differential log-ratios are relative changes, not absolute abundance changes. A feature can change because its denominator changes. Prioritize effect size and uncertainty over a binary FDR label, and corroborate with `$absolute-abundance` when load data exist.

## Sources

- https://github.com/ggloor/ALDEx_bioc
- https://bioconductor.org/packages/ALDEx2
