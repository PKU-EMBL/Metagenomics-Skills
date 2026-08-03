---
name: basalt
description: >
  PKU-EMBL BASALT and BASALT-Air refined MAG recovery across assemblies.
  Use this skill when: (1) Running multi-binner candidate generation with BASALT,
  (2) Cross-assembly selection and contig refinement,
  (3) Choosing BASALT vs BASALT-Air,
  (4) Resuming checkpointed runs,
  (5) Reporting reproducible BASALT Methods.

  For classical MetaWRAP catalogues, use mag-classical.
  For study design of multi-assembly inputs, use study-design.
  For QC thresholds, use mag-qc.
license: MIT
category: analysis-tools
tags: [BASALT, MAG, refinement, multi-assembly, PKU-EMBL]
---

# BASALT / BASALT-Air

## Authoritative docs

- Guide: https://basalt-guide.readthedocs.io/en/latest/
- Paper: https://doi.org/10.1038/s41467-024-46539-7
- Air: https://github.com/PKU-EMBL/BASALT-Air

## Edition choice

| Capability | Conda `BASALT` | Air `basalt` |
|------------|----------------|--------------|
| Environment | Conda/Micromamba | Pixi |
| Paths | Local/relative names preferred | Absolute paths first-class |
| Work/output | CWD intermediates; `-o` name | `--workdir` / `--outdir` |
| Best for | Resume existing Conda runs | New deployments |

**Checkpoints and CLIs are not interchangeable.**

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Linux x86_64 | Same |
| RAM | 128 GB | 256 GB+ |
| Threads | 8 | 32+ |
| Models | `BASALT_WEIGHT` (5 ensemble CSVs) | Checksummed |
| QC | CheckM2 DB | Version-pinned |

## How to run (Conda edition)

```bash
mkdir -p /project/basalt_runs/study_01 && cd /project/basalt_runs/study_01
ln -s /data/assembly.fasta .
ln -s /data/sample_R1.fastq .
ln -s /data/sample_R2.fastq .

BASALT \
  -a assembly.fasta \
  -s sample_R1.fastq,sample_R2.fastq \
  -t 32 -m 128 \
  --sensitive sensitive \
  --refinepara quick \
  --min-cpn 35 --max-ctn 20 \
  -q checkm2 --mode new \
  -o study_01_basalt
```

Multi-assembly PE delimiter: `,` within pairs, `/` between samples. HiFi → `-hf` only.

## Key parameters

| Option | Values | Role |
|--------|--------|------|
| `--sensitive` | quick / sensitive / more-sensitive | Candidate generators |
| `--refinepara` | quick / deep | Retrieval depth |
| `--min-cpn` / `--max-ctn` | e.g. 35 / 20 | Refinement entry gates |
| `--mode` | new / continue | Init vs resume |
| `-e` | m,v,l | MetaBinner / VAMB / LorBin |

`-e l` requires the PKU-EMBL LorBin–BASALT fork; record its Git commit.

## Pipeline stages

```text
assemblies + reads
  → coverage / connectivity
  → multi-binner candidates
  → within- then cross-assembly selection
  → contig screening + retrieval (+ OLC)
  → reassembly
  → final MAG directory + QC report
```

## Hard rules

1. One dedicated run directory; never two processes in one CWD
2. Resume only with unchanged inputs/code/models/DBs
3. Do not invent flags; verify with `--help` / guide
4. Refinement is model-supported prediction, not experimental proof

## Related skills

- `study-design` — whether assemblies belong in one run
- `mag-qc` — publication filters vs refinement gates
- `setup` — install and weights
- `metagenomics-workflow` — end-to-end placement
