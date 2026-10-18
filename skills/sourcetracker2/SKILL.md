---
name: sourcetracker2
description: >-
  Estimate source-environment contributions to sink communities with SourceTracker2's
  Bayesian mixture model. Use for amplicon or feature-count source tracking when defining
  train/test folds, source/sink metadata, rarefaction or count handling, leave-one-out
  validation, unknown-source mass, seeds, and compositional interpretation.
license: MIT
compatibility: Requires SourceTracker2 2.0.1, a pinned Python 3.8-compatible environment or container, a BIOM integer-count table, and source/sink metadata keyed by sample.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "SourceTracker2,source-tracking,Bayesian,mixture,unknown-source"
  metagenomics.upstream: "https://github.com/biota/sourcetracker2"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/input/output contract reviewed; not executed here"
---

# SourceTracker2

SourceTracker2 estimates the mixture of declared source environment categories in each
sink plus an `Unknown` component. It models feature-count composition, not individual
strain migration.

## Input contract

- BIOM-format integer count table with feature and sample IDs;
- metadata with `Env` and `SourceSink` (`source`/`sink`) keyed to every sample;
- unique sample and feature IDs and explicit zero-depth exclusions;
- source categories defined before inspecting sink outcomes;
- train/test or leave-one-out design that keeps subjects, batches, time clusters, and
  technical replicates from leaking across folds;
- negative controls and plausible “missing source” controls.

Use the same extraction, marker/reference, filtering, and feature definition for sources
and sinks. The CLI calls `biom.load_table`; convert a validated TSV to BIOM explicitly rather than
passing TSV directly. Relative-abundance tables are not interchangeable with integer counts.

## Run

```bash
set -euo pipefail
table=${COUNT_TABLE:?set COUNT_TABLE}
meta=${METADATA:?set METADATA}
out=${OUTDIR:-results/sourcetracker2}
[[ -s "$table" && -s "$meta" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
sourcetracker2 gibbs -i "$table" -m "$meta" -o "$out/gibbs" \
  --jobs 8 --source_rarefaction_depth 0 --sink_rarefaction_depth 0 \
  >"$out/gibbs.stdout.log" 2>"$out/gibbs.stderr.log"
[[ -s "$out/gibbs/mixing_proportions.txt" && \
   -s "$out/gibbs/mixing_proportions_stds.txt" ]] || exit 3
```

Disabling rarefaction is an explicit modeling choice, not a universal recommendation.
When rarefying, choose depth from the depth distribution before outcome analysis and retain
dropped samples. SourceTracker2 2.0.1 does not expose a CLI seed; record that limitation or
use a tested wrapper that sets NumPy state rather than implying deterministic output.

## Validation

- reconcile count-table columns and metadata rows exactly;
- ensure source/sink and `Env` labels have no missing or accidental whitespace values;
- run cross-validated known-source-as-sink tests and report confusion/calibration;
- include held-out or synthetic unknown sources and negative controls;
- inspect posterior standard deviations, convergence/chain settings, low-depth sinks, and
  dominance by batch-specific features;
- perturb feature filters, depth handling, source granularity, and fold assignment;
- benchmark against `$feast` under the same folds and feature table.

## Recovery and provenance

Rerun from scratch in a new output after changing counts, metadata, source categories,
rarefaction, priors, iterations, or software. Record SourceTracker2/environment versions,
commands, random-state support/status, count/metadata checksums, fold assignments, source definition, depth and
feature filters, chain settings, and all exclusions.

## Interpretation

A contribution is compositional compatibility with sampled source categories. `Unknown`
is residual unexplained mass, not a single unknown habitat. Results do not identify cells,
strains, direction of transmission, timing, or direct migration; use `$strain-transmission`
for strain-level hypotheses.

## Source

- https://github.com/biota/sourcetracker2
- https://doi.org/10.1038/nmeth.1650

## Related skills

`source-tracking` · `feast` · `strain-transmission` · `transfer-network-analysis` ·
`absolute-abundance` · `study-design`
