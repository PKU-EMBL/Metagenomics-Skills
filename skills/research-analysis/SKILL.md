---
name: research-analysis
description: >
  Route statistically defensible downstream shotgun-metagenomics analysis: QC reports,
  diversity/composition figures, multivariable or compositional differential abundance,
  repeated measures, association networks, workflow managers, and Methods-ready
  provenance. Use after taxonomy/function/abundance tables and sample metadata exist;
  use study-design first when contrasts, biological units, batches, or controls are
  unresolved.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "research-analysis, statistics, visualization, differential-abundance, network, Nextflow, Snakemake"
  metagenomics.stage: "report"
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
| Monte Carlo CLR effects | `aldex2` | Absolute abundance |
| Count mean/dispersion models | `corncob` | Valid analysis of relative percentages |
| Community distance test | `permanova` | A centroid effect without dispersion checks |
| Classic LDA biomarkers | `lefse` | Modern multivariable default |
| GUI exploratory profile tests | `stamp` | Covariate-heavy models |
| Compositional correlations | `sparcc` | Direct interactions |
| Sparse conditional networks | `spieceasi` | DA between groups |
| Network construction/comparison | `netcomi` | Direct ecological interaction |
| Source contributions | `source-tracking` → `feast` | Proof of transmission |
| Load-aware abundance | `absolute-abundance` | Calibration-free absolute cells |
| Figure checklist by stage | `visualization` | Table generation |
| Portable pipeline (containers) | `nextflow` | Statistics Methods |
| Rule-based DAG (conda-centric) | `snakemake` | Statistics Methods |

Hard rules:

1. The independent biological sample/subject/site is the inferential unit — not
   reads, genes, contigs, MAGs, or technical replicates.
2. Join abundance and metadata by explicit IDs and report unmatched/duplicate
   IDs before filtering or modeling.
3. Freeze the primary contrast, covariates, repeated-measure structure, and
   exclusion rules before inspecting group-associated features.
4. Inspect depth, zero structure, prevalence, controls, batch, and confounding.
   If group and batch are inseparable, do not claim an adjusted group effect.
5. Preserve raw counts when a method requires them. Do not rarefy by default for
   differential abundance; if rarefaction is used for a specific diversity
   estimator, report depth, repetitions, and discarded samples.
6. Report filtering, pseudocount, normalization/offset, transform, model,
   effect-size scale, uncertainty, and **FDR/FWER** — not adjusted P values alone.
7. Do not mix MetaPhlAn, Kraken/Bracken, gene, pathway, and MAG abundance
   semantics in an unlabeled table.
8. Network edges and DA hits are associations, not direct interactions or
   validated mechanisms. Workflow managers still pin every tool and database.

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
│   ├─ Monte Carlo CLR effect sizes → aldex2
│   ├─ Count mean and dispersion effects → corncob
│   ├─ Classic LDA → lefse
│   └─ GUI exploratory → stamp
├─ Whole-community distances → permanova (plus dispersion)
├─ Association networks → netcomi (or sparcc / spieceasi)
├─ Source contributions → source-tracking → feast
├─ Absolute/load-aware abundance → absolute-abundance
├─ Reproducible pipelines
│   ├─ Nextflow / nf-core → nextflow
│   └─ Snakemake → snakemake
├─ Interactive MAG UI → anvio
└─ Unsure → this hub
```

## Inferential workflow

```text
study-design → (± nextflow|snakemake wrappers)
  → QC (+ multiqc)
  → validate abundance semantics + sample-ID join
  → inspect controls, depth, prevalence, zeroes, batch/confounding
  → phyloseq|microeco exploration (label exploratory analyses)
  → maaslin2|ancombc with declared contrast/covariates/repeated structure
  → diagnostics + effect sizes/CI + multiplicity correction
  → optional sparcc|spieceasi network (stability/sensitivity analysis)
  → Methods + machine-readable result/provenance tables
```

Do not choose a method from the desired significance pattern. Use negative
controls and mock communities to diagnose contamination/performance where
available, but do not automatically subtract every feature observed in a blank.
For longitudinal or clustered designs, keep subject/site identifiers and use a
method that represents within-unit dependence; otherwise qualify inference.

## Minimum delivery

- validated sample/feature tables and an ID-join report
- frozen contrast/covariate/filter specification
- model-ready input (unchanged after result inspection) and executable script
- software/session and database/profiling provenance
- full results including non-significant rows, effect sizes, uncertainty,
  raw and adjusted P values, and convergence/diagnostic flags
- figure source data plus captions stating abundance type, transform, test, and n
- sensitivity notes for filtering, normalization, influential samples, and batch

## Related skills

`visualization` · `microeco` · `phyloseq` · `maaslin2` · `ancombc` · `aldex2` ·
`corncob` · `permanova` · `lefse` · `stamp` · `netcomi` · `sparcc` ·
`spieceasi` · `absolute-abundance` · `source-tracking` · `feast` · `multiqc` ·
`nextflow` · `snakemake` · `nf-core-mag` · `nf-core-taxprofiler` ·
`study-design` · `setup` · `metaphlan` · `kraken2` · `humann` · `anvio` ·
`metagenomics-workflow` · `tool-selection`
