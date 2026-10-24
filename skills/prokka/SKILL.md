---
name: prokka
description: >
  Rapid prokaryotic genome annotation (CDS/rRNA/tRNA). Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "annotation, orf, prokaryote"
  metagenomics.upstream: "https://github.com/tseemann/prokka"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Prokka per-genome CLI template statically reviewed; not executed here"
---

# Prokka

Upstream: [Prokka](https://github.com/tseemann/prokka)

## Citation

Seemann, T. Prokka: rapid prokaryotic genome annotation. *Bioinformatics* **30**, 2068–2069 (2014). https://doi.org/10.1093/bioinformatics/btu153

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Prokka wraps Prodigal + feature predictors into GenBank/GFF — convenient for
**per-genome** annotation of isolates/MAGs. For large non-redundant gene
catalogues prefer `prodigal` → `cd-hit`/`mmseqs2` → `eggnog-mapper`.

| Need | Prefer |
|------|--------|
| Standardized bacterial annotation + modern DBs | `bakta` |
| Classic rapid GFF/GBK, minimal deps | `prokka` |
| Catalogue-scale ORFs only | `prodigal` |

Fragmented MAGs yield incomplete/wrong gene calls — filter with `mag-qc` first.

## How to run

```bash
set -Eeuo pipefail
id="${1:?usage: annotate-prokka.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
genome="${2:?usage: annotate-prokka.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
out="${3:?usage: annotate-prokka.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
threads="${THREADS:-8}"
kingdom="${PROKKA_KINGDOM:-Bacteria}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
case "$kingdom" in Bacteria|Archaea) ;; *) exit 2 ;; esac
test -s "$genome" || exit 2
log_dir="${out}.logs"
test ! -e "$out" && test ! -e "$log_dir" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$log_dir"

prokka "$genome" --outdir "$out" --prefix "$id" --cpus "$threads" \
  --kingdom "$kingdom" \
  >"$log_dir/prokka.stdout.log" 2>"$log_dir/prokka.stderr.log"
```

## Key parameters

| Flag | Notes |
|------|-------|
| `--cpus` | Threads |
| `--kingdom` | Bacteria default; set Archaea when appropriate |
| `--compliant` | NCBI-oriented outputs when submitting |

## Decision tree

```text
Annotate a bacterial/archaeal genome/MAG?
├─ Modern standardized → bakta
├─ Classic rapid GBK/GFF → prokka
└─ Only proteins for catalogue → prodigal
```

## Validation, recovery, and provenance

Require non-empty GFF, GenBank, FAA, FFN, and summary outputs. Reconcile input
contigs, feature counts and IDs, kingdom/genetic code, coding density, partial
calls, and warnings. Inspect missing rRNA/tRNA in the context of completeness and
fragmentation. Keep one stable locus-tag namespace per genome/catalogue.

Never use `--force` on an unarchived result. Run changed genomes, databases, or
parameters under a new path. Record Prokka and dependency/database versions,
input/output checksums, kingdom/genetic code/locus-tag settings, command, logs,
and feature summary. Product names are homology-supported annotations, not
experimentally verified functions.

## Related skills

`bakta` · `prodigal` · `eggnog-mapper` · `barrnap` · `antismash` · `dram` ·
`tool-selection`
