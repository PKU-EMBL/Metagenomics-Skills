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
install.packages("microeco")  # or remotes::install_github("ChiLiubio/microeco")
library(microeco)
# build microtable from otu/tax/sample tables — see Nat. Protoc. workflow
# then: alpha / beta / abundance / differential modules + ggplot exports
```

## Decision tree

```text
Need R diversity + paper figures?
├─ Modular exploration / plots → microeco
├─ Multivariable associations → maaslin2
├─ Classic LDA biomarkers → lefse
└─ Stage checklist only → visualization
```

## Related skills

`research-analysis` · `phyloseq` · `visualization` · `maaslin2` · `ancombc` ·
`lefse` · `spieceasi` · `sparcc` · `metaphlan` · `kraken2` · `humann` ·
`study-design` · `tool-selection`
