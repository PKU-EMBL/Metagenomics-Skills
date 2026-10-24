---
name: strobealign
description: >
  Ultra-fast short-read alignment with flexible seed size for metagenome coverage
  mapping. Use when mapping many Illumina samples to large contig sets before binning,
  or when Bowtie2/BWA is the throughput bottleneck. Pair with samtools.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, short-read, coverage"
  metagenomics.upstream: "https://github.com/ksahlin/strobealign"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired-end alignment template checked against upstream usage; not executed here"
---

# strobealign

Upstream: [ksahlin/strobealign](https://github.com/ksahlin/strobealign)

## Citation

Sahlin, K. Strobealign: flexible seed size enables ultra-fast and accurate
read alignment. *Genome Biol.* **23**, 260 (2022).
https://doi.org/10.1186/s13059-022-02831-7

## Analytical thinking

strobealign is built for **modern short-read → large reference** workloads
typical of metagenomes (many Gb contigs × many samples). Accuracy is competitive
with BWA-MEM for this use case while often much faster — prefer it when mapping
dominates wall-clock before MetaBAT/SemiBin/VAMB.

Still enforce: sorted+indexed BAM, same cleaned reads as assembly coverage
design, and flagstat QC. Do not mix strobealign BAMs and Bowtie2 BAMs in one
depth table without documenting the switch.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| strobealign | bioconda build | Pin version in Methods |
| Contigs + PE reads | From assembly / KneadData | |
| Threads | 8 | 16–64 |

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
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

strobealign -t "$threads" "$ref" "$r1" "$r2" \
  2>"$out/${id}.strobealign.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/${id}.bam" -
samtools index "$out/${id}.bam"
```

On-the-fly indexing is the default. If using a persistent `.sti` index, verify
that it was generated from the exact reference and a compatible release.

## Key parameters

| Option | Guidance |
|--------|----------|
| `-t` | Threads |
| PE args | R1 R2 positional |
| read group | Add via samtools if downstream needs SM tags |

## Decision tree

```text
Need Illumina contig coverage for binning?
├─ Many samples / huge assembly → strobealign
├─ Match KneadData/Bowtie2 lab SOP → bowtie2
└─ Need classic BWA ecosystem → bwa-mem2
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Version CLI differs | Check `strobealign --help` for your build |
| Lower map rate vs Bowtie2 | Confirm same contigs/reads; compare flagstat |
| Pipe breaks mid-run | Ensure samtools sort tempdir has space |

## Validation, recovery, and provenance

```bash
samtools quickcheck -v "$out/${id}.bam"
samtools view -H "$out/${id}.bam" | grep -q '^@HD.*SO:coordinate'
test -s "$out/${id}.bam.bai"
samtools flagstat -@ 4 -O tsv "$out/${id}.bam" >"$out/${id}.flagstat.tsv"
```

Review paired/primary mapping, reference IDs, depth distribution, and a pilot
comparison when switching mapper families. Do not combine BAMs from different
references or undocumented alignment policies in one coverage matrix. Preserve
Strobealign/Samtools versions, reference/read checksums, index provenance,
commands, logs, BAM checksum, and QC table.

## Related skills

`bowtie2` · `bwa-mem2` · `samtools` · `metabat2` · `coverm` · `basalt`
