---
name: metabat2
description: >
  Adaptive contig binning from tetranucleotide composition and multi-sample coverage.
  Use for primary single-binner runs feeding DAS Tool, MetaWRAP, or BASALT ensembles.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, metabat, coverage"
  metagenomics.upstream: "https://bitbucket.org/berkeleylab/metabat"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
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

## Validation, recovery, and provenance

Require a non-empty depth table and either candidate FASTAs or an explicit no-bin result. Confirm depth/FASTA contig IDs and lengths agree, every BAM maps against the same assembly, bin contigs are unique across MetaBAT2 outputs, and all binned contigs satisfy `-m`. Tabulate binned/unbinned bases, per-bin size/coverage, and downstream CheckM2/GUNC results; do not select bins by count alone.

Generate depth and bins into fresh paths after changing BAMs, assembly, `-m`, or seed. Record MetaBAT2/samtools/mapper versions, seed and command, assembly/BAM checksums, sample-to-BAM manifest, depth-table checksum, and candidate-bin checksums. A MetaBAT2 bin is a composition/coverage hypothesis, not a validated genome.

## Related skills

`bowtie2` · `strobealign` · `samtools` · `maxbin2` · `concoct` · `dastool` · `metawrap` · `basalt` · `checkm2`
