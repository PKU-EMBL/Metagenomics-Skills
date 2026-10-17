---
name: community-metabolic-modeling
description: >-
  Plan genome-scale and community metabolic modeling from genomes/MAGs through model reconstruction, media-constrained gap filling, quality control, abundance-weighted communities, flux simulation, and sensitivity analysis. Use when routing CarveMe, gapseq, or MICOM and separating model predictions from measured metabolism.
license: MIT
compatibility: Requires quality-gated genomes/proteomes, environmental medium information, metabolic-model software, and a solver.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "metabolic-modeling,gem,flux-balance,carveme,micom,cross-feeding"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Community metabolic modeling

Genome-scale metabolic models (GEMs) encode possible reactions under assumptions. Flux balance solutions are predictions conditional on model, medium, objective, constraints, and solver.

## Routing

- `$carveme`: reconstruct prokaryotic GEMs from proteins/DNA/RefSeq and optionally gap-fill in named media.
- `$gapseq`: pathway prediction and GEM reconstruction with its own databases/workflow.
- `$micom`: combine taxon models with abundance weights and simulate community growth/exchanges.
- `$alphagem`: structure/deep-learning-supported dark-metabolism exploration; treat as hypothesis generation.

## Input contract

For each genome/MAG retain taxonomy, completeness/contamination, annotation/proteome checksum, model source/version, and sample abundance. Define medium compounds, uptake bounds, units, oxygen status, pH/compartment assumptions, and objective before simulation.

Do not interpret missing reactions in incomplete MAGs as biological auxotrophy without sensitivity analysis. Dereplicate models/lineages appropriately and reconcile metabolite identifiers.

## Workflow

1. Quality-gate genomes and generate consistent proteomes.
2. Reconstruct each GEM with `$carveme` or `$gapseq`.
3. Validate SBML parseability, mass/charge issues where available, blocked reactions, biomass feasibility, and media growth.
4. Gap-fill only against documented biologically plausible media; retain added reactions as a separate evidence class.
5. Match models to sample taxa/abundances and state how unmodeled abundance is handled.
6. Build `$micom` communities, choose solver and cooperative-tradeoff strategy, and test a trade-off grid.
7. Simulate growth/exchange under baseline and perturbation media.
8. Validate against known growth/metabolomics where possible and run model/media/abundance sensitivity analyses.

## Required outputs

- model manifest and SBML/model-database checksums;
- original versus gap-filled reaction provenance;
- media file with IDs, bounds, units, and source;
- per-model build/growth QC and failed-model reasons;
- community build manifest, trade-off curve, growth rates, exchange fluxes, solver status;
- uncertainty/sensitivity results and software/solver/container versions.

## Analytical thinking

A feasible exchange flux is not evidence that cross-feeding occurs in situ. Multiple optima, objective choice, missing regulation/kinetics, uncertain biomass functions, MAG incompleteness, and media misspecification can dominate conclusions. Use “predicted potential,” validate direction/sign conventions, and corroborate with metabolomics or experiments.
