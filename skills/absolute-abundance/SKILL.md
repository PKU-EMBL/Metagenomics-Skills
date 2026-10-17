---
name: absolute-abundance
description: >-
  Plan and calculate absolute or load-scaled microbial abundance using spike-ins, flow cytometry, qPCR/dPCR, cell counts, or sample-mass standards. Use when relative abundance is insufficient, when distinguishing compositional shifts from biomass changes, or when documenting assumptions and uncertainty in quantitative microbiome profiling.
license: MIT
compatibility: Requires a relative/count feature table plus matched per-sample quantitative standard measurements.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "absolute-abundance,microbial-load,spike-in,qpcr,flow-cytometry,compositionality"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "calculation template; validate against study-specific controls"
---

# Absolute abundance

Call a result “absolute” only when it is anchored to a calibrated physical quantity. Library size is not microbial load.

## Choose an anchor

| Anchor | Typical unit | Main assumptions |
|---|---|---|
| Exogenous cells/DNA added before extraction | cells or genome equivalents per mass/volume | recovery and lysis behavior are characterized |
| Flow cytometry or microscopy | cells per mass/volume | gating and particle-to-cell conversion are valid |
| Universal qPCR/dPCR | marker copies per mass/volume | extraction efficiency and marker copy number are addressed |
| Sample dry/wet mass plus internal standard | copies per mass | mass and standard addition are accurate |

Adding a standard after extraction cannot correct extraction loss. 16S copies are not cells unless copy-number assumptions are explicit. Shotgun genome equivalents require effective genome-length/mappability considerations.

## Input contract

Use matched sample IDs for:

- non-negative feature counts or relative abundances;
- standard amount added and stage of addition;
- recovered standard reads/copies or independent total-load measurement;
- original sample mass/volume and dilution factors;
- blanks, positive controls, calibration curve, replicate measurements, and detection limits.

## Transparent calculation

For a directly measured total microbial load `L_j` and relative abundance `p_ij`:

`A_ij = p_ij × L_j`

For a spike-in with known amount `S_j`, target reads `R_ij`, and spike reads `R_sj`, a simple ratio estimator is:

`A_ij = (R_ij / R_sj) × S_j × dilution_or_mass_factor`

This estimator assumes comparable recovery and sequencing behavior; taxon-specific efficiency can violate it.

A guarded table calculation:

```bash
python3 - counts.tsv load.tsv absolute.tsv <<'PY'
import sys, pandas as pd
counts = pd.read_csv(sys.argv[1], sep="\t", index_col=0)
load = pd.read_csv(sys.argv[2], sep="\t").set_index("sample_id")["load"]
assert counts.columns.is_unique and counts.index.is_unique
assert set(counts.columns) == set(load.index), "sample IDs do not match"
assert (counts >= 0).all().all() and (load >= 0).all()
rel = counts.div(counts.sum(axis=0).replace(0, float("nan")), axis=1)
absolute = rel.mul(load[counts.columns], axis=1)
absolute.to_csv(sys.argv[3], sep="\t")
assert absolute.loc[:, counts.sum(axis=0)>0].notna().all().all()
PY
```

Record load units in a companion metadata file; the script cannot infer them.

## Validation

- calibration standards fall in the validated dynamic range;
- technical replicates and blanks behave as expected;
- spike recovery is not near zero or batch-dependent without correction;
- reconstructed feature totals agree with the intended load definition;
- uncertainty from calibration, dilution, extraction, and counting is propagated or discussed;
- conclusions are compared with relative-abundance analysis.

## Analytical thinking

Load scaling reduces compositional ambiguity but does not eliminate taxon-specific extraction, lysis, copy-number, mapping, or database bias. Report “load-scaled abundance” when the anchor does not support true cells or molecules. Values below detection should be censored/qualified, not silently set to zero.
