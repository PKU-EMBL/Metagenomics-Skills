---
name: element-cycling
description: >
  Route biogeochemical / elemental cycling annotation for shotgun metagenomics
  and MAGs: carbon (C), nitrogen (N), sulfur (S), iron (Fe), phosphorus (P),
  hydrogen (H2/H), oxygen (O), methane (CH4), and other metals/metalloids
  (Mn, As, Se, …) via METABOLIC, MEBS, FeGenie, plus DRAM/KEGG/eggNOG backups.
  Use when asking which elemental transformations a community or MAG can
  perform — not for taxonomy tables. Child skills: metabolic, mebs, fegenie.
  Related: dram, kegg, eggnog-mapper, gapseq. Route via microbial-mining.
license: MIT
category: orchestration
tags: [element-cycling, biogeochemistry, C, N, S, Fe, P, CH4, METABOLIC, MEBS, FeGenie]
stage: mining
---

# Element cycling (biogeochemistry)

Elemental / biogeochemical capacity is a **mining track** after gene call on
assemblies or QC-filtered MAGs. Hits are genetic potential — not fluxes.

## Elements to report (pin which you claim)

| Element / cycle | Typical transformations | Prefer |
|-----------------|-------------------------|--------|
| **C** (carbon) | Fixation, fermentation, respiration, C1 | `metabolic` · `dram` · `kegg` |
| **N** (nitrogen) | N₂ fixation, nitrification, denitrification, anammox, DNRA, ammonification | `metabolic` · `mebs` · `dram` |
| **S** (sulfur) | Sulfate/sulfite reduction, oxidation, disproportionation, organic S | `mebs` · `metabolic` · `dram` |
| **Fe** (iron) | Acquisition, siderophores, Fe²⁺/Fe³⁺ redox, storage, magnetosome | `fegenie` · `mebs` · `metabolic` |
| **P** (phosphorus) | Uptake, solubilization, poly-P, organic P | `metabolic` · `dram` · `kegg` |
| **H / H₂** | Hydrogenases, H₂ metabolism | `metabolic` · `dram` |
| **O** | Aerobic respiration markers / O-related scores | `mebs` · `metabolic` |
| **CH₄** (methane) | Methanogenesis, methanotrophy | `mebs` · `metabolic` · `dram` |
| **Other metals** | Mn, As, Se, Hg, … (tool “other” / KO modules) | `metabolic` · `kegg` · `eggnog-mapper` |

## Analytical thinking

| Claim | Prefer | Do not treat as |
|-------|--------|-----------------|
| Multi-element MAG/community diagrams (C/N/S/…) | `metabolic` (METABOLIC-G/C) | Measured rates |
| Entropy scores for S (and N/O/CH₄/Fe) machinery | `mebs` | Pathway proof without genes |
| Iron acquisition / redox / siderophores / magnetosome | `fegenie` | Sole Fe claim from generic KO only |
| Distilled metabolism tables (broad) | `dram` | Element-specific FeGenie depth |
| KO/module maps (licensed KEGG) | `kegg` / `eggnog-mapper` | Bulk redistributable KEGG dump |
| GEMs / flux hypotheses | `gapseq` (± `alphagem`) | Element HMM presence alone |

Hard rules:

1. Name **which elements** and which tool/DB version produced each claim
2. Do not merge METABOLIC diagrams, MEBS scores, FeGenie tables, and HUMAnN
   pathways unlabeled
3. Low-completeness MAGs under-call pathways — filter with `mag-qc` first
4. Siderophores / secondary metabolites ≠ proven secretion (`fegenie` / `antismash`)

## Decision tree

```text
Element / biogeochem need?
│
├─ Broad C / N / S (+ other) on MAGs ± reads → metabolic
├─ Sulfur-focused scores (± N, O, CH₄, Fe) → mebs
├─ Iron genes / neighborhoods / siderophores → fegenie
├─ Distilled multi-DB metabolism sheets → dram
├─ KO / modules → kegg / eggnog-mapper
├─ CAZymes (organic C polymer) → dbcan
├─ GEMs → gapseq
└─ Unsure → this hub + microbial-mining
```

## Related skills

`metabolic` · `mebs` · `fegenie` · `dram` · `dbcan` · `kegg` ·
`eggnog-mapper` · `gapseq` · `alphagem` · `antismash` · `microbial-mining` ·
`tool-selection`
