---
name: research-analysis
description: >
  Route downstream research analysis for shotgun metagenomics: QC reports
  (MultiQC), diversity/figures (visualization, microeco, phyloseq, STAMP),
  differential abundance (MaAsLin2/3, ANCOM-BC, LEfSe), association networks
  (SparCC, SPIEC-EASI), and workflow managers (Nextflow, Snakemake). Use after
  taxonomy/function tables exist. Child skills: visualization, microeco,
  phyloseq, maaslin2, ancombc, lefse, stamp, sparcc, spieceasi, multiqc,
  nextflow, snakemake.
license: MIT
category: orchestration
tags: [research-analysis, statistics, visualization, differential-abundance, network, Nextflow, Snakemake]
stage: report
---

# Research analysis (stats · figures · reports · workflows)

Downstream **scientific delivery** after profiling/annotation tables exist:
QC dashboards, diversity/composition figures, differential abundance, microbial
networks, and reproducible pipeline wrappers. Does **not** replace `mag-qc`.

## Analytical thinking

| Claim / deliverable | Prefer | Do not treat as |
|---------------------|--------|-----------------|
| Multi-tool QC HTML | `multiqc` | Biological DA |
| Modular R paper figures | `microeco` | Causal mechanism |
| Classic R data class / ggplot2 | `phyloseq` | Sole DA method |
| Multivariable associations | `maaslin2` | Unadjusted LEfSe alone |
| Compositional bias-corrected DA | `ancombc` | Network edges |
| Classic LDA biomarkers | `lefse` | Modern multivariable default |
| GUI exploratory profile tests | `stamp` | Covariate-heavy models |
| Compositional correlations | `sparcc` | Direct interactions |
| Sparse conditional networks | `spieceasi` | DA between groups |
| Figure checklist by stage | `visualization` | Table generation |
| Portable pipeline (containers) | `nextflow` | Statistics Methods |
| Rule-based DAG (conda-centric) | `snakemake` | Statistics Methods |

Hard rules:

1. Every figure: **stage + method + DB/software version + normalization**
2. Inspect batch / library size before group tests
3. Report rarefaction (if used), transform, test, and **FDR/FWER**
4. Do not mix MetaPhlAn, Kraken, and MAG abundances unlabeled
5. Network edges and DA hits are associations — not validated biology
6. Workflow managers still must pin each process tool + database

## Decision tree

```text
Research downstream need?
│
├─ Aggregate QC logs → multiqc
├─ Diversity / composition figures
│   ├─ Modular R6 workflow → microeco
│   ├─ phyloseq object + classic API → phyloseq
│   └─ Stage checklist → visualization
├─ Differential abundance
│   ├─ Covariates / longitudinal → maaslin2
│   ├─ Sampling-fraction bias correction → ancombc
│   ├─ Classic LDA → lefse
│   └─ GUI exploratory → stamp
├─ Association networks
│   ├─ SparCC correlations → sparcc
│   └─ SPIEC-EASI graphs → spieceasi
├─ Reproducible pipelines
│   ├─ Nextflow / nf-core → nextflow
│   └─ Snakemake → snakemake
├─ Interactive MAG UI → anvio
└─ Unsure → this hub
```

## Typical order

```text
study-design → (± nextflow|snakemake wrappers)
  → QC (+ multiqc)
  → taxonomy / function tables
  → phyloseq|microeco explore
  → maaslin2|ancombc (± lefse|stamp)
  → (± sparcc|spieceasi)
  → Methods: pin versions, transforms, FDR
```

## Related skills

`visualization` · `microeco` · `phyloseq` · `maaslin2` · `ancombc` · `lefse` ·
`stamp` · `sparcc` · `spieceasi` · `multiqc` · `nextflow` · `snakemake` ·
`study-design` · `setup` · `metaphlan` · `kraken2` · `humann` · `anvio` ·
`metagenomics-workflow` · `tool-selection`
