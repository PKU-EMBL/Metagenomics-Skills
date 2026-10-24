---
name: phyloseq
description: >
  phyloseq — Bioconductor R package for storing and analyzing microbiome census data
  (OTU/ASV tables, taxonomy, phylogeny, sample data) with ggplot2 graphics. Use as a
  data container and classic analysis API; many DA/network tools accept phyloseq
  objects. Route via research-analysis; modular paper workflows also via microeco.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "phyloseq, Bioconductor, R, microbiome, diversity, visualization"
  metagenomics.upstream: "https://github.com/joey711/phyloseq"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "object-construction and ID reconciliation template statically reviewed; not executed here"
---

# phyloseq

Upstream: [joey711/phyloseq](https://github.com/joey711/phyloseq) ·
Bioconductor: https://bioconductor.org/packages/phyloseq/

## Citation

McMurdie, P. J. & Holmes, S. phyloseq: An R Package for Reproducible Interactive
Analysis and Graphics of Microbiome Census Data. *PLoS ONE* **8**, e61217
(2013). https://doi.org/10.1371/journal.pone.0061217

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

phyloseq is the long-standing **R data class + plotting** stack for microbiome
tables. Use it to organize ASV/species × sample matrices with taxonomy and
trees, then pass objects into `ancombc`, vegan ordinations, or custom ggplot2.
For a more modular modern paper workflow, also consider `microeco` (can coexist).

Pin Bioconductor release. Avoid double rarefaction without stating rationale.

## How to run

```r
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 4L)
counts_path <- args[[1]]; taxonomy_path <- args[[2]]
metadata_path <- args[[3]]; out <- args[[4]]
stopifnot(file.exists(counts_path), file.exists(taxonomy_path),
          file.exists(metadata_path), !dir.exists(out), !file.exists(out))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
log_con <- file(file.path(out, "build.log"), open = "wt")
sink(log_con, type = "output"); sink(log_con, type = "message")
on.exit({sink(type = "message"); sink(type = "output"); close(log_con)}, add = TRUE)

library(phyloseq)
counts <- as.matrix(read.delim(counts_path, row.names = 1, check.names = FALSE))
tax <- as.matrix(read.delim(taxonomy_path, row.names = 1, check.names = FALSE))
meta <- read.delim(metadata_path, row.names = 1, check.names = FALSE)
stopifnot(!anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)),
          !anyDuplicated(rownames(tax)), !anyDuplicated(rownames(meta)),
          is.numeric(counts), all(is.finite(counts)), all(counts >= 0),
          all(abs(counts - round(counts)) < 1e-8))
stopifnot(setequal(colnames(counts), rownames(meta)))
stopifnot(all(rownames(counts) %in% rownames(tax)))
meta <- meta[colnames(counts), , drop = FALSE]
tax <- tax[rownames(counts), , drop = FALSE]
ps <- phyloseq(otu_table(counts, taxa_are_rows = TRUE),
               sample_data(meta), tax_table(tax))
stopifnot(nsamples(ps) == nrow(meta), ntaxa(ps) == nrow(counts))
saveRDS(ps, file.path(out, "phyloseq.rds"))
write.table(data.frame(sample_id = sample_names(ps), status = "matched"),
            file.path(out, "sample-id-join.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
capture.output(sessionInfo(), file = file.path(out, "sessionInfo.txt"))
stopifnot(file.info(file.path(out, "phyloseq.rds"))$size > 0,
          inherits(readRDS(file.path(out, "phyloseq.rds")), "phyloseq"))
```

Run the saved script as `Rscript build_phyloseq.R counts.tsv taxonomy.tsv
metadata.tsv fresh_output_dir`, redirecting process stdout/stderr if your scheduler
does not retain them. Install a pinned Bioconductor/phyloseq release outside the
analysis script. Add a tree only after reconciling tip IDs; transformations must
create named derived objects rather than replace raw counts.

## Decision tree

```text
R microbiome data structure / classic plots?
├─ phyloseq object + ggplot2 → phyloseq
├─ Modular R6 paper workflow → microeco
├─ DA models → ancombc / maaslin2
└─ Networks → spieceasi / sparcc
```

## Validation, recovery, and provenance

Audit feature/sample orientation, duplicate/unmatched IDs, integer count status,
zero-sum samples/features, taxonomy rank consistency, tree-tip reconciliation,
and metadata types/missingness. Preserve the raw-count object; name and document
all prevalence filters, agglomeration, transforms, rarefaction, and subsets.

Use a fresh output after any source-table or package change. Archive source
checksums, ID-join report, construction script/log, R/Bioconductor/package
versions, RDS checksum, derived-object lineage, seeds, and figure/model scripts.
A phyloseq object is a container, not evidence that downstream assumptions or
inference are valid.

## Related skills

`research-analysis` · `microeco` · `ancombc` · `maaslin2` · `spieceasi` ·
`visualization` · `tool-selection`
