---
name: read-based
description: >
  Read-based taxonomic and functional profiling for shotgun metagenomes.
  Use this skill when: (1) Running MetaPhlAn4 clade profiles,
  (2) Running HUMAnN4 gene-family/pathway abundances,
  (3) Running Kraken2 + Bracken,
  (4) Choosing among marker, pathway, and k-mer methods,
  (5) Preparing tables for differential analysis.

  For assembly-based genes, use gene-catalogue.
  For figures, use visualization.
license: MIT
category: analysis-tools
tags: [humann, metaphlan, kraken2, taxonomy, function]
---

# Read-Based Profiling

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Host-depleted PE | From `preprocessing` |
| RAM | 32 GB | 64–128 GB |
| Databases | MetaPhlAn/HUMAnN and/or Kraken | Version-pinned |

## Profiler selection

| Question | Prefer | Why |
|----------|--------|-----|
| Marker-based species/clades | MetaPhlAn4 | Specificity on PE data |
| Gene families + pathways | HUMAnN4 | Joint taxonomy/function |
| Broad k-mer / custom DB | Kraken2 + Bracken | Throughput; DB-limited |
| Group biomarkers | LEfSe / MaAsLin2 / STAMP | Needs clear groups |

**Do not merge MetaPhlAn and Kraken into one unlabeled table.**

## How to run (conceptual order)

1. Complete `preprocessing`
2. Merge PE for HUMAnN if required by the chosen workflow
3. HUMAnN4 → MetaPhlAn tables + pathway/gene-family tables
4. Optional Kraken2 → Bracken
5. Optional LEfSe on declared metadata groups
6. Hand off to `visualization`

## Interpretive limits

| Product | Means | Does not mean |
|---------|-------|---------------|
| Relative abundance | Composition estimate | Absolute load |
| HUMAnN pathway | Homology-supported potential | Measured flux |
| Bracken species | Model redistributed reads | Exhaustive inventory |

## Related skills

- `preprocessing` — required upstream
- `visualization` — alpha/beta and biomarker plots
- `tool-selection` — when to leave read-based for MAGs
