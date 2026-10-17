---
name: stamp
description: >
  STAMP — Statistical Analysis of Metagenomic Profiles; GUI for taxonomic / functional
  profile tests with effect sizes, CIs, and publication plots (extended error bars, PCA,
  heatmaps). Use for interactive exploratory DA and classic two-group/multi-group tests.
  Prefer MaAsLin2/ANCOM-BC for covariate-heavy designs.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "STAMP, GUI, differential-abundance, effect-size, metagenomics"
  metagenomics.upstream: "https://github.com/dparks1134/STAMP"
  metagenomics.stage: "report"
---

# STAMP

Upstream: [dparks1134/STAMP](https://github.com/dparks1134/STAMP) ·
https://beikolab.cs.dal.ca/software/STAMP

## Citation

Parks, D. H., Tyson, G. W., Hugenholtz, P. & Beiko, R. G. STAMP: statistical
analysis of taxonomic and functional profiles. *Bioinformatics* **30**,
3123–3124 (2014). https://doi.org/10.1093/bioinformatics/btu494

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

STAMP emphasizes **effect sizes + confidence intervals** alongside p-values and
offers a GUI for profile exploration. Good for teaching, quick two-group
figures, and legacy Methods. For multivariable / longitudinal designs prefer
`maaslin2` or `ancombc`. Pin STAMP version, test (e.g. Welch), and multiple-test
correction.

## How to run

```bash
# install from GitHub Releases / pip package "stamp" per upstream
# launch GUI; load profile + metadata tables (QIIME/HUMAnN-style exports)
# export extended error-bar plots for features passing filters
```

## Decision tree

```text
Exploratory / GUI profile stats?
├─ Yes → stamp
├─ Covariates / mixed models → maaslin2
├─ Compositional bias correction → ancombc
└─ Scripted R figures → microeco / phyloseq
```

## Related skills

`research-analysis` · `maaslin2` · `ancombc` · `lefse` · `microeco` ·
`visualization` · `tool-selection`
