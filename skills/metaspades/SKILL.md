---
name: metaspades
description: >
  More sensitive metagenomic assembly via SPAdes meta mode. Use this skill when working with metaspades: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/ablab/spades. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['assembly', 'spades']
upstream: https://github.com/ablab/spades
---

# metaSPAdes

Upstream: [ablab/spades](https://github.com/ablab/spades) (`metaspades.py`)

## Citation

Nurk, S., Meleshko, D., Korobeynikov, A. & Pevzner, P. A. metaSPAdes: a new versatile metagenomic assembler. *Genome Res.* **27**, 824–834 (2017). https://doi.org/10.1101/gr.213959.116

See also [docs/references.md](../../docs/references.md).

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

## Related skills

`megahit` · `prodigal` · `basalt` · `compute` via `setup`

