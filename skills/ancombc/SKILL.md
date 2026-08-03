---
name: ancombc
description: >
  ANCOM-BC / ANCOM-BC2 — compositionally aware differential abundance with
  sampling-fraction bias correction (Bioconductor ANCOMBC). Use when DA must
  account for compositionality and unequal sampling fractions; complements
  MaAsLin2/LEfSe. Upstream: https://github.com/FrederickHuangLin/ANCOMBC
  (Bioconductor ANCOMBC). Route via research-analysis.
license: MIT
category: evaluation
tags: [ANCOM-BC, ANCOM-BC2, differential-abundance, compositionality, Bioconductor]
upstream: https://github.com/FrederickHuangLin/ANCOMBC
stage: report
---

# ANCOM-BC / ANCOM-BC2

Upstream: [FrederickHuangLin/ANCOMBC](https://github.com/FrederickHuangLin/ANCOMBC) ·
Bioconductor: https://bioconductor.org/packages/ANCOMBC/

## Citation

Lin, H. & Peddada, S. D. Analysis of compositions of microbiomes with bias
correction. *Nat. Commun.* **11**, 3514 (2020).
https://doi.org/10.1038/s41467-020-17041-7

ANCOM-BC2: Lin, H. & Peddada, S. D. Multigroup analysis of compositions of
microbiomes with covariate adjustments and repeated measures. *Nat. Methods*
**21**, 83–89 (2024). https://doi.org/10.1038/s41592-023-02092-7

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

ANCOM-BC estimates **sampling fractions**, corrects compositional bias, and
reports taxon-wise effects with CIs and FDR. Prefer when compositionality is a
primary concern. Pin `ancombc` vs `ancombc2`, formula, and prevalence filters.
Often takes phyloseq / TreeSummarizedExperiment-style inputs.

| vs | Prefer ANCOM-BC when |
|----|----------------------|
| `maaslin2` | Explicit sampling-fraction bias correction focus |
| `lefse` | Modern FDR + CI vs classic LDA |
| `stamp` | R/Bioconductor pipeline vs GUI exploratory tests |

## How to run

```r
BiocManager::install("ANCOMBC")
library(ANCOMBC)
# ancombc(...) or ancombc2(...) — follow vignette for object class + formula
```

## Decision tree

```text
Differential abundance?
├─ Bias-corrected compositional DA → ancombc
├─ Multivariable / longitudinal meta-omics → maaslin2
├─ Classic LDA → lefse
└─ GUI exploratory → stamp
```

## Related skills

`research-analysis` · `maaslin2` · `lefse` · `phyloseq` · `microeco` ·
`stamp` · `tool-selection`
