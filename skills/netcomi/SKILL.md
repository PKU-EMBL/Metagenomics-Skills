---
name: netcomi
description: >-
  Construct, analyze, compare, and visualize composition-aware microbial association networks with NetCoMi. Use when network preprocessing, association estimator, sparsification, group comparison, stability, and multiple-testing choices can be declared; not to claim direct ecological interactions from correlations.
license: MIT
compatibility: Requires R with NetCoMi 1.3.0, phyloseq, method dependencies, raw count data, metadata, and adequate sample size.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "netcomi,network,association,compositionality,spring,spieceasi,r"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.3.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; template not executed here"
---

# NetCoMi

NetCoMi separates network construction (`netConstruct`), graph analysis (`netAnalyze`), comparison (`netCompare`), and differential networks (`diffnet`).

## Input/design contract

Use raw count data with taxa rows and samples columns, exact metadata matching, a predeclared taxonomic rank/filter, and enough independent samples for the chosen estimator. Avoid selecting taxa, estimator, or sparsification by the most visually appealing graph.

## Single-network SPRING example

```bash
cat > run_netcomi.R <<'RS'
suppressPackageStartupMessages({library(NetCoMi); library(phyloseq)})
args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==3)
counts <- read.delim(args[1], row.names=1, check.names=FALSE)
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(setequal(colnames(counts), rownames(meta)), all(counts >= 0))
meta <- meta[colnames(counts),,drop=FALSE]
keep <- rowSums(counts > 0) >= ceiling(0.20*ncol(counts))
ps <- phyloseq(otu_table(as.matrix(counts[keep,,drop=FALSE]), taxa_are_rows=TRUE),
               sample_data(meta))
set.seed(20261018)
net <- netConstruct(ps, filtTax="none", filtSamp="none", measure="spring",
                    measurePar=list(nlambda=10, rep.num=10, Rmethod="approx"),
                    normMethod="none", zeroMethod="none", sparsMethod="none",
                    dissFunc="signed", verbose=2, seed=20261018)
props <- netAnalyze(net, centrLCC=TRUE,
                    clustMethod="cluster_fast_greedy",
                    hubPar="eigenvector", weightDeg=FALSE, normDeg=FALSE)
write.table(net$edgelist1, args[3], sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(list(network=net, properties=props, retained_taxa=taxa_names(ps)),
        sub("\\.tsv$", ".rds", args[3]))
RS
Rscript run_netcomi.R counts.tsv metadata.tsv netcomi_edges.tsv \
  >netcomi.stdout.log 2>netcomi.stderr.log
[[ -s netcomi_edges.tsv && -s netcomi_edges.rds ]] || exit 3
```

The upstream SPRING example uses no extra normalization/zero replacement because SPRING handles counts through its own model. Other association measures require method-appropriate preprocessing; do not reuse these settings blindly.

## Group comparison

For two groups, construct both networks under identical preprocessing (or use the documented group argument), run `netAnalyze`, then `netCompare` with a predeclared permutation count and seed. Account for unequal sample size and covariate imbalance; permutation labels must be exchangeable.

## Validation

- report retained taxa/samples, prevalence filter, estimator, normalization/zero handling, sparsification, seed, and dependency versions;
- bootstrap or repeat estimation to assess edge/module/hub stability;
- inspect connected components and sensitivity to filtering/tuning;
- adjust network-comparison tests for multiplicity;
- export edge signs/weights and uncertainty, not only a plot.

## Analytical thinking

Edges are conditional or marginal statistical associations depending on the estimator—not direct interactions, metabolite exchange, or causality. Hubs are tuning- and sampling-dependent. Compositional correction does not remove confounding, habitat filtering, batch effects, or latent-variable bias.

## Source

- https://github.com/stefpeschel/NetCoMi
