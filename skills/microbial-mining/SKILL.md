---
name: microbial-mining
description: >
  Route microbial / genome mining after assembly or binning: biosynthetic gene
  clusters (antiSMASH), AMR (RGI, DeepARG), mobile elements and viruses
  (geNomad, VirSorter2, CheckV), antimicrobial peptides (Macrel), metabolism
  (DRAM, gapseq), defense systems (DefenseFinder), and genome annotation
  substrates (Bakta/Prokka). Use when the scientific question is discovery of
  functional elements, not community tables alone.
license: MIT
category: orchestration
tags: [genome-mining, BGC, AMR, MGE, virus, metabolism, routing]
stage: mining
---

# Microbial mining

Mine assembled contigs and QC-filtered genomes/MAGs for **functional elements**.
This is a parallel track after assembly/binning — not a replacement for
taxonomy tables.

## Analytical thinking

Ask what is being claimed:

| Claim type | Prefer | Caution |
|------------|--------|---------|
| Natural products / BGCs | `antismash` | Cluster ≠ characterized compound |
| AMR / resistome | `rgi` (+ `deeparg`) | Hit ≠ expression / phenotype |
| Plasmids / viruses / MGEs | `genomad`, `virsorter2`, `checkv` | Completeness via CheckV |
| Antimicrobial peptides | `macrel` | High candidate false-positive risk |
| Metabolic potential | `dram`, `gapseq` | Needs decent genome completeness |
| Anti-phage defense | `defensefinder` | Annotate proteins first (`bakta`) |
| Per-genome annotation substrate | `bakta` / `prokka` | Feed other miners |

## Decision tree

```text
Mining goal?
├─ BGCs / secondary metabolism → antismash  (+ bakta)
├─ Resistome / ARGs → rgi  (± deeparg)
├─ Plasmids / viruses / MGEs → genomad  (± virsorter2 → checkv)
├─ AMP smORFs → macrel
├─ Distilled metabolism → dram
├─ Genome-scale models → gapseq (high-quality MAGs)
├─ Defense systems → defensefinder
└─ Unsure → start bakta/prokka on MAGs, then branch
```

## Typical order

```text
bins/MAGs (checkm2 / mag-qc)
   → bakta | prokka
   ├─→ antismash
   ├─→ rgi (± deeparg)
   ├─→ dram → gapseq
   └─→ defensefinder
contigs (pre- or post-binning)
   → genomad | virsorter2 → checkv
   → macrel (smORF/AMP)
```

## Never

- Treat antiSMASH regions as proven natural products
- Merge viral contig counts with bacterial MAG catalogues unlabeled
- Skip CheckV when publishing viral genomes
- Run heavy mining on failed/low-quality bins without stating filters

## Related skills

`antismash` · `genomad` · `virsorter2` · `checkv` · `macrel` · `dram` · `bakta` ·
`rgi` · `deeparg` · `gapseq` · `defensefinder` · `prokka` · `tool-selection`
