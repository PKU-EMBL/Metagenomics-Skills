---
name: chopper
description: >-
  Filter and trim Oxford Nanopore FASTQ reads by mean quality and length with Chopper, including quality-based trimming modes and modified-base-tag cautions. Use when a fast streaming ONT filter is needed after inspecting raw read distributions.
license: MIT
compatibility: Requires Chopper 0.14.x and FASTQ input; gzip/pigz is recommended for compression.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "chopper,nanopore,long-read,quality-filtering,trimming,fastq"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.14.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Chopper

Use Chopper after `$nanoplot` or equivalent diagnostics. Thresholds are platform/run dependent.

## Preflight and inputs

```bash
command -v chopper >/dev/null
chopper --version
chopper --help > chopper.help.txt
```

Require FASTQ (not FASTA), declared minimum read length, minimum mean Phred quality, and a rationale tied to assembly/profiling needs. Preserve raw reads.

## Streaming filter

```bash
set -euo pipefail
in=${1:?usage: chopper-filter.sh reads.fastq.gz filtered.fastq.gz}
out=${2:?usage: chopper-filter.sh reads.fastq.gz filtered.fastq.gz}
[[ -s "$in" ]] || { echo "missing input: $in" >&2; exit 2; }
tmp="${out}.tmp.$$"
trap 'rm -f "$tmp"' EXIT
chopper -q 10 -l 1000 -i "$in" 2>"${out}.chopper.log" | gzip >"$tmp"
gzip -t "$tmp"
[[ $(gzip -cd "$tmp" | awk 'END{print NR%4}') -eq 0 ]] || exit 3
[[ $(gzip -cd "$tmp" | awk 'END{print NR/4}') -gt 0 ]] || exit 3
mv "$tmp" "$out"
trap - EXIT
```

Upstream trimming modes include:

```bash
chopper --trim-approach trim-by-quality --cutoff 15 -i reads.fastq > trimmed.fastq
chopper --trim-approach best-read-segment --cutoff 15 -l 100 -i reads.fastq > best.fastq
chopper --trim-approach split-by-low-quality --cutoff 15 --split-window 5 \
  -l 50 -i reads.fastq > split.fastq
```

If trimming reads that carry ONT modified-base `MM`, `ML`, and `MN` tags, inspect current `--update-mods` behavior and validate tags downstream. Updating tags does not make quality trimming modification-aware.

## Verify

Run `$nanoplot` before and after. Report read/base retention, N50, median length, quality distribution, and number of zero-length/malformed records. Pilot downstream assembly or profiling at alternate thresholds if results are threshold-sensitive.

If a pipe fails, a gzip file may still exist; the temporary-file pattern prevents it from replacing a valid output. Keep stderr and capture `chopper --version`.

## Analytical thinking

A Q10/1-kb command is an example, not a universal gate. Mean-quality filtering can retain reads with poor local segments and discard useful depth. Splitting or trimming changes read IDs/coordinates and may affect modified-base analyses and long-range assembly evidence.

## Source

- https://github.com/wdecoster/chopper
