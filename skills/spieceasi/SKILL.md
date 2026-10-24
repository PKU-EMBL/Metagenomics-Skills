---
name: spieceasi
description: >
  SPIEC-EASI — Sparse Inverse Covariance Estimation for Ecological Association
  Inference; compositionally robust microbial network inference (MB / glasso) with
  optional SparCC. Use for conditional association networks from count / relative
  abundance tables. Route via research-analysis; pure SparCC correlations → sparcc.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "SPIEC-EASI, SpiecEasi, network, glasso, microbiome, compositionality"
  metagenomics.upstream: "https://github.com/zdk123/SpiecEasi"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "spiec.easi/StARS extraction API checked against current upstream README; not executed here"
---

# SPIEC-EASI (SpiecEasi)

Upstream: [zdk123/SpiecEasi](https://github.com/zdk123/SpiecEasi)

## Citation

Kurtz, Z. D. *et al.* Sparse and compositionally robust inference of microbial
ecological networks. *PLoS Comput. Biol.* **11**, e1004226 (2015).
https://doi.org/10.1371/journal.pcbi.1004226

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

SPIEC-EASI infers **sparse graphical models** (neighborhood selection or
glasso) after compositional transforms — edges closer to conditional dependence
than raw correlations. Includes a `sparcc()` implementation for comparison.
Needs enough samples relative to taxa; filter rare features; pin method
(`mb`/`glasso`), λ path, and StARS/pulsar settings.

Networks are hypotheses — not proven interactions.

## How to run

Input is a raw count TSV with samples in rows, features in columns, and sample IDs
in column 1. This template exports the selected graph and fitted object.

```r
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
input <- args[[1]]; out <- args[[2]]
stopifnot(file.exists(input), !dir.exists(out), !file.exists(out))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
log_con <- file(file.path(out, "spieceasi.log"), open = "wt")
sink(log_con, type = "output"); sink(log_con, type = "message")
on.exit({sink(type = "message"); sink(type = "output"); close(log_con)}, add = TRUE)

library(SpiecEasi)
counts <- as.matrix(read.delim(input, row.names = 1, check.names = FALSE))
stopifnot(!anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)),
          is.numeric(counts), all(is.finite(counts)), all(counts >= 0),
          all(abs(counts - round(counts)) < 1e-8), nrow(counts) >= 20)
min_samples <- max(5L, ceiling(0.10 * nrow(counts)))
keep <- colSums(counts > 0) >= min_samples & colSums(counts) > 0
write.table(data.frame(feature = colnames(counts), retained = keep,
                       prevalence = colMeans(counts > 0)),
            file.path(out, "feature-filter.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
counts <- counts[, keep, drop = FALSE]
stopifnot(ncol(counts) >= 2L, all(rowSums(counts) > 0))
method <- Sys.getenv("SPIECEASI_METHOD", "mb")
stopifnot(method %in% c("mb", "glasso"))
seed <- as.integer(Sys.getenv("SPIECEASI_SEED", "1729"))
threads <- as.integer(Sys.getenv("THREADS", "1"))
stopifnot(is.finite(seed), is.finite(threads), threads >= 1L)
set.seed(seed)
fit <- spiec.easi(counts, method = method, lambda.min.ratio = 1e-2,
                  nlambda = 20, sel.criterion = "stars",
                  pulsar.select = TRUE,
                  pulsar.params = list(rep.num = 50, seed = seed,
                                       ncores = threads))
adj <- as.matrix(getRefit(fit))
dimnames(adj) <- list(colnames(counts), colnames(counts))
if (method == "mb") {
  weight <- as.matrix(symBeta(getOptBeta(fit), mode = "maxabs"))
} else {
  weight <- cov2cor(as.matrix(getOptCov(fit)))
}
weight[adj == 0] <- 0; diag(weight) <- 0
idx <- which(upper.tri(adj) & adj != 0, arr.ind = TRUE)
edges <- data.frame(feature1 = rownames(adj)[idx[, 1]],
                    feature2 = colnames(adj)[idx[, 2]],
                    weight = weight[idx])
write.table(adj, file.path(out, "selected-adjacency.tsv"), sep = "\t",
            quote = FALSE, col.names = NA)
write.table(edges, file.path(out, "selected-edges.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
saveRDS(fit, file.path(out, "spieceasi-fit.rds"))
writeLines(sprintf("method=%s\nseed=%d\nmin_samples=%d", method, seed,
                   min_samples), file.path(out, "settings.txt"))
capture.output(sessionInfo(), file = file.path(out, "sessionInfo.txt"))
stopifnot(file.info(file.path(out, "selected-adjacency.tsv"))$size > 0,
          file.info(file.path(out, "spieceasi-fit.rds"))$size > 0)
```

Run as `Rscript run_spieceasi.R counts.tsv fresh_output_dir`. Increase StARS
replicates and explore λ/filter sensitivity for final analyses; compare `mb` and
`glasso` only through separately labeled fits.

## Decision tree

```text
Network inference need?
├─ Conditional sparse network → spieceasi
├─ SparCC correlations only → sparcc
├─ Group DA → ancombc / maaslin2
└─ Exploratory plots → microeco / phyloseq
```

## Validation, recovery, and provenance

Require full selected adjacency/edge tables, fitted object, filter/settings
files, log and session information. Inspect sample-to-feature ratio, StARS path
and selected instability, graph density/degree, method and λ sensitivity,
influential samples, batch/confounding, zero/prevalence filters, component
structure, and edge
stability under resampling. Preserve zero-edge outcomes as valid results.

Use a fresh output after any input/filter/seed/method/package change. Record raw
count semantics/checksum, cohort, SpiecEasi/pulsar/R versions, seed, method,
λ path, repetitions/cores, filters, script/log, fitted object, graph extraction
and visualization rules. Conditional associations are hypotheses, not direct,
directional, causal, or experimentally validated interactions.

## Related skills

`sparcc` · `research-analysis` · `microeco` · `phyloseq` · `maaslin2` ·
`tool-selection`
