---
name: bwa
description: >
  Burrows–Wheeler short-read alignment (BWA-MEM) to contigs/genomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, short-read"
  metagenomics.upstream: "https://github.com/lh3/bwa"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "BWA-MEM/Samtools paired-end template statically reviewed; not executed here"
---

# BWA / BWA-MEM

Upstream: [BWA / BWA-MEM](https://github.com/lh3/bwa)

## Citation

Li, H. & Durbin, R. Fast and accurate short read alignment with Burrows–Wheeler transform. *Bioinformatics* **25**, 1754–1760 (2009). https://doi.org/10.1093/bioinformatics/btp324

Li, H. Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM. *arXiv* (2013). https://doi.org/10.48550/arXiv.1303.3997

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classic alternative to Bowtie2 for coverage mapping. Prefer **bwa-mem2** on large cohorts when available; keep identical PE cleaned reads as used for assembly.

## How to run

Build an index with an explicit prefix and retain the exact reference checksum.

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

bwa index -p "$out/index/reference" "$ref" \
  >"$out/bwa-index.stdout.log" 2>"$out/bwa-index.stderr.log"
bwa mem -t "$threads" "$out/index/reference" "$r1" "$r2" \
  2>"$out/${id}.bwa.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/${id}.bam" -
samtools index "$out/${id}.bam"
```

## Key parameters

| `bwa mem -t` | threads | |
| index | `bwa index` | Once per reference |

## Decision notes

- Stage: **mapping** (short reads)
- Prefer `bwa-mem2` for speed when compatible; keep BWA when Methods require BWA-MEM
- Indexes ≠ Bowtie2 / strobealign

## Validation, recovery, and provenance

```bash
samtools quickcheck -v "$out/${id}.bam"
samtools view -H "$out/${id}.bam" | grep -q '^@HD.*SO:coordinate'
test -s "$out/${id}.bam.bai"
samtools flagstat -@ 4 -O tsv "$out/${id}.bam" >"$out/${id}.flagstat.tsv"
```

Inspect paired/primary mapping rates, insert-size behavior, reference contig
names, and depth distribution before coverage or binning. Failed streams can
leave partial BAMs, so publish/rename only after validation. Record BWA and
Samtools versions, reference/read checksums, read-group policy, full command,
logs, flagstat, and BAM checksum.

## Related skills

`bwa-mem2` · `bowtie2` · `samtools` · `coverm` · `tool-selection` ·
`metagenomics-workflow`
