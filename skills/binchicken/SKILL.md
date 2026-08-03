---
name: binchicken
description: >
  Bin Chicken — targeted coassembly planning for recovering low-abundance /
  novel MAGs by grouping metagenomes that share marker-gene signal (SingleM).
  Use when: (1) Public or large cohorts where all-vs-all coassembly is impossible,
  (2) Prioritizing sample subsets for coassembly to recover rare lineages,
  (3) Novelty-focused recovery against reference genomes, (4) Study-design of
  coassembly strata. Upstream: https://github.com/AroneyS/binchicken.
  For general coassembly vs individual design use study-design.
  For binning after coassembly use basalt / metabat2 / etc.
license: MIT
category: analysis-tools
tags: [coassembly, low-abundance, BinChicken, SingleM, MAG]
upstream: https://github.com/AroneyS/binchicken
stage: assembly
---

# Bin Chicken

Upstream: [AroneyS/binchicken](https://github.com/AroneyS/binchicken)

## Citation

Aroney, S. T. N., Newell, R. J. P., Tyson, G. W. & Woodcroft, B. J. Bin Chicken:
targeted metagenomic coassembly for the efficient recovery of novel genomes.
*Nat. Methods* (2025). https://doi.org/10.1038/s41592-025-02901-1

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Low-abundance genomes are often **below recoverable coverage in any single
sample**. Blind coassembly of many samples increases graph complexity and
compute; random subsets explode combinatorially.

Bin Chicken plans **targeted coassemblies**: match SingleM marker sequences
across metagenomes, optionally prioritize markers divergent from references,
then greedily cluster samples into coassembly groups. It is a **sample-selection
/ assembly-planning** tool — not a replacement for MetaBAT2/BASALT after
contigs exist.

Use when:

- Mining public repositories or large private cohorts for rare/novel lineages
- You need a principled alternative to metadata-only pooling
- You want novelty-weighted recovery (markers distant from known genomes)

Do **not** use Bin Chicken to justify pooling unrelated biological strata for a
single hypothesis-driven contrast study — see `study-design`.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Inputs | Many metagenomes (reads) + SingleM/Bin Chicken DB stack |
| Compute | Coassembly of selected groups still expensive — plan RAM |
| Downstream | Assemble groups → map → bin (`basalt` ★ / single binners) → QC |

## How to run

Confirm subcommands against upstream (workflow is multi-step):

```bash
# high-level pattern — see upstream docs for exact CLI
binchicken \
  # 1) singlem / marker search across samples
  # 2) cluster samples into coassembly targets
  # 3) emit assembly recipes / sample lists
```

Then run your assembler (`megahit` / `metaspades`) on each planned group and
continue with mapping + binning.

## Decision tree

```text
Low-abundance / novelty MAG recovery across many samples?
├─ Need automated coassembly targeting → binchicken
├─ Few related samples, clear strata → study-design + matched co-assembly
├─ After contigs exist → basalt ★ / metawrap / dastool / single binners
└─ Only abundance of known refs → coverm / sylph / metaphlan (not coassembly)
```

## Methods caveats

- Targeted coassembly can still create chimeras — multi-coverage binning and
  GUNC/CheckM2 remain mandatory.
- Report marker DB, novelty filter, group size, and assembler.
- Genome counts from large public runs are not transferable to your biome.

## Related skills

`singlem` · `study-design` · `megahit` · `metaspades` · `basalt` · `coverm` · `gtdbtk` ·
`tool-selection` · `metagenomics-workflow`
