---
name: bbmap
description: >
  Fast splice-aware aligner and BBTools suite utilities (BBMerge, etc.). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, bbtools"
  metagenomics.upstream: "https://sourceforge.net/projects/bbmap/"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "BBMap/Samtools paired-end template statically reviewed; not executed here"
---

# BBMap

Upstream: [BBMap](https://sourceforge.net/projects/bbmap/)

## Citation

Bushnell, B. BBMap: a fast, accurate, splice-aware aligner. *LBNL Report* (2014). https://escholarship.org/uc/item/1h3515gn

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Useful Swiss-army mapper/utilities; for standard metagenome coverage prefer Bowtie2/strobealign unless BBMap is already standardized in the lab.

## How to run

```bash
set -Eeuo pipefail
id="${1:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
ref="${2:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
r1="${3:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
r2="${4:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
out="${5:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$ref" "$r1" "$r2"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

bbmap.sh ref="$ref" in1="$r1" in2="$r2" \
  out="$out/${id}.unsorted.bam" threads="$threads" \
  >"$out/${id}.bbmap.stdout.log" 2>"$out/${id}.bbmap.stderr.log"
samtools sort -@ "$threads" -o "$out/${id}.bam" "$out/${id}.unsorted.bam"
samtools index "$out/${id}.bam"
samtools quickcheck -v "$out/${id}.bam"
rm "$out/${id}.unsorted.bam"
```

## Key parameters

| `ref=` | contigs | |
| `out=` | BAM/SAM | |

## Decision notes

- Stage: **mapping** / utilities (BBTools suite)
- Prefer for specialized BBMerge/BBDuk tasks; for Illumina→contigs coverage prefer `strobealign` / `bowtie2`

## Validation, recovery, and provenance

Require a coordinate-sorted/indexed BAM and inspect BBMap statistics plus
`samtools flagstat`/`idxstats`. Confirm that paired inputs remained paired and
that the reference is the intended assembly. BBMap covers many utilities; do not
silently substitute BBDuk/BBMerge preprocessing for the study's declared QC
route.

Record BBMap/Java/Samtools versions, memory settings, reference/read checksums,
commands, logs, BAM checksum, and mapping summaries. Failed or changed runs
should use a fresh directory because index and temporary files may persist.

## Related skills

`bowtie2` · `samtools` · `coverm` · `tool-selection` · `metagenomics-workflow`
