---
name: research-analysis
description: >
  Route downstream research analysis for shotgun metagenomics: QC report
  aggregation (MultiQC), diversity and publication figures (visualization,
  microeco), differential abundance / multivariable associations (MaAsLin2/3,
  LEfSe), and Methods hygiene (normalization, batch, FDR). Use after taxonomy
  or function tables exist — not for assembly/binning itself. Child skills:
  visualization, microeco, maaslin2, lefse, multiqc. Upstream design via
  study-design; pipelines via metagenomics-workflow.
license: MIT
category: orchestration
tags: [research-analysis, statistics, visualization, diversity, differential-abundance, MultiQC]
stage: report
---

# Research analysis (stats · figures · reports)

Downstream **scientific delivery** after profiling/annotation tables exist:
aggregated QC, alpha/beta diversity, composition plots, differential features,
and figure labeling for papers. Does **not** replace `mag-qc` or taxonomy tools.

## Analytical thinking

| Claim / deliverable | Prefer | Do not treat as |
|---------------------|--------|-----------------|
| Multi-tool QC HTML report | `multiqc` | Biological group test |
| Diversity + composition figures (flexible R) | `microeco` (± `visualization`) | Causal mechanism |
| Multivariable associations (covariates, longitudinal) | `maaslin2` (MaAsLin2/3) | Unadjusted LEfSe alone |
| Classic biomarker / LDA effect size | `lefse` | Modern multivariable default |
| Figure checklist by pipeline stage | `visualization` | Table generation |
| Interactive MAG exploration | `anvio` | Cohort DA tables |
| Study strata / batch design | `study-design` | Post-hoc p-hacking |

Hard rules:

1. Every figure: **stage + method + DB/software version + normalization**
2. Inspect batch / library size before group tests
3. Report rarefaction (if used), transform, test, and **FDR/FWER**
4. Do not mix MetaPhlAn, Kraken, and MAG relative abundances unlabeled
5. Differential hits are associations — not validated biomarkers

## Decision tree

```text
Research downstream need?
│
├─ Aggregate FastQC/fastp/… reports → multiqc
├─ Alpha/beta/composition/heatmaps (R workflow) → microeco
├─ Figure recipe checklist by stage → visualization
├─ Multivariable DA / metadata associations → maaslin2
├─ Classic class biomarkers (LDA) → lefse
├─ Interactive bins / profiles → anvio
├─ Still designing strata / n → study-design
└─ Unsure → this hub
```

## Typical order

```text
study-design → QC (+ multiqc)
  → taxonomy / function tables
  → microeco / visualization (explore)
  → maaslin2 (± lefse)
  → Methods: pin versions, transforms, FDR
```

## Related skills

`visualization` · `microeco` · `maaslin2` · `lefse` · `multiqc` ·
`study-design` · `metaphlan` · `kraken2` · `humann` · `anvio` ·
`metagenomics-workflow` · `tool-selection`
