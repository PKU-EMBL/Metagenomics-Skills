---
name: metagenomics-workflow
description: >
  End-to-end shotgun metagenomics: quality control, assembly, mapping, binning,
  taxonomic annotation, functional annotation, and microbial mining (BGCs, AMR,
  MGEs/viruses, AMPs, metabolism, defense). Use when starting a project or
  ordering stages. For tool choice use tool-selection. For mining routes use
  microbial-mining. For public DBs use public-databases.
license: MIT
category: orchestration
tags: [guidance, pipeline, workflow, QC, assembly, mapping, binning, taxonomy, function, mining]
---

# Metagenomics Workflow

Organize by **scientific stage**. Mapping sits between assembly and binning.
Microbial mining is an optional discovery track on contigs/MAGs.

## Path

```text
study-design + setup (+ public-databases)
        │
        v
1 QC      fastp → kneaddata
        │
        ├─► 5 taxonomy / 6 function (reads) ─► visualization
        │
        v
2 Assembly   megahit | metaspades | metaflye | metamdbg
        │
        v
3 Mapping    bowtie2 | bwa-mem2 | strobealign | minimap2 → samtools
        │
        ├─► 6 function (genes)
        │
        v
4 Binning    single binners → basalt ★ | metawrap | dastool
             → drep → coverm → checkm2 / gunc / mag-qc
        │
        ├─► 5 taxonomy (genomes): gtdbtk
        ├─► 6 function (genomes): bakta / prokka / eggnog-mapper / rgi
        └─► 7 microbial mining: antismash / genomad / dram / …
        │
        v
   visualization → Methods archive
```

## Checklist

- [ ] Design & DB plan
- [ ] QC + PE order
- [ ] Assembly + QUAST glance
- [ ] Sorted BAM coverage
- [ ] Ensemble binning route declared (`basalt` recommended)
- [ ] Taxonomy / function layers not merged unlabeled
- [ ] If mining: route via `microbial-mining`; pin DBs; state hypothesis limits
- [ ] Provenance: software **and** database releases

## Related skills

`tool-selection` · `microbial-mining` · `public-databases` · stage skills under `skills/`
