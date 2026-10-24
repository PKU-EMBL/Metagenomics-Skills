---
name: biobakery-databases
description: >
  Install and pin bioBakery reference databases for MetaPhlAn and HUMAnN (ChocoPhlAn
  markers, UniRef gene families, MetaCyc pathways, utility mapping). Use this skill
  when: (1) Downloading MetaPhlAn/HUMAnN databases, (2) Choosing UniRef90 vs UniRef50,
  (3) Aligning MetaPhlAn and HUMAnN DB versions, (4) Troubleshooting missing index
  paths. For Kraken indexes use kraken2. For eggNOG/CARD/GTDB use those skills.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, bioBakery, ChocoPhlAn, UniRef, MetaPhlAn, HUMAnN"
  metagenomics.upstream: "https://github.com/biobakery/biobakery"
  metagenomics.stage: "utilities"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "database helper interfaces statically reviewed; large downloads not executed here"
---

# bioBakery databases (MetaPhlAn / HUMAnN)

Upstream: [MetaPhlAn](https://github.com/biobakery/MetaPhlAn) ·
[HUMAnN](https://github.com/biobakery/humann) ·
bioBakery: https://huttenhower.sph.harvard.edu/biobakery/

## Analytical thinking

MetaPhlAn and HUMAnN results are **database-version-dominated**. Changing
ChocoPhlAn or UniRef releases can move species/pathway tables more than tweaking
CLI flags.

Keep MetaPhlAn marker DB and HUMAnN nucleotide/protein DBs **compatible** for
the same study when you report both taxonomy and pathways. Record:
software version + DB names + install paths + download date.

UniRef90 vs UniRef50 is a sensitivity/specificity and disk trade-off — state it
explicitly; do not silently switch mid-cohort.

## Prerequisites

| DB | Used by | Notes |
|----|---------|-------|
| MetaPhlAn / ChocoPhlAn markers | `metaphlan` | Species-level marker genes |
| HUMAnN ChocoPhlAn | `humann` | Nucleotide mapping |
| UniRef90 or UniRef50 | `humann` | Translated search / gene families |
| Utility mapping + MetaCyc | `humann` | Pathway aggregation |

Disk: tens to hundreds of GB depending on UniRef choice.

## How to install (HUMAnN helpers)

Run large downloads only after checking free space, network policy, and bundle
names against the installed helper.

```bash
set -Eeuo pipefail
root="${1:?usage: install-humann-dbs.sh NEW_DATABASE_ROOT}"
log_dir="${root}.logs"
test ! -e "$root" && test ! -e "$log_dir" || {
  echo "use new database and log paths" >&2; exit 2;
}
mkdir -p "$root" "$log_dir"
humann_databases --download chocophlan full "$root" \
  >"$log_dir/chocophlan.stdout.log" 2>"$log_dir/chocophlan.stderr.log"
humann_databases --download uniref uniref90_diamond "$root" \
  >"$log_dir/uniref.stdout.log" 2>"$log_dir/uniref.stderr.log"
humann_databases --download utility_mapping full "$root" \
  >"$log_dir/utility.stdout.log" 2>"$log_dir/utility.stderr.log"

humann_config --update database_folders nucleotide "$root/chocophlan"
humann_config --update database_folders protein "$root/uniref"
humann_config --update database_folders utility_mapping "$root/utility_mapping"
find "$root" -type f -size +0c -print | sort >"$root/files.manifest"
```

These are HUMAnN 3 helper interfaces; capture `humann_databases --help`, package version, downloaded bundle names and checksums before configuring paths.

## How to install (MetaPhlAn)

```bash
set -Eeuo pipefail
root="${1:?usage: install-metaphlan-db.sh NEW_DATABASE_ROOT}"
log_dir="${root}.logs"
test ! -e "$root" && test ! -e "$log_dir" || {
  echo "use new database and log paths" >&2; exit 2;
}
mkdir -p "$root" "$log_dir"
metaphlan --install --db_dir "$root" \
  >"$log_dir/install.stdout.log" 2>"$log_dir/install.stderr.log"
find "$root" -type f -size +0c -print | sort >"$root/files.manifest"
test -s "$root/files.manifest"
```

Confirm the DB build string printed in MetaPhlAn logs and archive it.

## Decision tree

```text
Profiling DB need?
├─ Marker taxonomy only → MetaPhlAn DB (this skill) → metaphlan
├─ Pathways / gene families → HUMAnN DBs (this skill) → humann
├─ Custom / fast k-mer taxonomy → kraken2 indexes (not bioBakery)
└─ Genome taxonomy for MAGs → gtdb / gtdbtk
```

## Verify, recovery, and provenance

```bash
set -Eeuo pipefail
root="${1:?usage: verify-biobakery-db.sh DATABASE_ROOT}"
test -d "$root" && test -s "$root/files.manifest" || exit 2
metaphlan --version
humann --version
humann_config --print
find "$root" -type f -size 0 -print >"$root/empty-files.txt"
test ! -s "$root/empty-files.txt"
sha256sum "$root/files.manifest" >"$root/files.manifest.sha256"
```

Inspect helper logs, expected index shards, bundle/readme metadata, configured
paths, and a small tool-provided test before cohort use. Interrupted downloads
must be resumed only through supported helpers or moved aside; never combine
unknown partial bundles. Record software/helper versions, exact bundle/index
names, UniRef level, URLs, download date, file manifest/checksums, configuration,
and storage path. A database install is not validated merely because files exist.

## Related skills

`public-databases` · `metaphlan` · `humann` · `kraken2` · `setup`
