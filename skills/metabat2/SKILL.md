---
name: metabat2
description: >
  Adaptive contig binning from tetranucleotide composition and multi-sample
  coverage. Use for primary single-binner runs feeding DAS Tool, MetaWRAP, or
  BASALT ensembles. Upstream: https://bitbucket.org/berkeleylab/metabat.
license: MIT
category: analysis-tools
tags: [binning, metabat, coverage]
upstream: https://bitbucket.org/berkeleylab/metabat
stage: binning
---

# MetaBAT 2

Upstream: [berkeleylab/metabat](https://bitbucket.org/berkeleylab/metabat)

## Citation

Kang, D. D. *et al.* MetaBAT 2: an adaptive binning algorithm for robust and
efficient genome reconstruction from metagenome assemblies. *PeerJ* **7**,
e7359 (2019). https://doi.org/10.7717/peerj.7359

## Analytical thinking

MetaBAT2 is the workhorse **single binner**. Quality hinges on **depth from
sorted BAMs** (`jgi_summarize_bam_contig_depths`) across samples that share the
assembly. One sample still works; multi-sample coverage usually improves
separation.

Treat MetaBAT2 bins as candidates — refine via `dastool` / `metawrap` /
`basalt` (recommended ensemble) and QC with `checkm2`.

Raise `-m` (min contig length) on huge assemblies to control runtime/noise;
document the threshold.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Contigs | Assembly FASTA | |
| BAMs | Sorted+indexed | From bowtie2/strobealign/bwa-mem2 |
| Depth | `jgi_summarize_bam_contig_depths` | Same contig headers |

## How to run

```bash
conda install -c bioconda metabat2 samtools

jgi_summarize_bam_contig_depths \
  --outputDepth temp/map/depth.txt \
  temp/map/*.bam

metabat2 -i contigs.fa -a temp/map/depth.txt \
  -o temp/bins/metabat/bin \
  -t 16 -m 1500 --seed 2024
```

## Key parameters

| Option | Guidance |
|--------|----------|
| `-a` | Depth table (required for multi-cov signal) |
| `-m` | Min contig length (1500–2500 common) |
| `-t` | Threads |
| `--seed` | Reproducibility |

## Outputs

`temp/bins/metabat/bin.*.fa` — feed to DAS Tool / CheckM2 / dRep.

## Decision tree

```text
Binning path?
├─ Only MetaBAT2 → ok for pilot; ensemble for catalogues
├─ Ensemble classical → metabat2 + maxbin2 (+ concoct) → dastool/metawrap
└─ Recommended related multi-assembly → basalt
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Empty bins | Depth contig IDs ≠ FASTA headers |
| Tiny bins only | Lower community signal / raise depth quality |
| RAM issues | Increase `-m`; run on high-mem node |

## Related skills

`bowtie2` · `strobealign` · `samtools` · `maxbin2` · `concoct` · `dastool` · `metawrap` · `basalt` · `checkm2`
