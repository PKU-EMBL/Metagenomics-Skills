# Standard pipeline

End-to-end shotgun metagenomics using **per-software skills**.

## Overview

```text
fastp → kneaddata
   ├─► metaphlan / humann / kraken2
   └─► megahit|metaspades → prodigal → cd-hit → salmon → eggnog-mapper
                              ├─► metawrap → drep → coverm → gtdbtk
                              └─► basalt
                         checkm2 + mag-qc → visualization
```

## Phase notes (thinking)

1. **Design first** (`study-design`) — assembly mode is a biological decision.
2. **QC before biology** (`fastp`, `kneaddata`) — bad PE pairing poisons everything downstream.
3. **Profiling vs genomes** — read-based tables do not replace MAGs; do not merge profiler types.
4. **Assembler choice** — MEGAHIT for throughput; metaSPAdes when continuity budget exists.
5. **MAG route** — MetaWRAP for classical catalogues; BASALT for related multi-assembly refinement.
6. **Filters before claims** (`checkm2`, `mag-qc`, `drep` ANI).

## Skill map by phase

| Phase | Skills |
|-------|--------|
| Design/setup | `study-design`, `setup` |
| Reads | `fastp`, `kneaddata` |
| Profiles | `metaphlan`, `humann`, `kraken2` |
| Contigs/genes | `megahit`, `metaspades`, `prodigal`, `cd-hit`, `salmon`, `eggnog-mapper`, `rgi` |
| MAGs | `metawrap`, `basalt`, `drep`, `coverm`, `gtdbtk`, `checkm2` |
| Report | `mag-qc`, `visualization` |
