---
name: microbial-mining
description: >
  Route microbial / genome mining after assembly or binning: biosynthetic gene
  clusters (antiSMASH, BiG-SCAPE), AMR (RGI, DeepARG), mobile elements and
  viruses (geNomad, VirSorter2, CheckV), antimicrobial peptides (Macrel),
  metabolism (DRAM, gapseq, dbCAN), defense systems (DefenseFinder), and
  genome annotation substrates (Bakta/Prokka). Use when the question is
  discovery of functional elements, not community tables alone.
license: MIT
category: orchestration
tags: [genome-mining, BGC, AMR, MGE, virus, metabolism, routing]
stage: mining
---

# Microbial mining

Mine assembled contigs and QC-filtered genomes/MAGs for **functional elements**.
Parallel track after assembly/binning — not a replacement for taxonomy tables.

## Analytical thinking

| Claim type | Prefer | Caution |
|------------|--------|---------|
| Natural products / BGCs | `antismash` → `bigscape` | Cluster ≠ characterized compound |
| AMR / resistome | `rgi` (± `deeparg`) | Hit ≠ expression / phenotype |
| Plasmids / viruses / MGEs | `genomad`, `virsorter2`, `checkv`, `vcontact` | CheckV before taxonomy |
| Plasmid genome recovery | `plasmaag` | Multi-sample graphs help |
| Antimicrobial peptides | `macrel` | High candidate FDR |
| Distilled metabolism | `dram` | Needs decent completeness |
| CAZymes | `dbcan` | Consensus evidence rules |
| Genome-scale models | `gapseq` (± `vmh`) | HQ MAGs only |
| Anti-phage defense | `defensefinder` | Annotate proteins first |
| Annotation substrate | `bakta` / `prokka` | Feed other miners |

## Decision tree

```text
Mining goal?
├─ BGCs → antismash → (many genomes) bigscape
├─ Resistome → rgi (± deeparg); intersect genomad plasmids if relevant
├─ Plasmids / viruses → genomad (± virsorter2) → checkv → vcontact
├─ Plasmid MAGs → plasmaag (± genomad)
├─ AMP smORFs → macrel
├─ Metabolism distillate → dram (± dbcan)
├─ GEMs → gapseq
├─ Defense systems → bakta/prokka → defensefinder
└─ Unsure → bakta on HQ MAGs, then branch
```

## Typical order

```text
bins/MAGs (checkm2 / mag-qc / gunc)
   → bakta | prokka
   ├─→ antismash → bigscape
   ├─→ rgi (± deeparg)
   ├─→ dram → dbcan / gapseq
   └─→ defensefinder
contigs
   → genomad | virsorter2 → checkv → vcontact
   → plasmaag (multi-sample plasmid recovery)
   → macrel
```

## Never

- Treat antiSMASH regions as proven natural products
- Publish viral genomes without CheckV
- Merge mining hits with HUMAnN abundances unlabeled
- Mine failed/low-quality bins without stating filters

## Related skills

`antismash` · `bigscape` · `genomad` · `virsorter2` · `checkv` · `macrel` ·
`dram` · `dbcan` · `bakta` · `rgi` · `deeparg` · `gapseq` · `vmh` · `defensefinder` ·
`vcontact` · `plasmaag` · `tool-selection`
