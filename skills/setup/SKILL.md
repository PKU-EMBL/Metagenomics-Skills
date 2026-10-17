---
name: setup
description: >
  First-time environment and database setup for shotgun metagenomics tool skills. Use
  this skill when: (1) Installing Conda/Micromamba environments, (2) Preparing host,
  taxonomy, function, GTDB, or CheckM2 databases, (3) Installing BASALT weights, (4)
  Onboarding a new compute node. For public database routing (SRA/ENA, MGnify, GTDB
  releases, bioBakery), use public-databases and the matching resource skill. For
  individual tools, use the matching software skill (fastp, kneaddata, ...).
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "setup, onboarding, installation, conda"
  metagenomics.stage: "utilities"
---

# Setup

## Analytical thinking

Install **software and databases once**, version-pin them, and keep analysis runs
reproducible. Prefer one env per major tool family when dependency conflicts arise.

Public resources are a separate layer — see `public-databases` before inventing
ad-hoc download scripts.

When operating as a coding agent, inspect first and mutate second. Do not create
a new environment, download a large database, or change shell startup files
until existing runtimes, storage, network policy, and user scope are known.

## Agent preflight

```bash
set -euo pipefail
printf 'host=%s\n' "$(hostname)"
uname -a
printf 'cpus='; (command -v nproc >/dev/null && nproc) || getconf _NPROCESSORS_ONLN || true
if command -v free >/dev/null; then free -h; elif command -v vm_stat >/dev/null; then vm_stat; fi
command -v micromamba || command -v conda || true
command -v apptainer || command -v singularity || command -v docker || true
df -h .
quota -s 2>/dev/null || true
printf 'TMPDIR=%s\n' "${TMPDIR:-<unset>}"
```

Then report, without installing yet:

- OS/architecture and local vs scheduler execution
- package manager or container runtime already available
- CPU, memory, scratch, quota, and write permissions
- required database releases and estimated download/storage
- network/proxy restrictions and whether human-associated data are present
- reusable environments/indexes found and how their versions were verified

## Checklist

| Step | Check | Next skill |
|------|-------|------------|
| Package manager | `micromamba -V` | — |
| Project dirs | `seq/ temp/ result/` | `study-design` |
| Public DB plan | Which archives/catalogues/indexes | `public-databases` |
| QC tools | `fastp` | `fastp` |
| Host depletion | KneadData + Bowtie2 host index | `kneaddata` |
| Profiling DBs | MetaPhlAn/HUMAnN/Kraken | `biobakery-databases` / `kraken2` |
| Assemblers | MEGAHIT / SPAdes | `megahit` / `metaspades` |
| Binning QC | CheckM2 DB | `checkm2` |
| Taxonomy runtime | `GTDBTK_DATA_PATH` | `gtdb` + `gtdbtk` |
| Binning tools | BASALT★ / MetaWRAP / DAS Tool | `basalt` (recommended) / `metawrap` / `dastool` |
| Function DBs | eggNOG / CARD | `eggnog-mapper` / `rgi` |
| BASALT weights | `BASALT --help` + `$BASALT_WEIGHT` (5 CSVs) | `basalt` |

## Reproducibility records

Create these before the first production run:

```text
provenance/
├── environments/          # explicit lock/export or container digest
├── software-versions.tsv
├── database-manifest.tsv  # name, release, path/URL, checksum, install date
├── input-checksums.sha256
└── preflight.txt
```

Prefer an explicit environment lock or immutable container digest over an
unversioned environment export. Keep databases outside ephemeral environments;
make shared copies read-only during analysis. Verify an index belongs to the
exact FASTA/database release before reuse.

## BASALT install (Conda edition)

See `basalt` skill and https://basalt-guide.readthedocs.io/en/latest/installation.html

```bash
git clone --branch V1.2.2 --depth 1 https://github.com/PKU-EMBL/BASALT.git
cd BASALT
micromamba create -n basalt -f basalt_environment.yml --strict-channel-priority --yes
micromamba run -n basalt bash install.sh
```

## Related skills

`public-databases` · `tool-selection` · `nextflow` · `snakemake` ·
`research-analysis` · every software skill under `skills/`
