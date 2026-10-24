---
name: bakta
description: >
  Rapid standardized annotation of bacterial genomes (alignment-free ID). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "annotation, genome-mining, prokaryote"
  metagenomics.upstream: "https://github.com/oschwengers/bakta"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Bakta genome annotation CLI checked against current upstream usage; not executed here"
---

# Bakta

Upstream: [Bakta](https://github.com/oschwengers/bakta)

## Citation

Schwengers, O. *et al.* Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. *Microb. Genom.* **7**, 000685 (2021). https://doi.org/10.1099/mgen.0.000685

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Bakta provides **rapid, standardized** bacterial genome annotation with
alignment-free sequence identification — preferred substrate for many new
studies over Prokka when the Bakta DB is available.

Use on QC-filtered MAGs/genomes before `antismash`, `dram`, `rgi`,
`defensefinder`. Not a substitute for catalogue-scale `prodigal`+clustering.

## How to run

```bash
set -Eeuo pipefail
id="${1:?usage: annotate-bakta.sh GENOME_ID GENOME_FASTA DB_DIR OUTPUT_DIR}"
genome="${2:?usage: annotate-bakta.sh GENOME_ID GENOME_FASTA DB_DIR OUTPUT_DIR}"
db="${3:?usage: annotate-bakta.sh GENOME_ID GENOME_FASTA DB_DIR OUTPUT_DIR}"
out="${4:?usage: annotate-bakta.sh GENOME_ID GENOME_FASTA DB_DIR OUTPUT_DIR}"
threads="${THREADS:-8}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
test -s "$genome" && test -d "$db" || exit 2
log_dir="${out}.logs"
test ! -e "$out" && test ! -e "$log_dir" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$log_dir"

bakta --db "$db" --threads "$threads" --output "$out" --prefix "$id" \
  "$genome" \
  >"$log_dir/bakta.stdout.log" 2>"$log_dir/bakta.stderr.log"
```

## Key parameters

| Item | Notes |
|------|-------|
| `$BAKTA_DB` | Required — pin release with software |
| Input | Prefer near-complete, low-contamination genomes |
| Threads | Scale with CPU |

## Decision tree

```text
Genome annotation substrate?
├─ Bacterial MAG/isolate, modern default → bakta
├─ Minimal classic pipeline → prokka
└─ Mining next → bakta/prokka → microbial-mining tools
```

## Validation, recovery, and provenance

Require non-empty JSON, GFF3, GenBank, nucleotide, and protein outputs expected
for the pinned release. Reconcile input replicons/contigs, feature counts,
translation table, locus tags, pseudogene/partial-call rates, and warnings;
inspect anomalous coding density or rRNA/tRNA absence against MAG completeness.
Downstream mining must consume outputs from the exact same annotation run.

Use a fresh output after changing genome, database, taxonomy hints, or release.
Record Bakta and dependency versions, database type/version/checksum, input and
output checksums, translation/replicon settings, command, logs, and feature
summary. Annotation is database-supported prediction, not experimental function.

## Related skills

`prokka` · `prodigal` · `antismash` · `dram` · `rgi` · `defensefinder` ·
`mag-qc` · `microbial-mining` · `tool-selection`
