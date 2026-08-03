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

## Analytical thinking

CheckM2 estimates completeness/contamination quickly with ML models. Values are
**filters and reporting metrics**, especially uncertain for unusual lineages.
Do not mix CheckM and CheckM2 databases across design comparisons silently.

BASALT refinement entry gates and publication filters may differ—state both.

## How to run

```bash
checkm2 database --download
checkm2 predict --input bins/ --output-directory checkm2_out --threads 16
```

## Related skills

`mag-qc` · `metawrap` · `basalt` · `drep`

