---
name: metawrap
description: >
  MetaWRAP suite for multi-binner MAG recovery and CheckM-style bin refinement — one
  option in the ensemble binning family (with DAS Tool and BASALT). Use this skill when
  working with metawrap: installing, choosing parameters, running
  binning/bin_refinement/reassemble_bins, or troubleshooting. Prefer basalt as the
  recommended ensemble default for related multi-assembly work; use dastool for
  classical contig2bin aggregation. For routing, use tool-selection.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MAG, ensemble-binning, binning, metabat, maxbin"
  metagenomics.upstream: "https://github.com/bxlab/metaWRAP"
---

# MetaWRAP

Upstream: [bxlab/metaWRAP](https://github.com/bxlab/metaWRAP)

## Citation

Uritskiy, G. V., DiRuggiero, J. & Taylor, J. MetaWRAP—a flexible pipeline for
genome-resolved metagenomic data analysis. *Microbiome* **6**, 158 (2018).
https://doi.org/10.1186/s40168-018-0541-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MetaWRAP is a **module suite** in the **ensemble binning** family (alongside
DAS Tool and BASALT). For MAG recovery the critical path is
`binning` → `bin_refinement` (± `reassemble_bins`). Refinement consolidates
MetaBAT2/MaxBin2/(CONCOCT) predictions; refinement thresholds (`-c/-x`) are
scientific choices, not mere software defaults.

**Recommended default in this package:** `basalt` (especially related samples /
multi-assembly refinement). Choose MetaWRAP when you want a classical packaged
multi-binner + refinement catalogue on a single assembly workflow. Choose
`dastool` when you already have contig2bin tables and only need SCG aggregation.

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

## Key parameters

| Module flag | Typical | Thinking |
|-------------|---------|----------|
| `--metabat2 --maxbin2` | on | Core pair; add CONCOCT if affordable |
| `bin_refinement -c/-x` | 50 / 10 | Publication-oriented; stricter → fewer bins |
| `reassemble_bins` | optional | Per-bin reassembly; validate with CheckM2 |

## Decision tree

```text
Ensemble MAG recovery?
├─ Recommended (related / multi-assembly) → basalt
├─ Packaged multi-binner + CheckM refinement suite → metawrap
└─ Classical SCG aggregation of contig2bin sets → dastool
```


## Literature notes (Microbiome 2018)

Uritskiy *et al.* position MetaWRAP as a **modular suite** (raw reads → bins →
bin analysis) with hybrid consolidation that outperformed individual binners and
other consolidation tools on synthetic and real data in that paper.

Operational takeaways for this package:

- Critical MAG path: `binning` → `bin_refinement` (± `reassemble_bins`).
- Refinement `-c/-x` (completeness/contamination) are **scientific thresholds** —
  report them; they are not universal truth.
- Modules are standalone — you may use refinement on bins from outside MetaWRAP.
- Reassembly can improve bins but costs CPU/IO; reserve for priority genomes.
- For related multi-assembly refinement beyond classical MetaBAT/MaxBin suites,
  prefer **`basalt`**; keep MetaWRAP when you want the packaged CheckM-era
  refinement catalogue.

## Related skills

`basalt` · `dastool` · `megahit` · `drep` · `coverm` · `gtdbtk` · `checkm2` · `mag-qc`
