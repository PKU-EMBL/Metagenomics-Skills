---
name: metagenomics-workflow
description: >
  End-to-end guidance for shotgun metagenomics pipelines.
  Use this skill when: (1) Starting a new metagenomics project,
  (2) Need step-by-step workflow guidance,
  (3) Integrating preprocessing, profiling, assembly, and MAG recovery,
  (4) Planning compute resources and timelines,
  (5) Assembling a Methods/provenance checklist.

  For tool choice, use tool-selection.
  For QC thresholds, use mag-qc.
license: MIT
category: orchestration
tags: [guidance, pipeline, workflow]
---

# Metagenomics Workflow

## Standard shotgun pipeline

```text
Metadata + PE reads
        │
        v
   preprocessing  (fastp → KneadData)
        │
        ├──────────────► read-based (MetaPhlAn/HUMAnN/Kraken)
        │
        v
   gene-catalogue (MEGAHIT → Prodigal → cd-hit → salmon → annotation)
        │
        ├──────────────► mag-classical (MetaWRAP → dRep → CoverM → GTDB)
        │
        └──────────────► basalt (multi-assembly refined MAGs)
        │
        v
   mag-qc → visualization → Methods / provenance archive
```

## Phase 1: Design and setup

**Skills**: `study-design`, `setup`

- [ ] Manifest complete (sample, stratum, host, assembly, coverage)
- [ ] Environments and databases verified
- [ ] Acceptance criteria predeclared

## Phase 2: Preprocessing

**Skill**: `preprocessing`

- [ ] fastp metrics archived
- [ ] Host depletion with `--reorder`
- [ ] PE headers verified
- [ ] Dehosted reads checksummed

## Phase 3: Community tables (optional)

**Skill**: `read-based`

- [ ] Profiler + DB version recorded
- [ ] No unlabeled merging of MetaPhlAn and Kraken

## Phase 4: Assembly / genes (optional)

**Skill**: `gene-catalogue`

- [ ] Assembly mode matches study design
- [ ] Clustering and quantification units stated

## Phase 5: Genomes (optional)

**Skills**: `mag-classical` or `basalt`, then `mag-qc`

- [ ] Route chosen via `tool-selection`
- [ ] Filters applied; not bin-count maximization

## Phase 6: Report

**Skill**: `visualization`

- [ ] Figures labeled by method
- [ ] Provenance bundle complete

## Resource planning (order-of-magnitude)

| Stage | Small (~6 Gb × 3) | Large (~10 Gb × 20) |
|-------|-------------------|---------------------|
| fastp | minutes | ~1 h |
| KneadData | minutes–hours | hours |
| HUMAnN | ~0.5–1 h | ~1 day |
| MEGAHIT | minutes–hours | ~0.5–1 day |
| MetaWRAP bin+refine | hours | ~1 day |
| BASALT | hours–days | days (dataset-dependent) |

## Related skills

All tool skills under this plugin; start with `tool-selection` if undecided.
