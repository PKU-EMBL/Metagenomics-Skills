---
name: binchicken
description: >
  Bin Chicken — targeted coassembly planning for recovering low-abundance / novel MAGs
  by grouping metagenomes that share marker-gene signal (SingleM). Use when: (1) Public
  or large cohorts where all-vs-all coassembly is impossible, (2) Prioritizing sample
  subsets for coassembly to recover rare lineages, (3) Novelty-focused recovery against
  reference genomes, (4) Study-design of coassembly strata. For general coassembly vs
  individual design use study-design. For binning after coassembly use basalt / metabat2
  / etc.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "coassembly, low-abundance, BinChicken, SingleM, MAG"
  metagenomics.upstream: "https://github.com/AroneyS/binchicken"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "0.15.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream documentation; not executed here"
---

# Bin Chicken

Upstream: [AroneyS/binchicken](https://github.com/AroneyS/binchicken)

## Citation

Aroney, S. T. N., Newell, R. J. P., Tyson, G. W. & Woodcroft, B. J. Bin Chicken:
targeted metagenomic coassembly for the efficient recovery of novel genomes.
*Nat. Methods* (2025). https://doi.org/10.1038/s41592-025-02901-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

Create forward and reverse lists with one matching absolute FASTQ path per line, in identical sample order. Bin Chicken currently targets Illumina paired reads.

```bash
set -euo pipefail
[[ -s samples_forward.txt && -s samples_reverse.txt ]] || exit 2
[[ $(wc -l < samples_forward.txt) -eq $(wc -l < samples_reverse.txt) ]] || exit 3
binchicken --version
binchicken single \
  --forward-list samples_forward.txt --reverse-list samples_reverse.txt \
  --run-aviary --cores 64 --output binchicken_single_assembly \
  >binchicken.single.stdout.log 2>binchicken.single.stderr.log
binchicken iterate \
  --coassemble-output binchicken_single_assembly \
  --run-aviary --cores 64 --output binchicken_2_coassembly \
  >binchicken.iterate.stdout.log 2>binchicken.iterate.stderr.log
```

A later iteration can set `--coassembly-samples 3` and use the preceding iteration as `--coassemble-output`. Do not launch the expensive Aviary path before reviewing the dry plan, storage, and scheduler resources.

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

## Validation, recovery, and provenance

Require all input libraries to be accounted for, emitted coassembly groups to contain only permitted strata, SingleM evidence for targets, completed Aviary logs, and explicit recovered/failed group status. Compare individual and targeted coassemblies under identical assembly, mapping, CheckM2/GUNC and dereplication gates; report recovery gains, chimerism and compute—not raw MAG count alone.

Resume only through documented Bin Chicken/Aviary checkpoints with unchanged lists, databases and parameters; otherwise use a fresh output. Record Bin Chicken/SingleM/Aviary versions, metapackage/GTDB release, ordered read lists and checksums, commands, group manifests, seeds, resource use and accepted/rejected MAG lineage. Targeted grouping does not prove that coassembled contigs belong to one population.

## Related skills

`singlem` · `study-design` · `megahit` · `metaspades` · `basalt` · `coverm` · `gtdbtk` ·
`tool-selection` · `metagenomics-workflow`
