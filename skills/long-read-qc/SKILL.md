---
name: long-read-qc
description: >-
  Plan and verify Oxford Nanopore or PacBio HiFi metagenomic read QC, including raw diagnostics, length/quality filtering, adapter removal, host depletion, and before-versus-after yield gates. Use when selecting NanoPlot, Chopper, Filtlong, HiFiAdapterFilt, or Hostile without applying short-read assumptions to long reads.
license: MIT
compatibility: Requires FASTQ input and POSIX shell; specialist tools are selected by platform.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "long-reads,nanopore,pacbio-hifi,qc,nanoplot,chopper,filtlong"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Long-read QC

Choose operations from the sequencing platform and downstream objective; do not copy Illumina thresholds.

## Routing

| Need | Preferred skill | Key boundary |
|---|---|---|
| Raw and post-filter diagnostics | `$nanoplot` | descriptive; does not clean reads |
| ONT quality/length filtering and trimming | `$chopper` | reads FASTQ; preserve modified-base tags only with deliberate options |
| Length/quality prioritization, optionally with short-read evidence | `$filtlong` | streams selected reads; no native report |
| PacBio HiFi adapter contamination | `$hifiadapterfilt` | PacBio-specific adapter filter |
| Human/host depletion | `$hostile` | reference choice controls false removal |
| General adapter/primer trimming | `$cutadapt` | adapter sequence must be known or justified |

For ONT, retain enough depth for assembly while removing clearly unusable reads. For HiFi, preserve high-accuracy reads and target residual adapters rather than imposing ONT-style quality cutoffs.

## Input contract

- platform and basecaller/CCS software version;
- FASTQ files with unique read IDs and unambiguous sample ownership;
- expected genome/community complexity and target output bases or depth;
- adapter model and host reference/index identity;
- whether modified-base tags must remain synchronized after trimming.

Inspect a small sample before setting thresholds. Quality encodings, ONT score calibration, and run chemistry change over time.

## Example staged execution

```bash
set -euo pipefail
in=${1:?usage: long-read-qc.sh reads.fastq.gz output_dir}
out=${2:?usage: long-read-qc.sh reads.fastq.gz output_dir}
[[ -s "$in" ]] || { echo "missing input: $in" >&2; exit 2; }
mkdir -p "$out"/{raw,filtered,logs}
NanoPlot --fastq "$in" --tsv_stats -t 8 -o "$out/raw" \
  >"$out/logs/nanoplot.raw.stdout.log" 2>"$out/logs/nanoplot.raw.stderr.log"
# ONT branch: choose thresholds from raw diagnostics and study requirements.
chopper -q 10 -l 1000 -i "$in" 2>"$out/logs/chopper.log" \
  | gzip >"$out/filtered/reads.q10.l1000.fastq.gz"
[[ -s "$out/filtered/reads.q10.l1000.fastq.gz" ]] || exit 3
NanoPlot --fastq "$out/filtered/reads.q10.l1000.fastq.gz" --tsv_stats -t 8 \
  -o "$out/filtered/nanoplot" >"$out/logs/nanoplot.filtered.stdout.log" \
  2>"$out/logs/nanoplot.filtered.stderr.log"
```

This is an ONT starting point, not a universal recommendation. For abundance-sensitive read profiling, aggressive length/quality selection can alter organism representation; quantify that effect.

## Quality gates

Compare raw and retained:

- read and base counts, retention fraction, N50, median length, and longest reads;
- quality-score distributions, not only a single mean;
- adapter and host-mapped fractions;
- read-ID uniqueness and parseability;
- assembly or profiling pilot outcomes at at least two defensible filtering settings.

Investigate zero output, implausibly high host removal, or large taxonomic shifts before continuing. Retain the unfiltered data and never overwrite it.

## Recovery and provenance

Streaming failures can leave valid-looking truncated gzip files. Validate with `gzip -t`, count records, and use a temporary file followed by `mv` in production. Capture tool versions, complete command, platform chemistry/basecaller, thresholds, reference checksums, input/output checksums, and observed retention metrics.

## Analytical thinking

Higher read N50 is not automatically better if filtering destroys depth or compositional representativeness. A clean exit is not a quality result. Report observed filtering outcomes separately from downstream biological interpretation.
