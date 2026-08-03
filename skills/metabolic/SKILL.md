---
name: metabolic
description: >
  METABOLIC (AnantharamanLab) — high-throughput metabolic and biogeochemical
  trait profiling of MAGs/SAGs/isolates with C, N, S, and other elemental cycle
  diagrams (METABOLIC-G genomes-only; METABOLIC-C with reads / community
  networks). Use for multi-element cycling potential and MW-score networks.
  Upstream: https://github.com/AnantharamanLab/METABOLIC. Route via
  element-cycling. Fe-deep dive → fegenie; S entropy scores → mebs.
license: MIT
category: analysis-tools
tags: [METABOLIC, biogeochemistry, C, N, S, P, element-cycling, MAG]
upstream: https://github.com/AnantharamanLab/METABOLIC
stage: mining
---

# METABOLIC

Upstream: [AnantharamanLab/METABOLIC](https://github.com/AnantharamanLab/METABOLIC)

## Citation

Zhou, Z. *et al.* METABOLIC: high-throughput profiling of microbial genomes for
functional traits, metabolism, biogeochemistry, and community-scale functional
networks. *Microbiome* **10**, 33 (2022).
https://doi.org/10.1186/s40168-021-01213-8

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

METABOLIC annotates genomes then draws **biogeochemical cycle** summaries —
commonly **carbon (C)**, **nitrogen (N)**, **sulfur (S)**, plus **other**
transformations (H₂, metals/metalloids as covered by the HMM/KOfam template).
Use **METABOLIC-G.pl** without reads; **METABOLIC-C.pl** when metagenomic reads
enable coverage / community contribution diagrams (MW-score, Sankey, networks).

| Element focus | Role of METABOLIC |
|---------------|-------------------|
| C | Fixation and organic C transformations |
| N | Fixation, nitrification, denitrification, anammox, … |
| S | Oxidative/reductive sulfur steps |
| P / H₂ / others | Via modules / “other” cycle panels — pin template version |
| Fe | Present at trait level; deep Fe → `fegenie` |

Heavy DB install (KOfam etc.). Pin METABOLIC version, module cutoff, and DB.

## How to run

```bash
# genomes only (example pattern — verify flags in installed wiki)
perl METABOLIC-G.pl -t 40 -m-cutoff 0.75 -in-gn Genome_files -kofam-db full -o METABOLIC_out
# with reads / community: METABOLIC-C.pl — see upstream wiki
```

## Decision tree

```text
Multi-element biogeochem on MAGs?
├─ Genomes ± reads → metabolic (G or C)
├─ S-centric entropy → mebs
├─ Fe genes/siderophores → fegenie
└─ Distilled sheets → dram
```

## Related skills

`element-cycling` · `mebs` · `fegenie` · `dram` · `kegg` · `gapseq` ·
`microbial-mining` · `tool-selection`
