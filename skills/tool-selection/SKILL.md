---
name: tool-selection
description: >
  Choose shotgun metagenomics tools and routes by scientific deliverable.
  Use this skill when: (1) Deciding which software skill to load,
  (2) Choosing MetaPhlAn vs Kraken vs HUMAnN,
  (3) Choosing MEGAHIT vs metaSPAdes,
  (4) Choosing MetaWRAP vs BASALT for MAGs,
  (5) Planning a multi-tool analysis path.
  For end-to-end ordering, use metagenomics-workflow.
license: MIT
category: orchestration
tags: [guidance, tool-selection, workflow]
---

# Tool Selection

## Start from the deliverable

```text
Deliverable?
│
├─ Clean PE reads
│     fastp → kneaddata
├─ Taxonomic composition from reads
│     metaphlan  OR  kraken2 (+ bracken)
├─ Pathways / gene families from reads
│     humann
├─ Contigs
│     megahit (default) OR metaspades (heavier)
├─ Gene catalogue + function
│     prodigal → cd-hit → salmon → eggnog-mapper (± rgi)
├─ Classical MAG catalogue
│     metawrap → drep → coverm → gtdbtk  (+ checkm2 / mag-qc)
└─ Refined multi-assembly MAGs
      basalt  (+ checkm2 / mag-qc)
```

## Head-to-head thinking

| Choice | Prefer A when… | Prefer B when… |
|--------|----------------|----------------|
| MetaPhlAn vs Kraken2 | Marker specificity | Custom DB / speed / contig classify |
| MEGAHIT vs metaSPAdes | Time/memory limited | Continuity / hybrid assembly budget |
| MetaWRAP vs BASALT | Standard multi-binner catalogue | Related multi-assembly refinement |
| Conda BASALT vs Air | Resume old runs | New absolute-path deployments |

## Never

- Merge MetaPhlAn and Kraken into one unlabeled table
- Treat `more-sensitive` / more binners as guaranteed better MAGs
- Pool unrelated samples only to increase assembly depth

## Related skills

Every tool skill under `skills/` · `metagenomics-workflow` · `study-design`
