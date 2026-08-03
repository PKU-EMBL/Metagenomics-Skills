---
name: biosurfdb
description: >
  BioSurfDB — curated portal for biosurfactant production and hydrocarbon
  biodegradation genes/pathways with BLAST and related metagenome analysis
  helpers. Use for surfactant/biodegradation-focused searches and pathway
  browsing. Portal: https://www.biosurfdb.org/. Route via dom-biosurfactant.
  Offline experimental gene sets → hadeg; glycan DOM → dbcan.
license: MIT
category: analysis-tools
tags: [BioSurfDB, biosurfactant, biodegradation, hydrocarbon, DOM, portal]
upstream: https://www.biosurfdb.org/
stage: mining
---

# BioSurfDB

Portal: https://www.biosurfdb.org/ ·
Tutorial: https://www.biosurfdb.org/tutorial.php (paths may change — verify)

## Citation

Oliveira, J. S. *et al.* BioSurfDB: knowledge and algorithms to support
biosurfactants and biodegradation studies. *Database* **2015**, bav033 (2015).
https://doi.org/10.1093/database/bav033

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

BioSurfDB integrates biosurfactant catalogues, biodegradation-relevant genes /
pathways, and metagenome-oriented BLAST utilities. Useful for
**surfactant class** exploration and HC biodegradation context. Large private
metagenome uploads may need admin/contact per portal policy — for fully local
pipelines prefer `hadeg` FASTA + DIAMOND.

MEGAN users sometimes map DIAMOND hits onto BioSurfDB classifications — cite
both MEGAN and BioSurfDB if used.

| vs | Prefer BioSurfDB when |
|----|------------------------|
| `hadeg` | Portal pathways / curated surfactant lists / interactive BLAST |
| `antismash` | Pathway/DB hit tables vs BGC coordinates |
| `dbcan` | Surfactant/HC focus vs carbohydrate DOM |

## How to run

```bash
# interactive: upload/search via biosurfdb.org (BLAST vs curated sets)
# local pipeline alternative: hadeg + diamond on proteins.faa
# MEGAN+BioSurfDB functional mapping: follow Sci. Rep. 2022 BioSurfDB+MEGAN notes
```

## Decision tree

```text
Biosurfactant / biodegradation portal need?
├─ Curated portal / pathway browse → biosurfdb
├─ Local experimental gene DB → hadeg
├─ Glycan DOM → dbcan
└─ BGC structure → antismash
```

## Related skills

`dom-biosurfactant` · `hadeg` · `dbcan` · `antismash` · `dram` ·
`microbial-mining` · `tool-selection`
