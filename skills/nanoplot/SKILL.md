---
name: nanoplot
description: >-
  Generate diagnostic plots and machine-readable summary statistics for Oxford Nanopore or other long-read FASTQ, sequencing-summary, or BAM inputs with NanoPlot. Use for raw-versus-filtered read length, quality, yield, and alignment QC; not for filtering reads.
license: MIT
compatibility: Requires NanoPlot 1.48.x, Python environment, and FASTQ/summary/BAM input.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "nanoplot,nanopore,long-reads,qc,read-length,quality"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.48.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# NanoPlot

NanoPlot summarizes long-read length and quality distributions. It does not trim or filter reads.

## Input contract

Choose exactly the input mode that matches the data: `--fastq`, `--summary`, or `--bam`. Keep raw and post-filter reports in separate directories. For large runs, decide whether downsampling is acceptable and record it.

## FASTQ execution

```bash
set -euo pipefail
reads=${1:?usage: nanoplot.sh reads.fastq.gz output_dir}
out=${2:?usage: nanoplot.sh reads.fastq.gz output_dir}
[[ -s "$reads" ]] || { echo "missing FASTQ: $reads" >&2; exit 2; }
command -v NanoPlot >/dev/null
mkdir -p "$out"
NanoPlot --fastq "$reads" --threads 8 --tsv_stats --info_in_report \
  --loglength --plots dot -o "$out" \
  >"$out/NanoPlot.stdout.log" 2>"$out/NanoPlot.stderr.log"
[[ -s "$out/NanoStats.txt" && -s "$out/NanoPlot-report.html" ]] || {
  echo "NanoPlot outputs incomplete" >&2; exit 3;
}
grep -E 'Number of reads|Total bases|Read length N50|Mean read quality' \
  "$out/NanoStats.txt" || true
```

Alternative upstream-documented modes include:

```bash
NanoPlot --summary sequencing_summary.txt --loglength -o nanoplot-summary
NanoPlot --bam alignments.bam --downsample 100000 -t 8 -o nanoplot-bam
```

Do not combine heterogeneous runs merely to simplify plotting; summarize per sample/run before aggregation.

## Validation

- inspect `NanoStats.txt`, `NanoStats.tsv` when generated, HTML, and image files;
- compare number of reads/bases with an independent FASTQ counter;
- examine the full distributions for multimodality, low-quality tails, and truncation;
- compare raw and filtered data using retention in both reads and bases;
- note downsampling or maximum-length clipping in every figure caption.

A successful report with zero or implausibly few reads usually indicates wrong input mode, malformed/compressed input, or aggressive upstream filtering.

## Provenance and recovery

Capture `NanoPlot --version`, command, input checksum, output directory, and stdout/stderr. Delete or rename a partial output directory before rerunning with changed inputs; do not mix plots from multiple attempts.

## Analytical thinking

N50 and mean quality are descriptive, not acceptance criteria by themselves. Filtering that improves N50 can reduce depth or alter taxonomic representation. Select thresholds from downstream performance and study goals, then report observed trade-offs.

## Source

- https://github.com/wdecoster/NanoPlot
