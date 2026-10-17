---
name: lefse
description: >
  LEfSe — Linear discriminant analysis Effect Size for metagenomic biomarker discovery
  between classes (taxa, genes, pathways). Use for classic LDA-style biomarkers and
  cladograms; prefer MaAsLin2/3 when many covariates or longitudinal designs are
  required.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "LEfSe, biomarker, LDA, differential-abundance, bioBakery"
  metagenomics.upstream: "https://github.com/SegataLab/lefse"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.upstream-version: "snapshot ff93a8b"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Bioconda entry points reviewed against upstream example; not executed here"
---

# LEfSe

Upstream: [SegataLab/lefse](https://github.com/SegataLab/lefse) ·
https://huttenhower.sph.harvard.edu/lefse/

## Citation

Segata, N. *et al.* Metagenomic biomarker discovery and explanation.
*Genome Biol.* **12**, R60 (2011).
https://doi.org/10.1186/gb-2011-12-6-r60

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

LEfSe couples nonparametric tests with **LDA effect size** and (optionally)
cladogram displays — widely used in papers but sensitive to compositionality
and limited for complex multivariable designs. Prefer `maaslin2` for modern
covariate-adjusted analyses; LEfSe remains useful for simple class contrasts
and familiar LDA plots.

Pin LDA cutoff, multiclass strategy, and input table type (relative abundances).

## Inputs and run

Input is LEfSe's transposed text format: metadata rows precede feature rows and sample columns must align exactly. This example declares class row 1 and no subclass/subject; change those indices only after inspecting the file.

```bash
set -euo pipefail
conda install -c conda-forge -c bioconda lefse
[[ -s lefse_input.tsv ]] || exit 2
mkdir -p result/lefse
lefse_format_input.py lefse_input.tsv result/lefse/input.in \
  -c 1 -s -1 -u -1 -o 1000000
lefse_run.py result/lefse/input.in result/lefse/results.res
lefse_plot_res.py result/lefse/results.res result/lefse/effects.png
lefse_plot_cladogram.py result/lefse/results.res \
  result/lefse/cladogram.png --format png
```

Predeclare alpha, multiclass strategy and LDA threshold (`lefse_run.py -h`). Use subclass/subject rows only when their meaning matches LEfSe's restricted design—not as a substitute for a mixed model.

## Decision tree

```text
Biomarker discovery?
├─ Simple classes / LDA plots → lefse
├─ Covariates / mixed models → maaslin2
└─ Broad exploration → microeco
```

## Validation, recovery, and provenance

Validate sample/feature IDs, class sizes, hierarchy delimiters, scale/non-negativity and the exact formatted matrix. Require a completed result file even when no feature passes; inspect all tested features, class direction, p-values, LDA scores and sensitivity to prevalence/normalization. Cross-check primary findings with a compositionally aware or multivariable method.

Use a fresh result path after input/options change. Record LEfSe/R versions, full formatting/run commands, input/checksums, metadata levels, normalization, alpha/LDA/multiclass options and exported source/result tables—not images alone. LEfSe biomarkers are exploratory associations, not causal effects or absolute abundance.

## Related skills

`research-analysis` · `maaslin2` · `microeco` · `visualization` ·
`metaphlan` · `humann` · `tool-selection`
