---
name: sparcc
description: >
  SparCC — Sparse Correlations for Compositional data; infer taxon–taxon correlations
  from relative abundances without naive Pearson on compositions. Use for correlation
  networks on microbiome tables. convenient R implementation inside SpiecEasi
  (sparcc()). Route via research-analysis; conditional networks → spieceasi.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "SparCC, network, correlation, compositionality, microbiome"
  metagenomics.upstream: "https://bitbucket.org/yonatanf/sparcc"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "SpiecEasi sparcc/sparccboot API checked against current source; not executed here"
---

# SparCC

Upstream (original): https://bitbucket.org/yonatanf/sparcc ·
R helper often via [SpiecEasi](https://github.com/zdk123/SpiecEasi) `sparcc()`

## Citation

Friedman, J. & Alm, E. J. Inferring correlation networks from genomic survey
data. *PLoS Comput. Biol.* **8**, e1002687 (2012).
https://doi.org/10.1371/journal.pcbi.1002687

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Relative abundances are **compositional** — Pearson/Spearman on proportions
yields spurious correlations. SparCC estimates correlations under a sparse
assumption. Correlation ≠ direct ecological interaction; for conditional
independence graphs prefer `spieceasi`. Filter rare taxa; report bootstrap /
thresholding if used.

## How to run

Input is a raw count TSV with samples in rows, features in columns, and sample IDs
in column 1. Filter rules and edge thresholds must be chosen before inspection.

```r
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
input <- args[[1]]; out <- args[[2]]
stopifnot(file.exists(input), !dir.exists(out), !file.exists(out))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
log_con <- file(file.path(out, "sparcc.log"), open = "wt")
sink(log_con, type = "output"); sink(log_con, type = "message")
on.exit({sink(type = "message"); sink(type = "output"); close(log_con)}, add = TRUE)

library(SpiecEasi)
counts <- as.matrix(read.delim(input, row.names = 1, check.names = FALSE))
stopifnot(!anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)),
          is.numeric(counts), all(is.finite(counts)), all(counts >= 0),
          all(abs(counts - round(counts)) < 1e-8), nrow(counts) >= 10)
min_samples <- max(5L, ceiling(0.10 * nrow(counts)))
keep <- colSums(counts > 0) >= min_samples & colSums(counts) > 0
write.table(data.frame(feature = colnames(counts), retained = keep,
                       prevalence = colMeans(counts > 0)),
            file.path(out, "feature-filter.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
counts <- counts[, keep, drop = FALSE]
stopifnot(ncol(counts) >= 2L, all(rowSums(counts) > 0))
seed <- as.integer(Sys.getenv("SPARCC_SEED", "1729"))
boot_n <- as.integer(Sys.getenv("SPARCC_BOOTSTRAPS", "1000"))
threads <- as.integer(Sys.getenv("THREADS", "1"))
stopifnot(boot_n >= 100L, threads >= 1L)
set.seed(seed)
boot <- sparccboot(counts, R = boot_n, ncpus = threads)
pv <- pval.sparccboot(boot)
idx <- which(upper.tri(diag(ncol(counts))), arr.ind = TRUE)
edges <- data.frame(feature1 = colnames(counts)[idx[, 1]],
                    feature2 = colnames(counts)[idx[, 2]],
                    correlation = pv$cors, p_value = pv$pvals)
edges$q_value <- p.adjust(edges$p_value, method = "BH")
write.table(edges, file.path(out, "all-edges.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE, na = "NA")
saveRDS(boot, file.path(out, "sparcc-bootstrap.rds"))
writeLines(sprintf("seed=%d\nbootstraps=%d\nmin_samples=%d",
                   seed, boot_n, min_samples), file.path(out, "settings.txt"))
capture.output(sessionInfo(), file = file.path(out, "sessionInfo.txt"))
stopifnot(file.info(file.path(out, "all-edges.tsv"))$size > 0,
          file.info(file.path(out, "sparcc-bootstrap.rds"))$size > 0)
```

Run as `Rscript run_sparcc.R counts.tsv fresh_output_dir`. The original Python
pipeline remains valid only when its exact tag, bootstrapping procedure, and
output semantics are recorded separately.

## Decision tree

```text
Microbial association network?
├─ Compositional correlations → sparcc
├─ Sparse conditional networks → spieceasi
├─ DA between groups → ancombc / maaslin2
└─ Plot networks in R suite → microeco (± igraph)
```

## Validation, recovery, and provenance

Require full edge results, filter table, bootstrap object, settings, logs and
session information. Inspect sample/feature ratio, prevalence, library-size and batch/confounding
structure, unstable/NA P values, sign/magnitude distributions, threshold and FDR
sensitivity, influential samples, and network stability under filtering. Retain
all edges; create thresholded graphs as derived artifacts.

Use a fresh output after any input/filter/seed/package change. Record count-table
semantics/checksum, metadata cohort, SpiecEasi/boot/R versions, seed, iterations,
bootstrap count, cores, filters, command/script, logs, full results and graph
rules. SparCC edges are compositional associations, not direct interactions,
directionality, or validated ecological mechanisms.

## Related skills

`spieceasi` · `research-analysis` · `microeco` · `phyloseq` · `maaslin2` ·
`tool-selection`
