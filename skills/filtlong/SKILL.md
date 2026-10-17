---
name: filtlong
description: >-
  Select long reads with Filtlong using minimum/maximum length, retained percentage or target bases, optionally weighting quality against paired short-read evidence. Use for assembly-oriented ONT/PacBio read prioritization when the retention objective is explicit.
license: MIT
compatibility: Requires Filtlong 0.3.1 and FASTA/FASTQ long reads; gzip is optional for output.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "filtlong,long-reads,filtering,target-bases,hybrid-assembly"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.3.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Filtlong

Filtlong scores long reads by length and quality and streams retained reads. It does not create a comprehensive QC report.

## Choose one explicit objective

- `--keep_percent`: retain a percentage of the highest-scoring reads;
- `--target_bases`: retain approximately a specified number of bases;
- `--min_length`/`--max_length`: hard length bounds;
- `-1` and `-2`: use accurate paired short reads as an external quality reference.

Do not combine aggressive objectives without calculating expected retained depth.

## Long-read-only run

```bash
set -euo pipefail
in=${1:?usage: filtlong.sh reads.fastq.gz output.fastq.gz}
out=${2:?usage: filtlong.sh reads.fastq.gz output.fastq.gz}
[[ -s "$in" ]] || { echo "missing reads: $in" >&2; exit 2; }
command -v filtlong >/dev/null
tmp="${out}.tmp.$$"
trap 'rm -f "$tmp"' EXIT
filtlong --min_length 1000 --keep_percent 90 --target_bases 500000000 \
  "$in" 2>"${out}.filtlong.log" | gzip >"$tmp"
gzip -t "$tmp"
[[ $(gzip -cd "$tmp" | awk 'END{print NR/4}') -gt 0 ]] || exit 3
mv "$tmp" "$out"
trap - EXIT
```

Hybrid evidence, where the short reads derive from the same biological sample:

```bash
filtlong -1 short_R1.fastq.gz -2 short_R2.fastq.gz --min_length 1000 \
  --keep_percent 90 --target_bases 500m --trim --split 500 long.fastq.gz \
  2>filtlong.log | gzip > long.filtered.fastq.gz
```

`--trim` and `--split` can alter long-range information; use them only for a defined reason. Decimal suffix semantics should be confirmed from `filtlong --help` for the pinned build.

## Verification

Validate compression and FASTQ record structure. Use `$nanoplot` to compare read count, total bases, N50, length/quality distributions, and longest-read retention. Calculate expected coverage only if target genome/community size is meaningful, and pilot assembly outcomes where possible.

## Recovery and provenance

Filtlong writes reads to stdout, so pipe failures can leave partial output. Always write to a temporary path, test it, then rename. Capture version/help output, complete command, input/output checksums, stderr score summary, and observed retained reads/bases.

## Analytical thinking

Filtlong optimizes a read-scoring objective, not taxonomic representativeness. In metagenomes, high-quality/long-read selection may favor abundant taxa and alter rare-population recovery. A larger N50 does not prove a better or less biased metagenome.

## Source

- https://github.com/rrwick/Filtlong
