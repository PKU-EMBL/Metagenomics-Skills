---
name: tool-selection
description: >
  Guidance for choosing shotgun metagenomics analysis routes and tools.
  Use this skill when: (1) Deciding read-based vs assembly vs MAG recovery,
  (2) Choosing classical MetaWRAP-style binning vs BASALT,
  (3) Selecting MetaPhlAn vs Kraken vs HUMAnN,
  (4) Planning compute and deliverables for a new study.

  For detailed parameters, use the specific tool skills
  (preprocessing, read-based, gene-catalogue, mag-classical, basalt).
license: MIT
category: orchestration
tags: [guidance, tool-selection, workflow]
---

# Tool Selection

## Start from the deliverable

```text
What must the paper/table/genome set contain?
│
├─ Species/pathway tables from reads → read-based
│     ├─ Marker clades → MetaPhlAn4
│     ├─ Pathways/gene families → HUMAnN4
│     └─ k-mer / custom DB → Kraken2+Bracken
│
├─ Gene catalogue + function → gene-catalogue
│
├─ MAG catalogue
│     ├─ Classical multi-binner baseline → mag-classical
│     └─ Refined multi-assembly recovery → basalt
│
└─ Unsure → metagenomics-workflow + study-design
```

## Classical MAG vs BASALT

| Need | Prefer |
|------|--------|
| Standard MetaWRAP → dRep → GTDB catalogue | `mag-classical` |
| Cross-assembly selection + contig refinement + reassembly | `basalt` |
| New deployment with absolute paths / isolated outdirs | BASALT-Air (`basalt` skill) |
| Resume old Conda checkpoints | Conda BASALT |

## Comparison snapshot

| Route | Strengths | Weaknesses |
|-------|-----------|------------|
| Read-based | Fast composition/function | No genomes |
| Gene catalogue | Community gene content | Assembly bias |
| Classical MAGs | Mature ecosystem | Weaker cross-assembly refinement |
| BASALT | Multi-assembly refinement | Heavier setup/compute |

## Related skills

- `metagenomics-workflow` — ordered pipeline
- Individual tool skills for parameters
