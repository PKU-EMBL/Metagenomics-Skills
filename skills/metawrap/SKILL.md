---
name: metawrap
description: >
  Metagenomic wrapper for binning, refinement, reassembly, and related modules. Use this skill when working with metawrap: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/bxlab/metaWRAP. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['MAG', 'binning', 'metabat', 'maxbin']
upstream: https://github.com/bxlab/metaWRAP
---

# MetaWRAP

Upstream: [bxlab/metaWRAP](https://github.com/bxlab/metaWRAP)

## Analytical thinking

MetaWRAP is a **module suite**. For MAG recovery the critical path is
`binning` → `bin_refinement` (± `reassemble_bins`). Refinement consolidates
MetaBAT2/MaxBin2/(CONCOCT) predictions; refinement thresholds (`-c/-x`) are
scientific choices, not mere software defaults.

For cross-assembly refined recovery with contig-level DL screening, prefer
`basalt` instead of stopping at MetaWRAP.

Depth guidance: ~≥6 Gb/sample typical; complex soils often ≥30 Gb.

## How to run

```bash
metawrap binning -o temp/bin -t 32 \
  -a contigs.fa --metabat2 --maxbin2 \
  reads/*_1.fastq reads/*_2.fastq
# CONCOCT optional; costly

metawrap bin_refinement -o temp/bin_refine -t 32 \
  -A temp/bin/metabat2_bins/ \
  -B temp/bin/maxbin2_bins/ \
  -c 50 -x 10
```

Modes: mixed co-assembly, per-sample, or subgroup binning for huge cohorts.

## Decision tree

```text
MAG route?
├─ Classical multi-binner catalogue → metawrap (+ drep + coverm + gtdbtk)
└─ Multi-assembly refinement → basalt
```

## Related skills

`megahit` · `drep` · `coverm` · `gtdbtk` · `checkm2` · `basalt`

