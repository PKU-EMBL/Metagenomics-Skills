---
name: resistome-analysis
description: >-
  Design and audit shotgun-metagenomic resistome analyses across curated ARG calls,
  read-level quantification, resistance mutations, MGE context, host assignment, and risk
  interpretation. Use when choosing RGI, AMRFinderPlus, ARGs-OAP, DeepARG, ResFinder, or
  PathoFact and when ARG abundance must not be confused with phenotype or mobility.
license: MIT
compatibility: Requires quality-controlled reads and/or assemblies, pinned ARG databases, gene coordinates, controls, and sample metadata.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "resistome,ARG,AMR,CARD,SARG,mobility,risk"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Resistome analysis

A resistome result has at least four separable layers: **determinant detection,
quantity, genomic context, and biological consequence**. Never collapse these
into one “resistance” label.

## Route by question

| Question | Prefer | Evidence returned |
|---|---|---|
| Curated ARGs on proteins/contigs | `$rgi` (CARD) and/or `$amrfinderplus` (NCBI) | model/homology calls |
| Environmental read-level profiles | `$args-oap` | SARG hierarchy and normalized counts |
| Model-based complement | `$deeparg` | class probability plus best-hit evidence |
| Integrated ARG/VF/toxin/MGE report | `$pathofact` | harmonized but method-specific columns |
| Acquired genes in isolates/HQ MAGs | `$resfinder` / `$staramr` | ResFinder calls |
| Curated chromosomal mutations | `$pointfinder` or organism-aware `$amrfinderplus` | genotype evidence |
| ARG–MGE–host question | `$arg-mge-host-linkage` | coordinate and linkage evidence |

Keep CARD, NCBI AMRFinder, SARG, ResFinder, and DeepARG namespaces in separate
columns. Agreement can raise confidence; disagreement is information, not a
reason to silently union calls.

## Input contract

- immutable sample manifest and biological/technical replicate structure;
- QC/decontamination record and negative/mock controls;
- read files and/or contigs, proteins, GFF coordinates, with globally unique IDs;
- software, model, database release, retrieval date, and checksums;
- predeclared identity, coverage, model-category, probability, and abundance rules;
- measured denominator for absolute claims (spike-in, qPCR, flow cytometry, or mass);
- MGE and host evidence tables when mobility or host attribution is requested.

Taxon-specific mutation prediction is inappropriate on an unresolved mixed
community. Run it only on a defensible isolate or genome assignment and retain
callable-locus/no-call information.

## Analysis workflow

1. Freeze inputs, controls, database releases, and the primary reporting rule.
2. Call genes consistently; preserve contig and coordinate mappings.
3. Run one curated detector; add an orthogonal detector only for a declared purpose.
4. Reconcile exact sequence/coordinate identities, not gene names alone.
5. Quantify with a denominator matching the claim: reads, gene length/library size,
   cells, 16S copies, DNA mass, or external spike-in.
6. Join ARGs to MGE boundaries and hosts through `$arg-mge-host-linkage`.
7. Report detection limits, no-hit samples, controls, and threshold sensitivity.
8. Treat metatranscriptomic support, phenotype, and transfer assays as separate layers.

## Required result schema

At minimum retain:

```text
sample_id, query_id, contig_id, start, end, strand, detector, database,
database_release, accession, gene_symbol, drug_class, mechanism, model_or_method,
identity, query_coverage, subject_coverage, score_or_probability, call_tier,
quantity, quantity_unit, mge_id, host_id, linkage_tier, control_flag, provenance_id
```

Missing values must remain explicit. Keep all primary no-calls and filtered calls
in an audit table with reasons.

## Evidence and risk boundaries

Sequence confidence, abundance, mobility, host/pathogen context, environmental
selection, expression, and phenotype are different axes. A high-abundance ARG is
not automatically high risk; an ARG on the same sample as a plasmid is not
plasmid-borne. Use the risk-ranking concept of Martínez *et al.* as a framework,
not as permission to invent an unvalidated universal score.

Claims should progress only as evidence supports them:

```text
ARG-like sequence → curated determinant → coordinate-linked MGE context
→ independently supported host → expressed determinant → measured phenotype
→ observed transfer under defined conditions
```

Computational analysis normally stops before the last three steps.

## Validation and provenance

Reconcile query counts, duplicated IDs, coordinate bounds, database-accession
versions, controls, and samples with zero calls. Inspect full-length versus
fragment calls and separate intrinsic/core genes from acquired determinants.
Archive commands, environments, database manifests/checksums, raw and filtered
outputs, join code, and the exact reporting thresholds. Database or threshold
changes require a new output directory.

For the cross-layer evidence framework and classic literature, see the
[ARG–MGE–host–strain evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`rgi` · `amrfinderplus` · `args-oap` · `deeparg` · `pathofact` · `resfinder` ·
`pointfinder` · `staramr` · `abricate` · `mobilome-analysis` ·
`arg-mge-host-linkage` · `absolute-abundance` · `metatranscriptomics`
