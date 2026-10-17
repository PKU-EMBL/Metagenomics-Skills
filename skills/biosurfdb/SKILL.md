---
name: biosurfdb
description: >
  BioSurfDB — curated portal for biosurfactant production and hydrocarbon biodegradation
  genes/pathways with BLAST and related metagenome analysis helpers. Use for
  surfactant/biodegradation-focused searches and pathway browsing. Offline experimental
  gene sets → hadeg; glycan DOM → dbcan.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "BioSurfDB, biosurfactant, biodegradation, hydrocarbon, DOM, portal"
  metagenomics.upstream: "https://www.biosurfdb.org/"
  metagenomics.stage: "mining"
---

# BioSurfDB

Portal: https://www.biosurfdb.org/ ·
Tutorial: https://www.biosurfdb.org/tutorial.php

## Citation

Oliveira, J. S. *et al.* BioSurfDB: knowledge and algorithms to support
biosurfactants and biodegradation studies. *Database* **2015**, bav033 (2015).
https://doi.org/10.1093/database/bav033

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

## Portal contract

BioSurfDB is an interactive web resource; the reviewed public site does not expose a stable versioned CLI/API, so do not invent one. Before upload, confirm data policy and avoid sensitive/unreleased sequence. Record access date, database/site version if displayed, query IDs/checksum, search program, database scope, all thresholds and downloaded raw hit/pathway tables. Take a local copy of the result schema and portal citations.

For auditable local sequence analysis, route to `$hadeg` with its pinned FASTA/Proteinortho workflow or another licensed downloadable reference. If MEGAN mapping is used, preserve its mapping database release and parameters separately; portal screenshots alone are not machine-readable evidence.

## Decision tree

```text
Biosurfactant / biodegradation portal need?
├─ Curated portal / pathway browse → biosurfdb
├─ Local experimental gene DB → hadeg
├─ Glycan DOM → dbcan
└─ BGC structure → antismash
```

## Validation and interpretation

Reconcile every portal result to submitted query IDs, retain no-hit queries, verify coordinates/scores/annotations where exported, and cross-check priority hits against HADEG, profile HMMs, gene neighborhood or curated literature. If version/database details cannot be recovered, label the run non-reproducible and do not merge it into a frozen production table.

BioSurfDB similarity/pathway labels support candidate biodegradation or biosurfactant potential; they do not establish pathway completeness, expression, compound production or degradation rate.

## Related skills

`dom-biosurfactant` · `hadeg` · `dbcan` · `antismash` · `dram` ·
`microbial-mining` · `tool-selection`
