---
name: pilon
description: >
  Polish genome assemblies and fix small errors using short-read BAM evidence. Use after
  mapping Illumina reads to a draft assembly (including long-read drafts).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "polish, assembly, short-read"
  metagenomics.upstream: "https://github.com/broadinstitute/pilon"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Bowtie2/Samtools/Pilon template statically reviewed; not executed here"
---

# Pilon

Upstream: [broadinstitute/pilon](https://github.com/broadinstitute/pilon)

## Citation

Walker, B. J. *et al.* Pilon: an integrated tool for comprehensive microbial
variant detection and genome assembly improvement. *PLoS ONE* **9**, e112963
(2014). https://doi.org/10.1371/journal.pone.0112963

## Analytical thinking

Pilon uses **short-read alignments** to correct SNPs/indels and optionally fill
gaps. Requires high-quality BAM (Bowtie2/BWA) to the draft. Over-polishing
heterogeneous metagenome contigs can erase true strain variation — prefer on
**isolate-like MAGs** or low-complexity drafts, not blindly on all community
contigs.

## How to run

Restrict polishing reads to the declared sample/population and write one
immutable round per output directory.

```bash
set -Eeuo pipefail
id="${1:?usage: pilon-round.sh SAMPLE_ID DRAFT R1 R2 OUTPUT_DIR}"
draft="${2:?usage: pilon-round.sh SAMPLE_ID DRAFT R1 R2 OUTPUT_DIR}"
r1="${3:?usage: pilon-round.sh SAMPLE_ID DRAFT R1 R2 OUTPUT_DIR}"
r2="${4:?usage: pilon-round.sh SAMPLE_ID DRAFT R1 R2 OUTPUT_DIR}"
out="${5:?usage: pilon-round.sh SAMPLE_ID DRAFT R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$draft" "$r1" "$r2"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/index"

bowtie2-build "$draft" "$out/index/draft" \
  >"$out/bowtie2-build.stdout.log" 2>"$out/bowtie2-build.stderr.log"
bowtie2 -x "$out/index/draft" -1 "$r1" -2 "$r2" -p "$threads" \
  2>"$out/bowtie2.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/illumina.bam" -
samtools index "$out/illumina.bam"
samtools quickcheck -v "$out/illumina.bam"

pilon --genome "$draft" --frags "$out/illumina.bam" \
  --output "${id}.pilon" --outdir "$out" --threads "$threads" --changes \
  >"$out/pilon.stdout.log" 2>"$out/pilon.stderr.log"
```

## Validation, recovery, and provenance

Require a non-empty `${id}.pilon.fasta`, a valid sorted/indexed BAM, completed
logs, and a reviewed changes file. Compare mapping/coverage, corrected SNP/indel
counts, assembly statistics, and independent k-mer/QV evidence before accepting
a round. Excess corrections in heterogeneous regions can signal strain collapse
or mis-mapping; do not polish all metagenome contigs blindly.

Keep the unmodified draft and every round. Rerun failed or changed parameters in
a new directory. Record Pilon/Java/mapper/Samtools versions, read and draft
checksums, mapping filters, full commands, logs, changes, and output checksum.

## Related skills

`bowtie2` · `samtools` · `racon` · `quast` · `megahit` · `metaflye`
