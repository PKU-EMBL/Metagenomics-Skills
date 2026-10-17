---
name: eukcc
description: >-
  Estimate completeness, contamination, and lineage of microbial-eukaryotic genomes or bins with EukCC2, singly or by folder. Use for eukaryotic MAG quality assessment with a pinned EukCC2 database; not for bacterial/archaeal MAGs.
license: MIT
compatibility: Requires EukCC 2.2.0, EukCC2 database 1.2 or a pinned successor, MetaEuk, pplacer/EPA-ng, HMMER, aligners, and substantial memory.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "eukcc,eukaryotic-mag,completeness,contamination,taxonomy,quality"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.2.0; database 1.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# EukCC

EukCC2 selects lineage-aware marker sets to assess eukaryotic genomes/MAGs. EukCC v1 databases are incompatible.

## Database setup

```bash
set -euo pipefail
mkdir -p /data/eukcc && cd /data/eukcc
wget -c https://ftp.ebi.ac.uk/pub/databases/metagenomics/eukcc/eukcc2_db_ver_1.2.tar.gz
tar -xzf eukcc2_db_ver_1.2.tar.gz
export EUKCC2_DB="$(realpath eukcc2_db_ver_1.2)"
test -d "$EUKCC2_DB"
```

Record archive checksum and extraction path. Prefer HTTPS even when older upstream examples show HTTP.

## Single genome

```bash
set -euo pipefail
bin=${1:?usage: eukcc-single.sh bin.fa output_dir}
out=${2:?usage: eukcc-single.sh bin.fa output_dir}
[[ -s "$bin" && -d "${EUKCC2_DB:?set EUKCC2_DB}" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a fresh output directory" >&2; exit 2; }
eukcc single --out "$out" --threads 8 "$bin" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/eukcc.tsv" && -s "$out/eukcc.log" ]] || exit 3
```

## Folder mode

```bash
eukcc folder --out eukcc_folder_out --threads 8 bins \
  >eukcc.folder.stdout.log 2>eukcc.folder.stderr.log
```

Folder mode expects `.fa` by default and can attempt automatic refinement/merging. Preserve `merged_bins.csv`, `bad_quality.csv`, `missing_marker_genes.txt`, merged FASTAs, and the original bins; do not replace source bins silently.

## Validation

- ensure each expected bin is represented in good, bad-quality, or missing-marker outputs;
- inspect selected lineage/marker support, completeness, contamination, and log warnings;
- compare with an appropriate BUSCO lineage where scientifically useful;
- re-run assessment on any refined sequence, not merely copy old scores;
- examine contig-domain, coverage, GC, and taxonomic discordance independently.

Upstream cautions that published genomes used to train marker sets can create non-independent evaluation; inspect database training accessions for benchmarking claims.

## Recovery and provenance

Tree placement may be memory intensive despite thread settings. On failure, preserve debug logs, increase memory or process bins individually, and use a clean output path. Capture EukCC/dependency versions, database release/checksum, command, and input/output FASTA checksums.

## Analytical thinking

Completeness and contamination are model estimates conditional on selected lineage and marker database. They do not validate ploidy, haplotype resolution, or absence of prokaryotic/viral contamination. Interpret unsupported marker sets as uncertainty, not zero quality.

## Source

- https://github.com/EBI-Metagenomics/EukCC
