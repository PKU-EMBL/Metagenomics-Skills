---
name: coverm
description: >
  Calculate coverage/relative abundance of genomes or contigs. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "abundance, MAG, coverage"
  metagenomics.upstream: "https://github.com/wwood/CoverM"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# CoverM

Upstream: [wwood/CoverM](https://github.com/wwood/CoverM)

## Citation

Aroney, S. T. N. *et al.* CoverM: read alignment statistics for metagenomics. *Bioinformatics* **41**, btaf147 (2025). https://doi.org/10.1093/bioinformatics/btaf147

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CoverM unifies **per-contig** (binning inputs) and **per-genome** (community
profiling) coverage using Mosdepth-style arrays. Relative abundance (default
genome mode) scales mean coverages by the fraction of reads that align —
incomplete references leave many reads unmapped; CoverM accounts for that in
its relative-abundance formula.

Important defaults / assumptions from the paper:

- Genome presence filter: by default ≥**10%** of genome length covered ≥1× before
  assigning non-zero coverage (limits off-target hits in conserved regions).
- Relative abundance assumes roughly similar average genome sizes for mapped vs
  missing community members, and roughly complete/uncontaminated references.
- Near-identical references distort recruitment — CoverM can dereplicate with
  Galah using skani/FastANI/Dashing ANI before mapping.
- Aligners: strobealign / minimap2 / BWA; filter by identity, alignment length,
  or fraction of read aligned.

Relative abundance ≠ absolute load. Use the same dehosted reads that define
biological samples. Merge per-sample outputs carefully (headers differ by version).

## How to run

```bash
# genome relative abundance vs dereplicated MAGs
coverm genome --coupled ${id}_1.fastq ${id}_2.fastq \
  --genome-fasta-directory drep95/dereplicated_genomes/ -x fa \
  -t 8 -o temp/coverm/${id}.txt

# contig coverage for binning (example)
coverm contig -r contigs.fa --coupled ${id}_1.fastq ${id}_2.fastq \
  -t 8 -o temp/coverm/${id}.contig.tsv
```

## Key parameters

| Choice | Thinking |
|--------|----------|
| `genome` vs `contig` | Profiling vs binning coverage tables |
| method (mean / trimmed_mean / …) | Match what your binner expects |
| min covered fraction | Default ~10% genome; tighten for strict presence |
| mapper | `strobealign` often fastest for Illumina→large refs |

## Validation, recovery, and provenance

Require a non-empty table with unique sample/reference labels, finite non-negative values, and all intended samples. For contig binning, verify contig IDs exactly match the assembly and confirm the selected method/column layout is accepted by the binner. For genome abundance, report covered fraction, mapped/unmapped fraction, presence filter, identity/aligned-fraction filters, and multi-mapping policy; inspect unexpected zero/high values.

Rerun into a new output after changing catalogue, mapper, or filters. Capture `coverm --version`, complete command, read and reference checksums, dereplication manifest, mapper/version, table schema, and mapping logs. A non-zero genome abundance is a recruitment estimate, not proof of organism viability or absolute load.

## Related skills

`drep` · `skani` · `strobealign` · `gtdbtk` · `visualization` · `metabat2`
