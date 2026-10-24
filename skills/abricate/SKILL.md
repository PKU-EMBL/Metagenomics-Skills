---
name: abricate
description: >
  ABRicate — mass screening of contigs for AMR/virulence/plasmid markers against bundled
  databases (ResFinder, CARD, NCBI, VFDB, PlasmidFinder, EcoLI_VF, ARG-ANNOT, MEGARES,
  …). Use for fast multi-DB isolate or MAG screens and database concordance checks.
  Route via cge-finders / microbial-mining; official CGE CLI still via
  resfinder/plasmidfinder when phenotype mapping or PointFinder is required.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ABRicate, AMR, virulence, PlasmidFinder, ResFinder, CARD, VFDB, screening"
  metagenomics.upstream: "https://github.com/tseemann/abricate"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "ABRicate screen/summary interface checked against upstream usage; not executed here"
---

# ABRicate

Upstream: [tseemann/abricate](https://github.com/tseemann/abricate)

## Citation

Seemann, T. ABRicate: mass screening of contigs for antimicrobial and virulence
genes. https://github.com/tseemann/abricate

Also cite the **database** papers for each `--db` used (ResFinder, CARD,
PlasmidFinder, VFDB, … — see `resfinder`, `rgi`, `plasmidfinder`,
`virulencefinder`).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

ABRicate is a **BLASTN mass-screen wrapper** over multiple curated gene DBs.
Ideal for: (1) quick multi-DB presence/absence, (2) cross-checking ResFinder vs
CARD vs NCBI AMRFinder-style sets, (3) plasmid replicon + virulence gene panels
on many assemblies.

Does **not** replace PointFinder chromosomal SNPs, ResFinder phenotype
summaries, or CARD protein models (`rgi`). Thresholds (%ID / coverage) drive
sensitivity — pin them in Methods. Metagenome contigs: expect fragmented hits.

## How to run

Freeze the installed databases before screening; do not update them in the middle
of a cohort.

```bash
set -Eeuo pipefail
id="${1:?usage: screen-abricate.sh SAMPLE_ID ASSEMBLY OUTPUT_DIR}"
assembly="${2:?usage: screen-abricate.sh SAMPLE_ID ASSEMBLY OUTPUT_DIR}"
out="${3:?usage: screen-abricate.sh SAMPLE_ID ASSEMBLY OUTPUT_DIR}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
test -s "$assembly" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
abricate --list >"$out/database-manifest.tsv"

IFS=, read -r -a databases <<<"${ABRICATE_DATABASES:-resfinder,plasmidfinder,vfdb}"
reports=()
for db in "${databases[@]}"; do
  [[ "$db" =~ ^[A-Za-z0-9._-]+$ ]] || exit 2
  report="$out/${id}.${db}.tsv"
  abricate --db "$db" "$assembly" >"$report" 2>"$out/${id}.${db}.stderr.log"
  grep -q '^#FILE' "$report"
  reports+=("$report")
done
abricate --summary "${reports[@]}" >"$out/${id}.summary.tsv" \
  2>"$out/${id}.summary.stderr.log"
test -s "$out/${id}.summary.tsv"
test -s "$out/database-manifest.tsv"
```

## Decision tree

```text
Multi-DB gene screen on assemblies?
├─ Fast concordance / batch TSV → abricate
├─ CGE ResFinder + phenotype / PointFinder → resfinder (± pointfinder)
├─ CGE DisinFinder → disinfinder via resfinder
├─ CARD protein models → rgi
├─ Official PlasmidFinder CLI → plasmidfinder
└─ Plasmid ST schemes → pmlst
```

## Validation, recovery, and provenance

Require raw per-database tables with headers, a summary table, and the database
manifest. Retain no-hit samples. Inspect identity, coverage, coordinates,
fragmentation, overlapping/duplicate hits, database discordance, and whether a
hit lies on a plasmid/MGE-supported sequence. Do not infer phenotype, gene
expression, or complete plasmids from an ABRicate row.

Use fresh outputs after changing assemblies, databases, or thresholds. Record
ABRicate/BLAST versions, every database name/date/sequence count and checksum,
assembly checksum, command, logs, raw/summary checksums, and filtering rules.

## Related skills

`cge-finders` · `resfinder` · `plasmidfinder` · `disinfinder` ·
`virulencefinder` · `staramr` · `rgi` · `pmlst` · `mlst` ·
`microbial-mining` · `tool-selection`
