---
name: feast
description: >-
  Estimate microbial source contributions to sink communities with FEAST from integer sample-by-feature counts and Env/SourceSink/id metadata. Use when source sets, rarefaction depth, unknown-source contribution, random seed, and validation with held-out or synthetic mixtures are explicit.
license: MIT
compatibility: Requires R, FEAST 0.1.0 upstream package and dependencies, integer counts, and matched source/sink metadata.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "feast,source-tracking,source-sink,expectation-maximization,contamination"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.1.0 upstream snapshot"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; template not executed here"
---

# FEAST

FEAST uses expectation maximization to estimate sampled-source and unknown-source proportions for each sink.

## Inputs

Counts must be **samples by features**, integer and non-negative. Metadata row names are sample IDs and must contain exactly meaningful values for:

- `Env`: source environment label;
- `SourceSink`: `Source` or `Sink`;
- `id`: sink/source-set identifier when each sink has distinct candidate sources.

Set `different_sources_flag=0` when every sink shares all sources; set it to `1` when `id` assigns distinct source sets. Do not convert arbitrary relative abundances to integers solely to satisfy the API.

## Reproducible run

```bash
cat > run_feast.R <<'RS'
suppressPackageStartupMessages(library(FEAST))
args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==3)
C <- read.delim(args[1], row.names=1, check.names=FALSE)
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(all(c("Env","SourceSink","id") %in% names(meta)))
stopifnot(!anyDuplicated(rownames(C)), !anyDuplicated(rownames(meta)))
stopifnot(setequal(rownames(C), rownames(meta)))
meta <- meta[rownames(C),,drop=FALSE]
stopifnot(all(is.finite(as.matrix(C))), all(C>=0),
          all(abs(as.matrix(C)-round(as.matrix(C)))<1e-8))
stopifnot(any(tolower(meta$SourceSink)=="source"),
          any(tolower(meta$SourceSink)=="sink"))
dir.create(args[3], recursive=TRUE, showWarnings=FALSE)
set.seed(20261018)
res <- FEAST(C=C, metadata=meta, EM_iterations=1000, COVERAGE=NULL,
             different_sources_flag=0, dir_path=normalizePath(args[3]),
             outfile="feast")
outfile <- file.path(args[3], "feast_source_contributions_matrix.txt")
stopifnot(file.exists(outfile), file.info(outfile)$size>0)
saveRDS(res, file.path(args[3], "feast_result.rds"))
RS
Rscript run_feast.R counts_samples_by_features.tsv feast_metadata.tsv feast_out \
  >feast.stdout.log 2>feast.stderr.log
[[ -s feast_out/feast_source_contributions_matrix.txt && \
   -s feast_out/feast_result.rds ]] || exit 3
```

With `COVERAGE=NULL`, upstream chooses a minimum depth within each sink/source group and rarefies. Record the realized depth from logs/code and assess stochastic sensitivity. Use `different_sources_flag=1` only after validating `id` assignments.

## Validation

- confirm every sink has an output row and appropriate source columns;
- account for `NA` where a source was not offered to a sink;
- verify each sink's non-NA contributions, including `Unknown`, sum to approximately one;
- repeat seeds/subsampling and bootstrap source samples;
- run known sources as pseudo-sinks and test synthetic mixtures;
- inspect batch and negative-control sources explicitly.

## Recovery and provenance

FEAST changes the working directory internally and writes files, so always use a dedicated output directory. Rerun cleanly after metadata/depth changes. Preserve FEAST commit/package metadata, dependency versions, seed, count/metadata checksums, output matrix, and RDS object.

## Analytical thinking

Source contributions are relative model allocations among supplied sources plus unknown. Closely related source communities may be non-identifiable, and omitted sources can redistribute estimates. FEAST does not prove transfer, infection, or temporal direction.

## Source

- https://github.com/cozygene/FEAST
