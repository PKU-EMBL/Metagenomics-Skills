---
name: samtools
description: >
  SAM/BAM/CRAM processing for metagenomic mapping outputs — sort, index, flagstat,
  coverage, and filtering. Use whenever an aligner writes SAM/BAM before CoverM,
  MetaBAT2, inStrain, or BASALT.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, bam, sam, qc"
  metagenomics.upstream: "https://github.com/samtools/samtools"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# Samtools

Upstream: [samtools/samtools](https://github.com/samtools/samtools)

## Citation

Danecek, P. *et al.* Twelve years of SAMtools and BCFtools. *GigaScience* **10**,
giab008 (2021). https://doi.org/10.1093/gigascience/giab008

## Analytical thinking

Aligners produce records; **samtools makes them usable**. Binning and CoverM
expect coordinate-sorted, indexed BAMs. Always stream `aligner | samtools sort`
to avoid multi-hundred-GB unsorted SAM files.

flagstat / coverage are your first QC after mapping — catch wrong references
before spending days on MetaBAT/BASALT.

## Essential recipes

```bash
# Sort + index (canonical)
samtools sort -@ 8 -o out.bam in.sam   # or stdin from aligner
samtools index out.bam

# Mapping QC
samtools flagstat out.bam
samtools idxstats out.bam | head
samtools coverage out.bam | head

# Keep primary mapped only (optional cleanup)
samtools view -@ 8 -b -F 0x900 out.bam > out.primary.bam

# Merge lanes (same sample)
samtools merge -@ 8 sample.bam L1.bam L2.bam && samtools index sample.bam
```

## Key options

| Option | Guidance |
|--------|----------|
| `-@` | Threads for CPU-heavy ops |
| `-o` | Output path (sort/view) |
| `-F/-f` | Flag filters; know 0x4 unmapped, 0x900 secondary/supplementary |
| `TMPDIR` | Point to large scratch for sort |

## Decision notes

- Never feed unsorted BAM to MetaBAT depth helpers expecting coordinate order
- Archive flagstat next to BAM for provenance
- CRAM saves space but ensure reference FASTA remains available

## Validation, recovery, and provenance

```bash
set -euo pipefail
samtools quickcheck -v out.bam
samtools view -H out.bam | grep -q '^@HD.*SO:coordinate'
[[ -s out.bam.bai ]] || exit 3
samtools flagstat -@ 4 -O tsv out.bam > out.flagstat.tsv
samtools idxstats out.bam > out.idxstats.tsv
```

Check reference names/lengths against the exact FASTA index, expected sample/read groups, primary/secondary/supplementary policy, mapped-pair fraction, and duplicate handling. Write sort/merge outputs to temporary paths and rename only after `quickcheck` and indexing; failed streams can leave parseable-looking partial files.

Record samtools and mapper versions, reference checksum, command/flags, input/output checksums, header, and flagstat/idxstats. CRAM provenance must retain the exact reference FASTA.

## Related skills

`bowtie2` · `strobealign` · `bwa-mem2` · `minimap2` · `coverm` · `metabat2` · `instrain`
