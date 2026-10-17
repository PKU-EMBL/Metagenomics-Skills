---
name: decontam
description: >-
  Identify likely contaminant features in microbiome count data using the R decontam package's negative-control prevalence, DNA-concentration frequency, combined, or batch-aware models. Use when controls and sample metadata support statistical contaminant flagging; not for automatic universal blacklist subtraction.
license: MIT
compatibility: Requires R, decontam 1.13+ or a pinned Bioconductor release, feature counts, and matched metadata.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "decontam,contamination,negative-controls,prevalence,frequency,r"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.13.0 upstream snapshot"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; not executed here"
---

# decontam

`decontam` flags features whose frequency declines with input DNA concentration and/or whose prevalence is higher in negative controls.

## Inputs

- integer/non-negative feature table with features as rows and samples as columns;
- metadata with exact sample IDs;
- `is_negative` for extraction/library blanks and/or positive DNA concentration;
- optional batch variable when contaminant profiles differ by extraction or sequencing batch.

Do not run prevalence mode without true negative controls. Do not use post-library read depth as a substitute for input DNA concentration.

## Preflight

```bash
Rscript -e 'stopifnot(requireNamespace("decontam", quietly=TRUE)); packageVersion("decontam"); sessionInfo()'
```

Archive the package version, metadata, raw counts, and threshold. Use `$contamination-control` to define controls and sensitivity analyses first.

## Reproducible prevalence run

```bash
cat > run_decontam.R <<'RS'
suppressPackageStartupMessages(library(decontam))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 3)
counts <- read.delim(args[1], row.names=1, check.names=FALSE)
meta <- read.delim(args[2], row.names=1, check.names=FALSE)
stopifnot(!anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)))
stopifnot(!anyDuplicated(rownames(meta)), setequal(colnames(counts), rownames(meta)))
counts <- counts[, rownames(meta), drop=FALSE]
stopifnot(all(is.finite(as.matrix(counts))), all(counts >= 0))
stopifnot("is_negative" %in% colnames(meta))
neg <- as.logical(meta$is_negative)
stopifnot(!anyNA(neg), any(neg), any(!neg))
# decontam expects samples x features for a plain matrix.
res <- isContaminant(t(counts), method="prevalence", neg=neg,
                     threshold=0.10, detailed=TRUE)
out <- cbind(feature_id=rownames(res), res)
write.table(out, args[3], sep="\t", quote=FALSE, row.names=FALSE)
stopifnot(nrow(out) == nrow(counts), !anyNA(out$contaminant))
cat("features", nrow(out), "flagged", sum(out$contaminant), "\n")
RS
Rscript run_decontam.R counts.tsv metadata.tsv decontam_prevalence.tsv \
  >decontam.stdout.log 2>decontam.stderr.log
[[ -s decontam_prevalence.tsv ]] || exit 3
```

For frequency mode use `method="frequency", conc=meta$dna_concentration`; all values must be positive and measured before library normalization. For combined evidence pass both `neg` and `conc` and choose a documented combination mode. Use `batch=meta$extraction_batch` only after confirming each modeled batch has adequate controls/data.

## Validate and interpret

- plot blank versus biological prevalence and `plot_frequency` for representative flagged and retained features;
- tabulate flagged features by abundance, batch, taxonomy, and control type;
- verify known positive-control members are not systematically removed;
- repeat at defensible thresholds (the upstream default is 0.1; 0.5 in prevalence mode has a specific, more aggressive interpretation);
- rerun primary biological analyses with and without flagged features.

Keep `decontam_prevalence.tsv` as evidence and create a separate reviewed decision table. A `TRUE` flag is a statistical classification, not proof of reagent origin.

## Failure recovery

Zero-sum samples and mismatched orientation can silently invalidate analyses; stop and repair inputs rather than transposing until a command runs. If a batch lacks controls, do not force a batch-specific model. Preserve all original features so decisions are reversible.

## Analytical thinking

Low-biomass true organisms can resemble contaminants, and contaminants can be common in real samples. Removal must combine model evidence, control behavior, batch structure, biology, and sensitivity analysis. Never apply a taxon blacklist across studies.

## Sources

- Documentation: https://benjjneb.github.io/decontam/
- Upstream: https://github.com/benjjneb/decontam
