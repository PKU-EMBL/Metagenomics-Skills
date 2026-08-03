---
name: sparcc
description: >
  SparCC — Sparse Correlations for Compositional data; infer taxon–taxon
  correlations from relative abundances without naive Pearson on compositions.
  Use for correlation networks on microbiome tables. Original:
  https://bitbucket.org/yonatanf/sparcc; convenient R implementation inside
  SpiecEasi (sparcc()). Route via research-analysis; conditional networks →
  spieceasi.
license: MIT
category: evaluation
tags: [SparCC, network, correlation, compositionality, microbiome]
upstream: https://bitbucket.org/yonatanf/sparcc
stage: report
---

# SparCC

Upstream (original): https://bitbucket.org/yonatanf/sparcc ·
R helper often via [SpiecEasi](https://github.com/zdk123/SpiecEasi) `sparcc()`

## Citation

Friedman, J. & Alm, E. J. Inferring correlation networks from genomic survey
data. *PLoS Comput. Biol.* **8**, e1002687 (2012).
https://doi.org/10.1371/journal.pcbi.1002687

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Relative abundances are **compositional** — Pearson/Spearman on proportions
yields spurious correlations. SparCC estimates correlations under a sparse
assumption. Correlation ≠ direct ecological interaction; for conditional
independence graphs prefer `spieceasi`. Filter rare taxa; report bootstrap /
thresholding if used.

## How to run

```r
# via SpiecEasi (common)
# remotes::install_github("zdk123/SpiecEasi")
library(SpiecEasi)
# sparcc.amgut <- sparcc(counts_matrix)
# threshold abs(Cor) for edges — pin cutoff in Methods
```

Or follow the original SparCC Python/bitbucket pipeline for the installed tag.

## Decision tree

```text
Microbial association network?
├─ Compositional correlations → sparcc
├─ Sparse conditional networks → spieceasi
├─ DA between groups → ancombc / maaslin2
└─ Plot networks in R suite → microeco (± igraph)
```

## Related skills

`spieceasi` · `research-analysis` · `microeco` · `phyloseq` · `maaslin2` ·
`tool-selection`
