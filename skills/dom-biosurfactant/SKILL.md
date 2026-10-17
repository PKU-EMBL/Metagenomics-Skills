---
name: dom-biosurfactant
description: >
  Route dissolved organic matter (DOM) / glycan substrate capacity, biosurfactant
  production, and hydrocarbon/plastic biodegradation annotation for shotgun
  metagenomics. Covers “like-dissolves-like” solubility-related microbial functions:
  CAZyme–glycan (dbCAN), biosurfactants + HC degradation (HADEG, BioSurfDB), and related
  BGC context (antiSMASH). Child skills: hadeg, biosurfdb; also dbcan, antismash, dram.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "DOM, biosurfactant, hydrocarbon, biodegradation, CAZyme, solubility, HADEG"
  metagenomics.stage: "mining"
---

# DOM / biosurfactant / biodegradation

Genetic potential for **dissolving, emulsifying, and degrading organic matter**
— CAZymes against complex glycans (DOM-relevant polymers), **biosurfactants**,
and **hydrocarbon / plastic** degradation. Not measured concentrations or CMC.

## What to claim (pin tool)

| Claim | Prefer | Notes |
|-------|--------|-------|
| Complex carbohydrate / glycan DOM processing | `dbcan` (dbCAN3 substrates / CGC) | Cellulose, xylan, pectin, mucin, … |
| Biosurfactant production genes | `hadeg` · `biosurfdb` | Lipopeptide/glycolipid pathways as covered |
| Alkane / alkene / aromatic HC degradation | `hadeg` · `biosurfdb` | Aerobic markers; pin DB release |
| Plastic polymer degradation genes | `hadeg` | Experimental-evidence set |
| Surfactant-related BGCs (NRPS lipopeptides, …) | `antismash` | Cluster ≠ purified surfactant |
| Broad metabolic distillate | `dram` | Complements, does not replace HADEG |

## Analytical thinking

Hard rules:

1. Name substrate class (glycan vs HC vs plastic vs surfactant) and DB version
2. Do not merge CAZyme tables, HADEG hits, and antiSMASH regions unlabeled
3. Hits ≠ emulsification assay or degradation rate
4. Filter low-quality MAGs (`mag-qc`) before community-level claims

## Decision tree

```text
Organic solubility / DOM / surfactant / HC need?
│
├─ Glycan / polymer DOM (CAZymes, PUL/CGC substrates) → dbcan
├─ Biosurfactant + HC/plastic curated genes → hadeg
├─ BioSurfDB pathways / portal BLAST → biosurfdb
├─ Lipopeptide / glycolipid BGCs → antismash
├─ Broad metabolism sheets → dram
└─ Unsure → this hub + microbial-mining
```

## Related skills

`hadeg` · `biosurfdb` · `dbcan` · `antismash` · `dram` · `element-cycling` ·
`qsap` · `microbial-mining` · `tool-selection`
