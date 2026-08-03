---
name: mag-classical
description: >
  Classical MAG recovery with multi-binner workflows (MetaWRAP-style).
  Use this skill when: (1) Binning with MetaBAT2/MaxBin2 via MetaWRAP,
  (2) Refining bins (completeness/contamination gates),
  (3) Dereplicating with dRep,
  (4) Quantifying genomes with CoverM,
  (5) Assigning taxonomy with GTDB-Tk.

  For refined multi-assembly MAGs, use basalt.
  For QC thresholds, use mag-qc.
license: MIT
category: analysis-tools
tags: [MAG, metawrap, drep, coverm, gtdbtk, binning]
---

# Classical MAG Recovery

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Depth | ~6 Gb/sample | ≥30 Gb for complex soils |
| Input | Contigs + PE reads | From `gene-catalogue` / assembly |
| RAM | 128 GB | 512 GB–1 TB for large mixed runs |

## Workflow

| Step | Tool | Key params |
|------|------|------------|
| Binning | MetaWRAP `binning` | `--metabat2 --maxbin2` |
| Refine | MetaWRAP `bin_refinement` | `-c 50 -x 10` |
| Dereplicate | dRep | `-sa 0.95` or `0.99`, `-nc 0.30`, `-comp 50`, `-con 10` |
| QC refresh | CheckM2 | especially if dRep skipped quality |
| Abundance | CoverM | `--coupled` PE |
| Taxonomy | GTDB-Tk | `classify_wf` |

## Modes

- **Mixed co-assembly binning** — more candidates; watch memory/time
- **Single-sample binning** — preserves sample-restricted populations
- **Subgroup binning** — when samples >30 or data >~300 Gb

## Example

```bash
metawrap binning -o temp/bin -t 32 \
  -a temp/megahit/final.contigs.fa \
  --metabat2 --maxbin2 temp/hr/*.fastq

metawrap bin_refinement -o temp/bin_refine -t 32 \
  -A temp/bin/metabat2_bins/ \
  -B temp/bin/maxbin2_bins/ \
  -c 50 -x 10

dRep dereplicate temp/drep95/ -g temp/drep_in/*.fa \
  -sa 0.95 -nc 0.30 -comp 50 -con 10 -p 16
```

## Decision tree

```text
Need refined cross-assembly recovery?
│
├─ Yes → use basalt
└─ No / baseline catalogue → mag-classical
```

## Related skills

- `mag-qc` — acceptance thresholds
- `basalt` — PKU-EMBL refinement path
- `visualization` — MAG figures
