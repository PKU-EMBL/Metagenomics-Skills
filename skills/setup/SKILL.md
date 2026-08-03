---
name: setup
description: >
  First-time environment setup for shotgun metagenomics analysis.
  Use this skill when: (1) Installing Conda/Micromamba tool environments,
  (2) Configuring host-depletion and taxonomy/function databases,
  (3) Commands fail with missing binaries or databases,
  (4) Preparing CheckM2 or BASALT model weights,
  (5) Onboarding a new compute node for metagenomics pipelines.

  For end-to-end analysis planning, use metagenomics-workflow.
  For tool choice, use tool-selection.
license: MIT
category: utilities
tags: [setup, onboarding, installation, conda]
---

# Metagenomics Setup

## Quick checklist

| Step | Check | Fix |
|------|-------|-----|
| 1. Package manager | `micromamba -V` or `conda -V` | Install Micromamba/Miniconda |
| 2. Project layout | `seq/`, `temp/`, `result/metadata.txt` | Create standard directories |
| 3. Host DB | KneadData Bowtie2 index exists | Download host genome and build index |
| 4. Profiling DBs | MetaPhlAn / HUMAnN / Kraken DBs present | Install per tool docs |
| 5. MAG QC DB | `checkm2 database --current` | `checkm2 database --download` |
| 6. BASALT (optional) | `BASALT --help` and `$BASALT_WEIGHT` | Install release tag + model weights |

## Recommended project layout

```text
$wd/
├── seq/                  # SampleID_1.fq.gz SampleID_2.fq.gz
├── temp/                 # intermediates
├── result/
│   └── metadata.txt      # tab-delimited; SampleID in column 1
└── logs/
```

```bash
mkdir -p seq temp result logs
sed -i 's/\r//' result/metadata.txt   # enforce Unix newlines
```

## Environment strategy

Prefer **one environment per major stage** (or validated packed envs):

| Stage | Typical env contents |
|-------|----------------------|
| QC / host removal | fastp, kneaddata, bowtie2, multiqc |
| Read-based | humann, metaphlan, kraken2, bracken |
| Assembly / genes | megahit, prodigal, cd-hit, salmon, eggnog-mapper |
| Classical MAGs | metawrap stack, drep, coverm, gtdbtk, checkm2 |
| BASALT | dedicated `basalt` env + `BASALT_WEIGHT` |

Record every env with `conda env export` / `micromamba env export`.

## BASALT-specific setup

```bash
git clone --branch V1.2.2 --depth 1 \
  https://github.com/PKU-EMBL/BASALT.git BASALT
cd BASALT
micromamba create -n basalt -f basalt_environment.yml \
  --strict-channel-priority --yes
micromamba run -n basalt bash install.sh
```

Then download model weights to a persistent path, export `BASALT_WEIGHT`, and
confirm five `*_ensemble.csv` files. Configure CheckM2 separately.

Prefer **BASALT-Air** for new deployments needing absolute paths and separate
workdir/outdir: https://github.com/PKU-EMBL/BASALT-Air

## Verify

```bash
command -v fastp bowtie2
command -v checkm2 || true
test -n "${BASALT_WEIGHT:-}" && find "$BASALT_WEIGHT" -maxdepth 1 -name '*_ensemble.csv' | wc -l
```

## Related skills

- `metagenomics-workflow` — full pipeline guidance
- `basalt` — BASALT / BASALT-Air execution
- `preprocessing` — fastp + KneadData defaults
