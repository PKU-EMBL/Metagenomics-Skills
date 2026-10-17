---
name: microeco
description: >
  microeco — R package for modular microbiome downstream analysis and publication
  figures (diversity, composition, differential tests, networks, machine learning
  helpers). Use for end-to-end stats/plotting after MetaPhlAn/ Kraken/HUMAnN-style
  tables. Protocol: Nature Protocols 2026. Multivariable DA with covariates → maaslin2.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "microeco, R, diversity, visualization, phyloseq-alternative, research-analysis"
  metagenomics.upstream: "https://github.com/ChiLiubio/microeco"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "R API reviewed against upstream; not executed here"
---

# microeco

Upstream: [ChiLiubio/microeco](https://github.com/ChiLiubio/microeco) ·
Tutorial: https://chiliubio.github.io/microeco_tutorial/ ·
file2meco helpers: https://github.com/ChiLiubio/file2meco

## Citation

Liu, C. *et al.* A workflow for statistical analysis and visualization of
microbiome omics data using the R microeco package. *Nat. Protoc.* **21**,
1300–1324 (2026). https://doi.org/10.1038/s41596-025-01239-4

Liu, C. *et al.* microeco: an R package for data mining in microbial community
ecology. *FEMS Microbiol. Ecol.* **97**, fiaa255 (2021).
https://doi.org/10.1093/femsec/fiaa255

microeco 2: Liu, C. *et al.* *iMeta* **5**, e70132 (2026).
https://doi.org/10.1002/imt2.70132

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

microeco provides **R6 modular classes** for preprocessing, alpha/beta diversity,
composition plots, differential abundance, networks, and related figures —
a practical paper-figure stack for shotgun-derived community tables. Import via
file2meco when starting from MetaPhlAn/HUMAnN/QIIME-style outputs.

For covariate-heavy epidemiology-style models, still run / report `maaslin2`.
Pin R + microeco version; save scripts for reproducibility.

## How to run

```r
library(microeco)
otu <- read.delim("counts.tsv", row.names = 1, check.names = FALSE)
tax <- read.delim("taxonomy.tsv", row.names = 1, check.names = FALSE)
meta <- read.delim("metadata.tsv", row.names = 1, check.names = FALSE)
stopifnot(setequal(colnames(otu), rownames(meta)), all(rownames(otu) %in% rownames(tax)))
meta <- meta[colnames(otu), , drop = FALSE]
tax <- tax[rownames(otu), , drop = FALSE]
d <- microtable$new(otu_table = otu, tax_table = tax,
                    sample_table = meta, auto_tidy = FALSE)
d$tidy_dataset()
d$cal_abund()
d$cal_alphadiv(PD = FALSE)
d$cal_betadiv(unifrac = FALSE)
dir.create("result/microeco", recursive = TRUE, showWarnings = FALSE)
saveRDS(d, "result/microeco/microtable.rds")
write.csv(d$alpha_diversity, "result/microeco/alpha_diversity.csv")
writeLines(capture.output(sessionInfo()), "result/microeco/sessionInfo.txt")
```

## Decision tree

```text
Need R diversity + paper figures?
├─ Modular exploration / plots → microeco
├─ Multivariable associations → maaslin2
├─ Classic LDA biomarkers → lefse
└─ Stage checklist only → visualization
```

## Validation, recovery, and provenance

Before object creation, require unique IDs, exact sample alignment, explicit feature orientation and scale, non-negative finite values, taxonomy-row coverage, and declared handling of unclassified features. After `tidy_dataset()`, compare retained samples/features to the original manifest. Validate distance/diversity assumptions, group sizes, permutation strata, multiplicity correction and plotting data; never treat an attractive ordination or network edge as a tested mechanism.

Save imported tables, filtering/normalization code, serialized objects, test tables—not plots alone—random seeds, package lockfile and `sessionInfo()`. Keep exploratory and confirmatory analyses labelled and use `$maaslin2`, `$ancombc`, `$permanova`, or `$netcomi` where their inferential contracts fit. Diversity and co-occurrence summarize the chosen representation; they do not establish causality or interaction.

## Related skills

`research-analysis` · `phyloseq` · `visualization` · `maaslin2` · `ancombc` ·
`lefse` · `spieceasi` · `sparcc` · `metaphlan` · `kraken2` · `humann` ·
`study-design` · `tool-selection`
