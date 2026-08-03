---
name: checkm2
description: >
  ML-based MAG completeness and contamination estimation. Use this skill when working with checkm2: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/chklovski/CheckM2. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'completeness', 'MAG']
upstream: https://github.com/chklovski/CheckM2
---

# CheckM2

Upstream: [chklovski/CheckM2](https://github.com/chklovski/CheckM2)

## Citation

Chklovski, A., Parks, D. H., Woodcroft, B. J. & Tyson, G. W. CheckM2: a rapid, scalable and accurate tool for assessing microbial genome quality using machine learning. *Nat. Methods* **20**, 1203–1212 (2023). https://doi.org/10.1038/s41592-023-01940-w

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

CheckM1-style tools predict quality from **lineage-specific single-copy markers**.
That fails or becomes overconfident when lineages lack robust marker sets
(novel phyla/classes, CPR, etc.). CheckM2 uses **gradient-boosting ML** on
broader genomic features to estimate completeness/contamination without
explicit lineage marker sets — the paper emphasizes improved accuracy on
taxonomically novel MAGs.

Still:

- Values are **filters and reporting metrics**, not wet-lab truth.
- Do not silently mix CheckM1 and CheckM2 scores across a study.
- Pair with `gunc` for chimeric / clade-separated contamination CheckM-style
  metrics can miss.
- BASALT refinement **entry** gates (e.g. comp≥35 / cont≤20) often differ from
  publication filters (e.g. ≥90 / ≤5) — state both (`mag-qc`).

## How to run

```bash
checkm2 database --download
checkm2 predict --input bins/ --output-directory checkm2_out --threads 16
```

## Key parameters

| Item | Notes |
|------|-------|
| Database | Pin CheckM2 DB release with software version |
| Input | Directory of bin FASTAs |
| Downstream | Feed filtered bins to `drep` / `gtdbtk` |

## Related skills

`mag-qc` · `gunc` · `metawrap` · `basalt` · `drep` · `busco`
