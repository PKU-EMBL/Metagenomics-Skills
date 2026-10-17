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
BiocManager::install("phyloseq")
library(phyloseq)
# ps <- phyloseq(otu_table(...), sample_data(...), tax_table(...), phy_tree(...))
# plot_bar / plot_ordination / transform_sample_counts — see vignettes
```

## Decision tree

```text
R microbiome data structure / classic plots?
├─ phyloseq object + ggplot2 → phyloseq
├─ Modular R6 paper workflow → microeco
├─ DA models → ancombc / maaslin2
└─ Networks → spieceasi / sparcc
```

## Related skills

`research-analysis` · `microeco` · `ancombc` · `maaslin2` · `spieceasi` ·
`visualization` · `tool-selection`
