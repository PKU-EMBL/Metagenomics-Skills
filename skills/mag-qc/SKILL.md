---
name: mag-qc
description: >
  Quality thresholds after binning (completeness/contamination, dRep ANI,
  publication vs refinement gates). Use this skill when: (1) Setting filters
  for bins before calling them MAGs, (2) Choosing dRep ANI cutoffs,
  (3) Interpreting CheckM2 reports, (4) Separating refinement entry gates from
  publication filters, (5) Ranking bin catalogues.
  For binning, use basalt (recommended), metawrap, or dastool.
license: MIT
category: evaluation
tags: [qc, checkm2, drep, completeness, contamination]
---

# MAG Quality Control

## Critical limitation

Marker-based completeness/contamination are **estimates**, not ground truth —
especially for unusual lineages. Treat them as filters and reporting metrics.

## Quick thresholds

| Criterion | Common working gate | Stricter publication |
|-----------|---------------------|----------------------|
| Completeness | ≥ 50% (MetaWRAP refine) / ≥ 35% (BASALT entry) | ≥ 90% (near-complete) |
| Contamination | ≤ 10% refine / ≤ 20% BASALT entry | ≤ 5% |
| dRep species ANI | 95% | study-defined |
| dRep strain ANI | 99% | study-defined |

Declare thresholds **before** inspecting results. Do not optimize for maximum bin count.

## CheckM2

```bash
checkm2 predict --input bins/ --output-directory checkm2_out --threads 16
```

Record database path/version. Do not silently mix CheckM and CheckM2 across design comparisons.

## Scoring / ranking (example)

Prefer multi-criterion ranking:

1. Pass hard filters (comp/cont/size)
2. Prefer higher completeness, lower contamination
3. Prefer better contiguity and read support
4. Prefer taxonomic consistency with study expectations

## Related skills

- `basalt` · `metawrap` · `dastool` — binning stage
- `checkm2` · `drep` — metrics / dereplication
- `visualization` — completeness–contamination plots
- `metagenomics-workflow` — five-stage order
