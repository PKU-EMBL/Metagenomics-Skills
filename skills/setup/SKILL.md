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
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "preflight and pinned BASALT install recipe statically reviewed; not executed here"
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
set -Eeuo pipefail
report="${1:-provenance/preflight.txt}"
test ! -e "$report" || { echo "use a new report path: $report" >&2; exit 2; }
mkdir -p "$(dirname "$report")"
{
  printf 'host=%s\n' "$(hostname)"
  uname -a
  printf 'cpus='
  (command -v nproc >/dev/null && nproc) || getconf _NPROCESSORS_ONLN || true
  if command -v free >/dev/null; then
    free -h
  elif command -v vm_stat >/dev/null; then
    vm_stat
  fi
  command -v micromamba || command -v conda || true
  command -v apptainer || command -v singularity || command -v docker || true
  df -h .
  quota -s 2>/dev/null || true
  printf 'TMPDIR=%s\n' "${TMPDIR:-<unset>}"
} >"$report" 2>&1
test -s "$report"
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

Read the `basalt` skill and
https://basalt-guide.readthedocs.io/en/latest/installation.html first. Execute
only after the preflight and user-approved storage/environment scope.

```bash
set -Eeuo pipefail
prefix="${1:?usage: install-basalt.sh INSTALL_PREFIX}"
env_name="${BASALT_ENV_NAME:-basalt-1.2.2}"
checkout="$prefix/BASALT-V1.2.2"
logs="$prefix/logs/BASALT-V1.2.2"
test ! -e "$checkout" && test ! -e "$logs" || {
  echo "use a new install prefix or preserve the existing installation" >&2; exit 2;
}
mkdir -p "$prefix" "$logs"
git clone --branch V1.2.2 --depth 1 https://github.com/PKU-EMBL/BASALT.git \
  "$checkout" >"$logs/clone.stdout.log" 2>"$logs/clone.stderr.log"
micromamba create -n "$env_name" -f "$checkout/basalt_environment.yml" \
  --strict-channel-priority --yes \
  >"$logs/environment.stdout.log" 2>"$logs/environment.stderr.log"
(
  cd "$checkout"
  micromamba run -n "$env_name" bash install.sh
) >"$logs/install.stdout.log" 2>"$logs/install.stderr.log"
micromamba run -n "$env_name" BASALT --help >"$logs/BASALT.help.txt"
git -C "$checkout" rev-parse HEAD >"$logs/source-commit.txt"
test -s "$logs/BASALT.help.txt"
test -s "$logs/source-commit.txt"
```

Do not infer database or model readiness from `--help`; verify CheckM2 data and
all five `BASALT_WEIGHT` files separately in the `basalt` preflight.

## Setup acceptance and recovery

An installation is usable only after version/help checks, a tool-provided smoke
test where available, database/index integrity checks, and write/read tests in
the intended runtime context. Archive lockfiles or container digests, source
commits, commands, logs, checksums, environment variables, install paths, and
failed attempts. Never claim a large database is installed until expected files,
checksums and a representative query were inspected.

Preserve failed installations for diagnosis or remove only the dedicated new
prefix after confirming it contains no reusable/user data. Do not mutate a
shared environment to repair one project; create a new pinned environment.

## Related skills

`public-databases` · `tool-selection` · `nextflow` · `snakemake` ·
`research-analysis` · every software skill under `skills/`
