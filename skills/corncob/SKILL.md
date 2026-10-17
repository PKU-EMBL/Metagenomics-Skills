---
name: corncob
description: >-
  Model taxon counts with corncob beta-binomial regression to test differential relative abundance and/or variability while adjusting covariates. Use for microbiome count data when mean and dispersion formulas, null models, and sufficient replication can be specified explicitly.
license: MIT
compatibility: Requires R with corncob 0.4.3 and phyloseq, raw taxon counts, and matched sample metadata.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "corncob,beta-binomial,differential-abundance,variability,regression,r"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.4.3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; template not executed here"
---

# corncob

corncob models feature counts conditional on sample totals using beta-binomial regression. The mean (`formula`) and dispersion (`phi.formula`) models are distinct.

## Inputs and design

Use raw non-negative integer counts (taxa rows, samples columns), matched metadata, a predeclared exposure, covariates, reference levels, and separate hypotheses for abundance versus variability. Filter extremely rare features before looking at outcomes and report the rule.

The example tests the `group` contribution to mean abundance while allowing `group + batch` in dispersion in both full and null models.

## Differential-abundance template

```bash
cat > run_corncob.R <<'RS'
suppressPackageStartupMessages({library(corncob); library(phyloseq)})
args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==3)
counts <- read.delim(args[1], row.names=1, check.names=FALSE)
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(setequal(colnames(counts), rownames(meta)),
          all(c("group","batch") %in% names(meta)))
meta <- meta[colnames(counts),,drop=FALSE]
stopifnot(all(counts >= 0), all(abs(as.matrix(counts)-round(as.matrix(counts)))<1e-8))
keep <- rowSums(counts > 0) >= max(3, ceiling(0.10*ncol(counts)))
writeLines(rownames(counts)[!keep], "corncob_filtered_features.txt")
ps <- phyloseq(otu_table(as.matrix(counts[keep,,drop=FALSE]), taxa_are_rows=TRUE),
               sample_data(meta))
set.seed(20261018)
fit <- differentialTest(formula=~ group + batch,
                        phi.formula=~ group + batch,
                        formula_null=~ batch,
                        phi.formula_null=~ group + batch,
                        test="Wald", boot=FALSE, data=ps, fdr_cutoff=0.05)
res <- data.frame(feature_id=names(fit$p), p_value=unname(fit$p),
                  q_value=unname(fit$p_fdr),
                  significant=names(fit$p) %in% fit$significant_taxa,
                  check.names=FALSE)
write.table(res, args[3], sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(fit, sub("\\.tsv$", ".rds", args[3]))
RS
Rscript run_corncob.R counts.tsv metadata.tsv corncob_da.tsv \
  >corncob.stdout.log 2>corncob.stderr.log
[[ -s corncob_da.tsv && -s corncob_da.rds ]] || exit 3
```

Check object field names against the pinned corncob release. To test differential variability, keep the mean formula identical in full/null and remove the tested variable only from `phi.formula_null`, as documented upstream.

## Validation

- inspect convergence/warnings and prevalence/depth for every highlighted taxon;
- plot model coefficients and observed counts/proportions;
- verify factor references and design-matrix rank;
- use bootstrap/LRT or alternate specifications when appropriate and planned;
- report tested feature count, FDR method/cutoff, coefficients with uncertainty, and both formulas.

A significant dispersion effect is differential variability, not necessarily a mean shift. Zero inflation, unmodeled repeated measures, or complete separation can destabilize estimates.

## Analytical thinking

The response is relative abundance conditional on total counts; findings are not absolute microbial loads. Full/null formulas define the hypothesis, so copying formulas without understanding them can test the wrong term. Avoid causal language in observational designs.

## Source

- https://github.com/statdivlab/corncob
