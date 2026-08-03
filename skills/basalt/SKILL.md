---
name: basalt
description: >
  PKU-EMBL BASALT and BASALT-Air — recommended ensemble MAG recovery across one
  or more assemblies (multi-binner + refinement). Use this skill when:
  (1) Running BASALT multi-binner recovery, (2) Choosing Conda BASALT vs
  BASALT-Air, (3) Multi-assembly refinement, (4) Resuming checkpoints,
  (5) Writing reproducible BASALT Methods.
  Upstream: https://github.com/PKU-EMBL/BASALT and
  https://github.com/PKU-EMBL/BASALT-Air.
  Ensemble peers: dastool (SCG aggregation), metawrap (binning+refinement suite).
  Prefer basalt as the default ensemble route; use metawrap/dastool when a
  classical suite or contig2bin consensus is enough.
  For study design of assemblies, use study-design.
  For QC thresholds, use checkm2 and mag-qc.
license: MIT
category: analysis-tools
tags: [BASALT, MAG, ensemble-binning, refinement, multi-assembly, PKU-EMBL]
upstream: https://github.com/PKU-EMBL/BASALT
---

# BASALT / BASALT-Air

Upstream: [PKU-EMBL/BASALT](https://github.com/PKU-EMBL/BASALT) ·
[BASALT-Air](https://github.com/PKU-EMBL/BASALT-Air) ·
Guide: https://basalt-guide.readthedocs.io/en/latest/

## Citation

Qiu, Z. *et al.* BASALT refines binning from metagenomic data and increases
resolution of genome-resolved metagenomic analysis. *Nat. Commun.* **15**, 2179
(2024). https://doi.org/10.1038/s41467-024-46539-7

See also [docs/references.md](../../docs/references.md).
## Analytical thinking

BASALT is one member of the **ensemble binning** family, alongside DAS Tool and
MetaWRAP: multiple binners propose candidates, then a refinement/selection step
produces a non-redundant MAG set.

Within that family, **BASALT is the recommended default** here — especially for
related samples with coherent multi-assembly evidence (sample-specific assemblies
preserve restricted populations; a matched co-assembly can rescue shared
low-abundance genomes; cross-sample coverage informs selection and contig
refinement).

Peers (still valid):

| Peer | Role |
|------|------|
| `basalt` | **Recommended** multi-assembly ensemble + DL/connectivity refinement |
| `metawrap` | Packaged multi-binner + CheckM-style bin refinement suite |
| `dastool` | Classical SCG scoring/aggregation of existing contig2bin tables |

Do **not** pool unrelated strata just to feed BASALT more FASTAs.

Refinement (MLP ensemble + connectivity retrieval) is **model- and
feature-supported prediction**, not experimental proof of contamination removal.
Report `BASALT_WEIGHT` checksums when refinement underpins claims.

## Edition choice

| Need | Prefer |
|------|--------|
| New deployment, absolute paths, separate work/out | **BASALT-Air** (`basalt`) |
| Resume existing Conda checkpoints | **Conda BASALT** (`BASALT`) |

CLIs and checkpoints are **not interchangeable**.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Linux x86_64 | Same |
| RAM | 128 GB | 256 GB+ |
| Threads | 8 | 32+ |
| Models | `BASALT_WEIGHT` with 5 `*_ensemble.csv` | Checksummed |
| QC DB | CheckM2 | Pinned |
| Inputs | ≥1 assembly + coverage reads | From `megahit`/`metaspades` + `kneaddata` |

## How to run (Conda BASALT)

Docs: [usage](https://basalt-guide.readthedocs.io/en/latest/usage.html)

```bash
mkdir -p /project/basalt_runs/study_01 && cd /project/basalt_runs/study_01
ln -s /data/assembly.fasta .
ln -s /data/R1.fastq .
ln -s /data/R2.fastq .

BASALT \
  -a assembly.fasta \
  -s R1.fastq,R2.fastq \
  -t 32 -m 128 \
  --sensitive sensitive \
  --refinepara quick \
  --min-cpn 35 --max-ctn 20 \
  -q checkm2 --mode new \
  -o study_01_basalt
```

PE syntax: `,` within a pair; `/` between samples. HiFi → `-hf` only (never `-l`).

## Key parameters

| Option | Values | Thinking |
|--------|--------|----------|
| `--sensitive` | quick / sensitive / more-sensitive | Candidate diversity vs cost; not accuracy magic |
| `--refinepara` | quick / deep | Deeper retrieval expands candidate space |
| `--min-cpn` / `--max-ctn` | e.g. 35 / 20 | Refinement **entry** gates ≠ publication filters |
| `--mode` | new / continue | Continue only if provenance unchanged |
| `-e` | m / v / l | Extra binners; `-e l` needs PKU-EMBL LorBin fork commit |

## Pipeline stages

```text
assemblies + reads → coverage/connectivity → multi-binner candidates
  → within-/cross-assembly selection → contig screening/retrieval
  → reassembly → final MAG dir + QC
```

## Hard rules

1. One dedicated run directory; never two processes in one CWD
2. Prefer local/symlink names for Conda edition
3. Resume only with identical inputs/code/models/DBs
4. Do not invent flags — verify against guide/`--help`


## Literature notes (Nat. Commun. 2024)

From Qiu *et al.* (BASALT paper), useful operational points:

- **Problem framed**: mis-clustering, genome splitting, and multi-genome mega-bins
  yield redundant/artificial/contaminated MAGs that poison downstream analyses.
- **Strategy**: multiple binners × multiple thresholds → neural-network core-sequence
  identification → redundant-bin removal → non-redundant refinement; supports
  short-read and short+long assemblies.
- **Coverage correlation coefficient (CCC)**: IQR-based contig coverage used in
  selection/refinement — multi-sample abundance structure is first-class evidence.
- **Reported gains** (same assemblies): up to ~2× MAGs vs VAMB / DAS Tool /
  MetaWRAP on CAMI; ~30% more MAGs than MetaWRAP on lake sediment, including
  unique class-level lineages; ~47.6% more non-redundant ORFs than MetaWRAP on
  that dataset. Treat as **paper benchmarks**, not a promise for every biome.
- **Quality language in paper**: baseline gates such as completeness ≥35 /
  contamination ≤20 for refinement entry; high-quality often completeness ≥90 /
  contamination ≤5. Keep refinement entry gates distinct from publication filters
  in Methods (`mag-qc`).

## Related skills

`dastool` · `metawrap` · `lorbin` · `comebin` · `semibin2` · `vamb` · `study-design` · `megahit` · `metaspades` · `kneaddata` · `checkm2` · `mag-qc` · `drep`
