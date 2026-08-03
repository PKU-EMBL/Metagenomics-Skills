---
name: lefse
description: >
  LEfSe — Linear discriminant analysis Effect Size for metagenomic biomarker
  discovery between classes (taxa, genes, pathways). Use for classic
  LDA-style biomarkers and cladograms; prefer MaAsLin2/3 when many covariates
  or longitudinal designs are required. Upstream:
  https://github.com/SegataLab/lefse · bioBakery docs. Route via
  research-analysis.
license: MIT
category: evaluation
tags: [LEfSe, biomarker, LDA, differential-abundance, bioBakery]
upstream: https://github.com/SegataLab/lefse
stage: report
---

# LEfSe

Upstream: [SegataLab/lefse](https://github.com/SegataLab/lefse) ·
https://huttenhower.sph.harvard.edu/lefse/

## Citation

Segata, N. *et al.* Metagenomic biomarker discovery and explanation.
*Genome Biol.* **12**, R60 (2011).
https://doi.org/10.1186/gb-2011-12-6-r60

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

LEfSe couples nonparametric tests with **LDA effect size** and (optionally)
cladogram displays — widely used in papers but sensitive to compositionality
and limited for complex multivariable designs. Prefer `maaslin2` for modern
covariate-adjusted analyses; LEfSe remains useful for simple class contrasts
and familiar LDA plots.

Pin LDA cutoff, multiclass strategy, and input table type (relative abundances).

## How to run

```bash
# conda install -c bioconda lefse   # or biobakery channel — verify
# format input table per Galaxy/tutorial (class + subclass rows)
# lefse_format_input.py … ; run_lefse.py … ; lefse_plot_*.py …
```

Follow the installed bioBakery tutorial for exact script names.

## Decision tree

```text
Biomarker discovery?
├─ Simple classes / LDA plots → lefse
├─ Covariates / mixed models → maaslin2
└─ Broad exploration → microeco
```

## Related skills

`research-analysis` · `maaslin2` · `microeco` · `visualization` ·
`metaphlan` · `humann` · `tool-selection`
