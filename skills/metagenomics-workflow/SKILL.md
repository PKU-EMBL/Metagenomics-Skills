---
name: metagenomics-workflow
description: >
  End-to-end shotgun metagenomics pipeline guidance across individual tool skills.
  Use this skill when: (1) Starting a new project, (2) Ordering stages,
  (3) Integrating QC, profiling, assembly, and MAG recovery,
  (4) Planning compute and provenance.
  For choosing among tools, use tool-selection.
  For assembly/pooling design, use study-design.
license: MIT
category: orchestration
tags: [guidance, pipeline, workflow]
---

# Metagenomics Workflow

## Standard path (tool skills)

```text
study-design + setup
        │
        v
   fastp → kneaddata
        │
        ├─► metaphlan / humann / kraken2 ─► visualization
        │
        v
   megahit | metaspades
        │
        ├─► prodigal → cd-hit → salmon → eggnog-mapper (± rgi)
        │
        ├─► metawrap → drep → coverm → gtdbtk
        │
        └─► basalt
        │
        v
   checkm2 + mag-qc → visualization → Methods archive
```

## Phase checklist

### 1. Design & setup
- [ ] Manifest complete (`study-design`)
- [ ] Envs/DBs ready (`setup`)
- [ ] Acceptance criteria predeclared (`mag-qc`)

### 2. Reads
- [ ] `fastp` reports archived
- [ ] `kneaddata --reorder` + PE header check

### 3. Optional community tables
- [ ] Choose profiler via `tool-selection`
- [ ] Pin DB versions

### 4. Contigs / genes
- [ ] Assembly mode matches strata
- [ ] Catalogue thresholds reported (`cd-hit`)

### 5. Genomes
- [ ] `metawrap` **or** `basalt` (not confused)
- [ ] `drep` ANI stated if cataloguing
- [ ] `checkm2` filters applied

### 6. Report
- [ ] Figures labeled by method (`visualization`)
- [ ] Provenance bundle complete

## Related skills

`tool-selection` lists every software skill; load only those required by the phase.
