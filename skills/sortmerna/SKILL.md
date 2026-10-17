---
name: sortmerna
description: >-
  Separate ribosomal from non-ribosomal reads in metatranscriptomic or total-RNA data with SortMeRNA using one or more pinned rRNA references. Use when paired-read handling, reusable indexes/workdirs, and aligned/non-aligned output validation are required.
license: MIT
compatibility: Requires SortMeRNA 7.1.0, FASTA/FASTQ reads, rRNA reference FASTA, and sufficient temporary storage/memory.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "sortmerna,rrna,metatranscriptomics,rna-filtering,paired-reads"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "7.1.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# SortMeRNA

SortMeRNA aligns reads to rRNA references and can emit aligned (rRNA) and other (non-rRNA) reads. Pin the reference release and pairing policy.

## Inputs

- one or more rRNA reference FASTAs (for example pinned SILVA-derived sets);
- single or paired FASTQ/FASTA, compressed or plain;
- a persistent work directory for reusable indexes;
- declared treatment of a pair when only one mate aligns.

Reference choice determines depletion breadth and off-target risk. Do not label all non-aligned reads as mRNA.

## Paired-end run

```bash
set -euo pipefail
r1=${1:?usage: sortmerna-pe.sh R1.fastq.gz R2.fastq.gz rrna.fasta output_dir}
r2=${2:?usage: sortmerna-pe.sh R1.fastq.gz R2.fastq.gz rrna.fasta output_dir}
ref=${3:?usage: sortmerna-pe.sh R1.fastq.gz R2.fastq.gz rrna.fasta output_dir}
out=${4:?usage: sortmerna-pe.sh R1.fastq.gz R2.fastq.gz rrna.fasta output_dir}
[[ -s "$r1" && -s "$r2" && -s "$ref" ]] || exit 2
mkdir -p "$out/work"
sortmerna --ref "$ref" --reads "$r1" --reads "$r2" \
  --workdir "$out/work" --aligned "$out/rRNA" --other "$out/non_rRNA" \
  --fastx --paired_out --out2 --threads 16 \
  >"$out/sortmerna.stdout.log" 2>"$out/sortmerna.stderr.log"
find "$out" -maxdepth 1 -type f \( -name 'non_rRNA*' -o -name 'rRNA*' \) -print \
  >"$out/output_files.txt"
grep -q 'non_rRNA' "$out/output_files.txt" || exit 3
```

With `--paired_out`, if only one mate aligns, both mates are assigned to the non-rRNA/`other` side, favoring purity of the rRNA output while allowing some rRNA into retained pairs. `--paired_in` makes the opposite trade-off. Document the choice. `--out2` requests separate paired files.

For multiple references, repeat `--ref`. Reuse the same workdir only for the same reference set/version; keep sample outputs separate.

## Validation

- enumerate actual release-specific output names and test FASTQ structure/compression;
- verify paired outputs have equal record counts and synchronized IDs;
- reconcile input pairs with aligned/other allocation under the selected pair policy;
- report rRNA and retained fractions by reads and bases;
- inspect the execution trace for progress and completion;
- classify a subset of retained reads for residual rRNA.

An empty non-rRNA output may be biologically possible but demands checking references, pair policy, and logs. A stalled non-progressing trace is not a successful long run.

## Recovery and provenance

Keep work/index directories and logs, but use a new workdir when reference files change. Capture `sortmerna --version`, command, reference checksums/release, input/output checksums, pairing options, and observed counts.

## Analytical thinking

SortMeRNA is a local aligner; depletion sensitivity and specificity depend on references and thresholds. Non-rRNA contains mRNA plus other RNA, DNA contamination, and unrecognized rRNA. Do not interpret retention as expressed coding sequence without downstream assignment.

## Source

- https://github.com/sortmerna/sortmerna
