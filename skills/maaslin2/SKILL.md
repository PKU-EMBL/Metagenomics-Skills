---
name: maaslin2
description: >
  MaAsLin2 / MaAsLin3 — multivariable association discovery between metadata and
  meta-omic features (taxonomy, pathways, genes) with filtering, normalization,
  transforms, and FDR control. Use for differential abundance with covariates
  or longitudinal designs. Upstream: https://github.com/biobakery/Maaslin2 and
  https://github.com/biobakery/MaAsLin3. Route via research-analysis. Classic
  LDA biomarkers → lefse; figure workflows → microeco / visualization.
license: MIT
category: evaluation
tags: [MaAsLin2, MaAsLin3, differential-abundance, statistics, bioBakery]
upstream: https://github.com/biobakery/Maaslin2
stage: report
---

# MaAsLin2 / MaAsLin3

Upstream: [biobakery/Maaslin2](https://github.com/biobakery/Maaslin2) ·
[biobakery/MaAsLin3](https://github.com/biobakery/MaAsLin3)

## Citation

Mallick, H. *et al.* Multivariable association discovery in population-scale
meta-omics studies. *PLoS Comput. Biol.* **17**, e1009442 (2021).
https://doi.org/10.1371/journal.pcbi.1009442

MaAsLin 3: Nickols, W. A. *et al.* MaAsLin 3: refining and extending generalized
multivariable linear models for meta-omic association discovery. *Nat. Methods*
(2025). https://doi.org/10.1038/s41592-025-02923-9

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Default for **covariate-adjusted** associations on compositional meta-omics
tables (MetaPhlAn, HUMAnN, MAG abundances, …). Pin normalization/transform,
fixed/random effects, and q-value threshold. MaAsLin3 adds prevalence vs
abundance association framing — cite the version you run.

| vs | Prefer MaAsLin when |
|----|---------------------|
| `lefse` | Multiple covariates / mixed models / modern FDR workflow |
| `microeco` | Need model coefficients vs exploratory diversity suite |

## How to run

```r
# Bioconductor / GitHub install per upstream README for Maaslin2 or MaAsLin3
# library(Maaslin2)  # or Maaslin3
# Maaslin2(input_data, input_metadata, output, fixed_effects = c("phenotype","age"), ...)
```

Do not invent formula syntax — follow the installed package vignette.

## Decision tree

```text
Differential / association analysis?
├─ Covariates / longitudinal → maaslin2 (2 or 3)
├─ Classic two-class LDA biomarkers → lefse
├─ Explore diversity first → microeco
└─ Plot checklist → visualization
```

## Related skills

`research-analysis` · `ancombc` · `lefse` · `stamp` · `microeco` ·
`phyloseq` · `visualization` · `metaphlan` · `humann` · `study-design` ·
`tool-selection`
