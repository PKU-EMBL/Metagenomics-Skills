---
name: barrnap
description: >
  Basic rapid ribosomal RNA predictor for genomes. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "rrna, annotation"
  metagenomics.upstream: "https://github.com/tseemann/barrnap"
  metagenomics.stage: "gene"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Barrnap CLI template statically reviewed; not executed here"
---

# Barrnap

Upstream: [Barrnap](https://github.com/tseemann/barrnap)

## Citation

Seemann, T. Barrnap: BAsic Rapid Ribosomal RNA Predictor. https://github.com/tseemann/barrnap

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Quick rRNA loci on MAGs/isolates for QC (16S presence) and annotation. Pair with GTDB-Tk / Prokka workflows.

## How to run

Select the kingdom from independent taxonomy evidence; do not assume bacteria
for every MAG.

```bash
set -Eeuo pipefail
id="${1:?usage: run-barrnap.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
genome="${2:?usage: run-barrnap.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
out="${3:?usage: run-barrnap.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
kingdom="${BARRNAP_KINGDOM:-bac}"
threads="${THREADS:-4}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
case "$kingdom" in bac|arc|euk|mito) ;; *) exit 2 ;; esac
test -s "$genome" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

barrnap --kingdom "$kingdom" --threads "$threads" "$genome" \
  >"$out/${id}.rrna.gff" 2>"$out/${id}.barrnap.stderr.log"
```

## Key parameters

| kingdom | bac/arc/euk | |

## Decision notes

- Stage: **function** (rRNA prediction)
- Prefer as a quick rRNA check on genomes/MAGs; not a substitute for full annotation (`bakta`/`prokka`)

## Validation, recovery, and provenance

A valid run may have no complete rRNA call, but the GFF and completed log must
exist. Check sequence IDs/coordinates, partial flags, overlapping calls, expected
5S/16S/23S patterns, kingdom setting, and assembly-edge truncation. Absence of
16S in a fragmented MAG is not proof that the organism lacks the gene.

Record Barrnap/HMM database version, genome checksum, kingdom, command, logs,
GFF checksum, and parsed feature summary. Rerun changed settings under a fresh
path and keep rRNA evidence separate from whole-genome taxonomy.

## Related skills

`prokka` · `gtdbtk` · `checkm2` · `tool-selection` · `metagenomics-workflow`
