---
name: padloc
description: >
  PADLOC (Prokaryotic Antiviral Defence LOCator) — HMM + synteny detection of antiviral
  defence systems (CRISPR-Cas and many other systems) in prokaryotic genomes. Use as a
  complement or alternative to DefenseFinder for defenseome surveys. Route via
  microbial-mining; pair with genomad/virsorter2 for MGE context.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PADLOC, defense, defenseome, CRISPR, antiviral, genome-mining"
  metagenomics.upstream: "https://github.com/padlocbio/padloc"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "2.x interface"
  metagenomics.command-status: "PADLOC 2 input/database CLI checked against upstream documentation; not executed here"
---

# PADLOC

Upstream: [padlocbio/padloc](https://github.com/padlocbio/padloc) ·
DB: [padloc-db](https://github.com/padlocbio/padloc-db) ·
Web: https://padloc.otago.ac.nz/padloc/

## Citation

Payne, L. J. *et al.* Identification and classification of antiviral defence
systems in bacteria and archaea with PADLOC reveals new system types.
*Nucleic Acids Res.* **49**, 10868–10878 (2021).
https://doi.org/10.1093/nar/gkab883

Web server: Payne, L. J. *et al.* PADLOC: a web server for the identification
of antiviral defence systems in microbial genomes. *Nucleic Acids Res.* **50**,
W541–W550 (2022). https://doi.org/10.1093/nar/gkac400

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

PADLOC finds defence systems via **HMM homology + system architecture/synteny**.
Complements `defensefinder` (different model sets / system coverage). For dark
neighborhood discovery without known system models use `spacedust`.

| vs | Prefer PADLOC when |
|----|---------------------|
| `defensefinder` | PADLOC-DB models / web precomputes; cross-check both for surveys |
| `spacedust` | Known antiviral system types vs de novo clusters |
| `genomad` | Host defenseome vs MGE/virus contigs |

Annotate proteins first (`bakta` / `prokka`). Pin **padloc-db** version.

## How to run

PADLOC 2.x requires PADLOC-DB 2.x. Install a named database release before the
study; do not run `--db-update` between samples.

```bash
set -Eeuo pipefail
genome="${1:?usage: run-padloc.sh GENOME_FASTA OUTPUT_DIR}"
out="${2:?usage: run-padloc.sh GENOME_FASTA OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$genome" || exit 2
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "${out}.logs"
data_args=()
if [[ -n "${PADLOC_DATA:-}" ]]; then
  test -d "$PADLOC_DATA" || exit 2
  data_args=(--data "$PADLOC_DATA")
fi
padloc --version >"${out}.logs/software-version.txt"
padloc "${data_args[@]}" --db-version >"${out}.logs/database-version.txt"
padloc --fna "$genome" --outdir "$out" --cpu "$threads" \
  "${data_args[@]}" >"${out}.logs/padloc.stdout.log" \
  2>"${out}.logs/padloc.stderr.log"
find "$out" -type f -name '*_padloc.csv' -print -quit | grep -q .
find "$out" -type f -name '*_padloc.gff' -print -quit | grep -q .
```

For existing proteins, provide the coordinate-matched FAA and GFF together;
apply `--fix-prodigal` only to affected Prodigal files after checking IDs.

## Decision tree

```text
Defenseome / antiviral systems?
├─ PADLOC models → padloc
├─ DefenseFinder models → defensefinder
├─ Prefer both for Methods robustness → padloc + defensefinder
├─ Dark conserved neighborhoods → spacedust
└─ Virus/plasmid contigs → genomad → checkv
```

## Validation, recovery, and provenance

Require CSV, GFF, domtblout, protein/GFF intermediates as applicable, version
files, and logs. Reconcile genomes and proteins; inspect complete versus partial
systems, model/domain support, gene order, overlapping calls, contig-edge
truncation, and optional ncRNA/CRISPR evidence. Keep PADLOC and DefenseFinder
calls separate before a documented consensus step.

Use fresh outputs after changing input, database, optional evidence, or release.
Record PADLOC/PADLOC-DB versions and database checksum, HMMER/Prodigal versions,
input and annotation checksums, command, logs, outputs and filtering rules.
Predicted systems indicate genomic potential, not measured antiviral activity.

## Related skills

`defensefinder` · `spacedust` · `genomad` · `virsorter2` · `bakta` ·
`microbial-mining` · `tool-selection`
