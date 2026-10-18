---
name: source-tracking
description: >-
  Design and audit microbial source-tracking analyses with explicit source/sink definitions, FEAST or SourceTracker2, controls, unknown-source fractions, cross-validation, and compositional limits. Use for contamination attribution, environmental mixing, or community-origin hypotheses without equating estimated proportions with proven transmission.
license: MIT
compatibility: Requires a harmonized sample-by-feature count table, source/sink metadata, controls, and a source-tracking method such as FEAST.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "source-tracking,feast,sourcetracker2,source-sink,contamination,mixing,unknown-source"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Source tracking

Source tracking estimates how a sink composition can be represented by sampled source communities plus an unknown component. It does not establish physical transfer or directionality by itself.

## Design before modeling

Define source classes independently of the sink results. Sample plausible sources with biological and technical replication, at relevant times/locations, and process them using the same extraction, sequencing, feature pipeline, and database. Include blanks as diagnostic sources where contamination attribution matters.

Avoid using a sample as both source and sink in the same fit. Prevent subject/time leakage in training and validation. If candidate sources were not sampled, expect the unknown fraction—not forced attribution—to carry that signal.

## Input contract

- non-negative integer sample-by-feature counts with identical feature definitions;
- unique sample IDs and metadata columns for environment, source/sink status, and source-set/sink group;
- predeclared rare-feature filter and sequencing-depth handling;
- batch, geography, subject, time, and control labels;
- negative controls and known/simulated mixtures for calibration where possible.

## Workflow

1. Harmonize and validate source/sink feature spaces.
2. Visualize depth, composition, batch, and source separability without using sinks to tune labels.
3. Run leave-one-source-out classification: treat known source samples as pseudo-sinks.
4. Run `$feast` or `$sourcetracker2` with a fixed seed, source assignment rule, and depth strategy.
5. Inspect the unknown fraction, source collinearity, convergence/stability, and control attribution.
6. Bootstrap source samples/features or repeat subsampling to estimate uncertainty.
7. Test sensitivity to source pooling, rare-feature filtering, depth, and omitted source classes.
8. Report sample-level estimates before any group aggregation.

## Quality gates

- contributions sum to approximately one for every modeled sink;
- source and sink IDs are fully accounted for;
- held-out sources are recovered above a predeclared baseline;
- negative controls do not dominate without investigation;
- near-identical source environments are not overinterpreted individually;
- unknown and unmodeled fractions remain visible in plots/tables.

## Deliverables

Produce source/sink manifest, feature-processing recipe, contribution matrix, uncertainty/sensitivity tables, pseudo-sink validation, control diagnostics, software/seed/commands, and a limitations statement.

## Analytical thinking

Estimated source proportions are model-dependent compositional allocations. Shared ecology, unsampled intermediates, laboratory contamination, and database/feature bias can mimic source relationships. Keep `source_contribution` edges separate from strain sharing and transmission posteriors. Use “compatible with contribution from” rather than “originated from” unless independent tracing evidence exists.

## Related skills

`feast` · `sourcetracker2` · `strain-resolved-analysis` · `strain-transmission` ·
`transfer-network-analysis` · `contamination-control` · `study-design`
