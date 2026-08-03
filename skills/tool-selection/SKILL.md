---
name: tool-selection
description: >
  Choose shotgun tools by stage: QC, assembly, mapping, binning, taxonomic
  annotation, functional annotation, and microbial mining. Use when deciding
  which skill to load — mappers, assemblers, ensemble binning (BASALT
  recommended), profilers, or miners (antiSMASH, geNomad, DRAM, RGI, …).
  For stage order use metagenomics-workflow. For mining goals use microbial-mining.
license: MIT
category: orchestration
tags: [guidance, tool-selection, mapping, binning, mining, workflow]
---

# Tool Selection

Start from the **stage**, then the deliverable.

## By stage

```text
1 QC       fastp · kneaddata · fastqc · cutadapt · trimmomatic
2 Assembly megahit · metaspades · metaflye · metamdbg  (+ quast)
3 Mapping  strobealign | bowtie2 | bwa-mem2 | bwa | minimap2 · samtools · diamond
4 Binning  metabat2 · maxbin2 · concoct · semibin2 · vamb
           → basalt ★ · metawrap · dastool → drep · coverm · checkm2 · gunc
5 Taxonomy metaphlan · kraken2+bracken · motus · sylph · kaiju · gtdbtk
6 Function humann · prodigal · bakta · prokka · cd-hit · mmseqs2 · salmon
           · eggnog-mapper · rgi
7 Mining   microbial-mining → antismash · genomad · virsorter2 · checkv
           · macrel · dram · gapseq · deeparg · defensefinder
```

## Mining head-to-head

| Goal | Prefer |
|------|--------|
| BGCs / natural products | `antismash` |
| Resistome | `rgi` (± `deeparg`) |
| Plasmids / viruses / MGEs | `genomad` (± `virsorter2` → `checkv`) |
| AMPs | `macrel` |
| Distilled metabolism | `dram` |
| Metabolic models | `gapseq` |
| Defense systems | `defensefinder` |

## Ensemble binning

| Skill | When |
|-------|------|
| `basalt` | **Recommended** multi-assembly refinement |
| `metawrap` | Packaged multi-binner suite |
| `dastool` | Aggregate contig2bin tables |

## Never

- Skip mapping when binning needs coverage
- Merge taxonomy methods unlabeled
- Treat mining hits as validated products/phenotypes
- Call bins MAGs before QC filters

## Related skills

`metagenomics-workflow` · `microbial-mining` · `study-design` · `public-databases`
