---
name: metaspades
description: >
  More sensitive metagenomic assembly via SPAdes meta mode. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, spades"
  metagenomics.upstream: "https://github.com/ablab/spades"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# metaSPAdes

Upstream: [ablab/spades](https://github.com/ablab/spades) (`metaspades.py`)

## Citation

Nurk, S., Meleshko, D., Korobeynikov, A. & Pevzner, P. A. metaSPAdes: a new versatile metagenomic assembler. *Genome Res.* **27**, 824–834 (2017). https://doi.org/10.1101/gr.213959.116

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

metaSPAdes often yields longer contigs than MEGAHIT at substantially higher
memory/time cost. Use it when continuity of medium/low-abundance genomes matters
and hardware allows. Hybrid Illumina+long-read modes exist—record which reads
entered assembly vs coverage.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 100 GB+ typical | 500 GB–1 TB large |
| CPU | 16 | 32+ |
| Input | Dehosted PE (± long) | Clean PE from `kneaddata` |

## How to run

```bash
metaspades.py -t 32 -m 500 \
  -1 s1_1.fastq -2 s1_2.fastq \
  -o temp/metaspades
# multi-library: repeat -1/-2 pairs per SPAdes docs
```

Primary contigs usually at `temp/metaspades/contigs.fasta`.

## Decision tree

```text
Assembly priority?
├─ Speed/memory → megahit
├─ Continuity / hybrid short+long → metaspades
└─ Already have good contigs → skip; go to prodigal / metawrap / basalt
```

## Validation, recovery, and provenance

Require non-empty `contigs.fasta`, completed `spades.log`, and no unresolved fatal/warning condition. Inspect contig/scaffold metrics with `$quast`, read recruitment, total assembled bases, graph/coverage artifacts, and low-coverage or extreme-GC contigs. Compare against MEGAHIT on a pilot when continuity materially affects recovery.

SPAdes supports `--continue`/`--restart-from` only under documented constraints; never alter inputs or incompatible parameters inside a resumed output directory. Preserve input library definitions, SPAdes version, complete command, `params.txt`, `spades.log`, resource use, contig checksum, and the assembly graph/path files needed by graph-aware tools such as `$metacoag`.

## Related skills

`megahit` · `prodigal` · `basalt` · `compute` via `setup`

