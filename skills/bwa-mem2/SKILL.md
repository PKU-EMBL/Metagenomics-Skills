---
name: bwa-mem2
description: >
  Architecture-aware faster BWA-MEM for Illumina reads to contigs/genomes. Use when a
  BWA-MEM workflow is required but throughput must improve, or when migrating from
  classic bwa mem. Index format is NOT compatible with classic bwa index.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, short-read, bwa"
  metagenomics.upstream: "https://github.com/bwa-mem2/bwa-mem2"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "BWA-MEM2/Samtools paired-end template checked against upstream usage; not executed here"
---

# BWA-MEM2

Upstream: [bwa-mem2/bwa-mem2](https://github.com/bwa-mem2/bwa-mem2)

## Citation

Vasimuddin, M., Misra, S., Li, H. & Aluru, S. Efficient architecture-aware
acceleration of BWA-MEM for multicore systems. *IEEE IPDPS* 314–324 (2019).
https://doi.org/10.1109/IPDPS.2019.00041

Classic algorithm context: Li, H. Aligning sequence reads, clone sequences and
assembly contigs with BWA-MEM. *arXiv* (2013).
https://doi.org/10.48550/arXiv.1303.3997

## Analytical thinking

BWA-MEM2 keeps the **MEM mapping model** familiar to BWA users while speeding
alignment on modern CPUs. Critical pitfall: **`bwa-mem2 index` ≠ `bwa index`** —
never point `bwa-mem2 mem` at a classic BWA index (or the reverse).

For new metagenome coverage projects, `strobealign` or `bowtie2` may be simpler;
choose BWA-MEM2 when SOPs/scripts already assume BWA-MEM flags and SAM fields.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Index | From `bwa-mem2 index` | Rebuild if upgrading major version |
| RAM | Index ~ reference size class | Large co-assemblies need big nodes |

## How to run

Use a BWA-MEM2-specific index prefix; it is not interchangeable with classic
BWA index files.

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
mkdir -p "$out/index"

bwa-mem2 index -p "$out/index/reference" "$ref" \
  >"$out/bwa-mem2-index.stdout.log" 2>"$out/bwa-mem2-index.stderr.log"
bwa-mem2 mem -t "$threads" "$out/index/reference" "$r1" "$r2" \
  2>"$out/${id}.bwa-mem2.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/${id}.bam" -
samtools index "$out/${id}.bam"
```

## Key parameters

| Option | Guidance |
|--------|----------|
| `-t` | Threads |
| `-R` | Read group (`@RG`) when merging multi-lane BAMs |
| `-K` | Process chunk size; raise on huge inputs if supported |

## Decision tree

```text
Need BWA-MEM-like mapping?
├─ Legacy classic bwa only available → bwa
├─ Speed on modern CPUs → bwa-mem2
└─ Greenfield metagenome coverage → strobealign or bowtie2
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Index load errors | Rebuild with `bwa-mem2 index` |
| Divergent SM tags | Set `-R` consistently across lanes |
| Huge unsorted SAM | Stream to `samtools sort` (never dump SAM) |

## Validation, recovery, and provenance

```bash
samtools quickcheck -v "$out/${id}.bam"
samtools view -H "$out/${id}.bam" | grep -q '^@HD.*SO:coordinate'
test -s "$out/${id}.bam.bai"
samtools flagstat -@ 4 -O tsv "$out/${id}.bam" >"$out/${id}.flagstat.tsv"
```

Inspect paired/primary mapping rates, insert-size behavior, reference contig
names, and coverage distribution. Rebuild indexes after incompatible version or
format changes; never silently reuse classic BWA indexes. Preserve BWA-MEM2 and
Samtools versions, index/reference checksum, read checksums, commands, logs,
flagstat, BAM checksum, and read-group policy.

## Related skills

`bwa` · `bowtie2` · `strobealign` · `samtools` · `coverm` · `metabat2`
