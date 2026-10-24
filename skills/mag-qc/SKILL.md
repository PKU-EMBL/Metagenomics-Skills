---
name: mag-qc
description: >
  Quality thresholds after binning (completeness/contamination, dRep ANI, publication vs
  refinement gates). Use this skill when: (1) Setting filters for bins before calling
  them MAGs, (2) Choosing dRep ANI cutoffs, (3) Interpreting CheckM2 reports, (4)
  Separating refinement entry gates from publication filters, (5) Ranking bin
  catalogues, (6) Choosing Deepurify vs Anvi'o vs GUNC. For binning, use basalt
  (recommended), metawrap, or dastool.
license: MIT
metadata:
  metagenomics.category: "evaluation"
  metagenomics.tags: "qc, checkm2, drep, completeness, contamination"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "quality-policy guidance reviewed; example CheckM2 command not executed here"
---

# MAG Quality Control

## Critical limitation

Marker/ML completeness/contamination are **estimates**, not ground truth —
especially for unusual lineages. Treat them as filters and reporting metrics.

## Quick thresholds

| Criterion | Common working gate | Stricter publication |
|-----------|---------------------|----------------------|
| Completeness | ≥ 50% (MetaWRAP refine) / ≥ 35% (BASALT entry) | ≥ 90% (near-complete) |
| Contamination | ≤ 10% refine / ≤ 20% BASALT entry | ≤ 5% |
| dRep species ANI | 95% | study-defined |
| dRep strain ANI | 99% | study-defined |

Declare thresholds **before** inspecting results. Do not optimize for maximum bin count.
Keep refinement **entry** gates distinct from publication filters in Methods.

## Recommended QC narrative

```text
bins
  → checkm2 (comp/cont scores)
  → gunc (chimerism / clade contamination)
  → optional deepurify (remove/split) or anvio (interactive) → re-checkm2/gunc
  → drep (skani|fastani ANI) → species/strain reps
  → gtdbtk / mining
```

## Tool roles

| Tool | Role |
|------|------|
| `checkm2` | ML completeness / contamination scores |
| `gunc` | Chimeric / foreign-lineage contamination |
| `deepurify` | Automated contig removal / sub-MAG split |
| `anvio` | Human-guided contig refinement |
| `drep` | Dereplicate by ANI |
| `skani` / `fastani` | ANI engines / cross-checks |
| `busco` | Optional gene-set view (not a CheckM2 replacement) |

## CheckM2

```bash
set -Eeuo pipefail
bins="${1:?usage: qc-mags.sh BINS_DIR OUTPUT_DIR}"
out="${2:?usage: qc-mags.sh BINS_DIR OUTPUT_DIR}"
threads="${THREADS:-16}"
test -d "$bins" || exit 2
find "$bins" -maxdepth 1 -type f -print -quit | grep -q . || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$(dirname "$out")" logs
checkm2 predict --input "$bins" --output-directory "$out" --threads "$threads" \
  >"logs/$(basename "$out").checkm2.stdout.log" \
  2>"logs/$(basename "$out").checkm2.stderr.log"
test -s "$out/quality_report.tsv"
```

Record database path/version. Do not silently mix CheckM1 and CheckM2 across
design comparisons.

## Scoring / ranking (example)

1. Pass hard filters (comp/cont/size)
2. Prefer higher completeness, lower contamination
3. Prefer better contiguity and read support
4. Prefer taxonomic consistency; discordant GUNC → review

## Required deliverables and acceptance

Create one audit table with stable genome ID, source binner/refinement lineage,
FASTA checksum, size/contiguity, CheckM2 values and release, GUNC metrics and
release, taxonomy, coverage support, dereplication cluster, decision, and explicit
rejection reason. Every input must appear exactly once. Keep raw and rounded
metrics separate and retain rejected bins.

Refinement or decontamination invalidates prior QC: rerun all gates on the exact
exported FASTA. Evaluate threshold sensitivity, novel-lineage discordance, and
representative selection. Archive commands, environments, databases/checksums,
logs, QC tables, decision code, accepted/rejected manifests, and final checksums.
Labels such as medium/high quality are operational criteria unless all required
standards and evidence are explicitly documented.

## Related skills

`basalt` · `metawrap` · `dastool` · `checkm2` · `gunc` · `deepurify` ·
`anvio` · `drep` · `skani` · `fastani` · `busco` · `visualization` ·
`metagenomics-workflow`
