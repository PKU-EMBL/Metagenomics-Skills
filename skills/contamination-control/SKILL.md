---
name: contamination-control
description: >-
  Design, execute, and audit contamination control for low-biomass or contamination-sensitive microbiome studies using blanks, positive controls, batch-aware evidence, decontam, and read-level host/reagent screening. Use when planning controls, deciding whether a feature or sample is contaminated, or documenting contamination handling without blindly subtracting taxa.
license: MIT
compatibility: Requires sample metadata and count/profile outputs; optional R/decontam and read-classification tools.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "contamination,negative-controls,low-biomass,blank-controls,decontam,qc"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Contamination control

Treat contamination as a study-design and evidence-integration problem, not a list of taxa to delete.

## Inputs to require

- sample manifest with biological sample, extraction blank, library blank, positive control, batch, plate, operator, and extraction-kit lot;
- raw read counts, DNA concentration before library preparation, and sequencing yield;
- a feature table from one consistently processed assay (taxa, genes, ASVs, or MAGs);
- host/reference identities and expected positive-control composition;
- a written rule for sample exclusion versus feature flagging.

Stop if controls were pooled under ordinary sample labels or if feature-table columns cannot be matched exactly to metadata. Record missing controls as a limitation; do not invent them computationally.

## Control design

| Failure source | Minimum evidence | Useful response |
|---|---|---|
| Field or collection contamination | field blanks, collection-device blanks | identify collection-specific features/batches |
| Extraction reagents | extraction blanks in every kit lot/batch | prevalence and DNA-concentration models |
| Library preparation | library blanks and positive controls | inspect batch and index cross-talk |
| Host carry-over | host reference and read-level mapping | quarantine mapped reads; retain removal statistics |
| Cross-sample leakage | unique dual indexes, abundance gradients | inspect unexpected control taxa and index pairs |

Randomize biological groups across extraction and library batches. A batch perfectly confounded with phenotype cannot be repaired by a statistical contaminant classifier.

## Auditable workflow

1. Preserve immutable raw files and checksums.
2. Process controls with the same pipeline and database as biological samples.
3. Plot library size, DNA concentration, control prevalence, and feature abundance by batch.
4. Run `$decontam` with prevalence, frequency, or combined evidence where inputs permit.
5. Independently inspect dominant features in blanks and positive-control deviations.
6. Mark each feature `retain`, `flag`, or `remove`, with method, threshold, batch, and evidence columns.
7. Re-run primary results with and without flagged features and excluded samples.

A minimal manifest gate:

```bash
set -euo pipefail
manifest=${1:?usage: check-controls.sh manifest.tsv}
[[ -s "$manifest" ]] || { echo "empty manifest: $manifest" >&2; exit 2; }
python3 - "$manifest" <<'PY'
import csv, sys
p = sys.argv[1]
with open(p, newline="") as fh:
    rows = list(csv.DictReader(fh, delimiter="\t"))
need = {"sample_id", "sample_type", "extraction_batch", "library_batch"}
missing = need - set(rows[0] if rows else {})
assert rows and not missing, f"missing columns or rows: {sorted(missing)}"
ids = [r["sample_id"] for r in rows]
assert len(ids) == len(set(ids)), "sample_id values are not unique"
types = {r["sample_type"] for r in rows}
assert "biological" in types, "no biological samples"
assert types & {"extraction_blank", "library_blank"}, "no negative controls"
print(f"rows={len(rows)} sample_types={sorted(types)}")
PY
```

## Output contract and verification

Produce:

- `control_manifest.tsv` with original and analysis labels;
- `contaminant_evidence.tsv` with feature ID, model score, threshold, blank prevalence, biological prevalence, batch, decision, and rationale;
- before/after library-size and ordination summaries;
- retained/excluded sample lists;
- versions, database releases, commands, seeds, and checksums.

Verify that table and metadata IDs are bijective, controls remain visible in diagnostic plots, each removal maps to evidence, and conclusions are stable or explicitly sensitivity-dependent.

## Analytical thinking

A feature enriched in blanks is evidence of contamination, not proof that every occurrence is contaminant-derived. Conversely, a biologically plausible taxon can still be a reagent contaminant. Prefer batch-aware models and sensitivity analyses. Never use a universal blacklist, never subtract blank counts arithmetically, and never report decontamination as experimental validation.

## References

- decontam: https://benjjneb.github.io/decontam/
- Davis *et al.* (2018): https://doi.org/10.1186/s40168-018-0605-2
