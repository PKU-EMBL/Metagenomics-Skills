---
name: setup
description: >
  First-time environment and database setup for shotgun metagenomics tool skills.
  Use this skill when: (1) Installing Conda/Micromamba environments,
  (2) Preparing host, taxonomy, function, GTDB, or CheckM2 databases,
  (3) Installing BASALT weights, (4) Onboarding a new compute node.
  For individual tools, use the matching software skill (fastp, kneaddata, ...).
license: MIT
category: utilities
tags: [setup, onboarding, installation, conda]
---

# Setup

## Analytical thinking

Install **software and databases once**, version-pin them, and keep analysis runs
reproducible. Prefer one env per major tool family when dependency conflicts arise.

## Checklist

| Step | Check | Next skill |
|------|-------|------------|
| Package manager | `micromamba -V` | — |
| Project dirs | `seq/ temp/ result/` | `study-design` |
| QC tools | `fastp` | `fastp` |
| Host depletion | KneadData + Bowtie2 host index | `kneaddata` |
| Profiling DBs | MetaPhlAn/HUMAnN/Kraken | `metaphlan` / `humann` / `kraken2` |
| Assemblers | MEGAHIT / SPAdes | `megahit` / `metaspades` |
| MAG QC | CheckM2 DB | `checkm2` |
| BASALT | `BASALT --help` + `$BASALT_WEIGHT` (5 CSVs) | `basalt` |

## BASALT install (Conda edition)

See `basalt` skill and https://basalt-guide.readthedocs.io/en/latest/installation.html

```bash
git clone --branch V1.2.2 --depth 1 https://github.com/PKU-EMBL/BASALT.git
cd BASALT
micromamba create -n basalt -f basalt_environment.yml --strict-channel-priority --yes
micromamba run -n basalt bash install.sh
```

## Related skills

`tool-selection` · every software skill under `skills/`
