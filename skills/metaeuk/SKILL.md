---
name: metaeuk
description: >
  MetaEuk — sensitive gene discovery and annotation on eukaryotic metagenomic contigs
  using MMseqs2 homology + exon dynamic programming (Söding lab). Use when: (1) Calling
  genes on eukaryotic contigs/MAGs, (2) Annotating via protein or profile targets, (3)
  Contig taxonomy via MetaEuk predictions. Not a prokaryotic default (prefer
  prodigal/bakta).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MetaEuk, eukaryotic, gene-prediction, MMseqs2, metagenomics"
  metagenomics.upstream: "https://github.com/soedinglab/metaeuk"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "easy-predict input/output contract checked against current upstream README; not executed here"
---

# MetaEuk

Upstream: [soedinglab/metaeuk](https://github.com/soedinglab/metaeuk)

## Citation

Levy Karin, E., Mirdita, M. & Söding, J. MetaEuk—sensitive, high-throughput
gene discovery and annotation for large-scale eukaryotic metagenomics.
*Microbiome* **8**, 48 (2020). https://doi.org/10.1186/s40168-020-00808-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Prokaryotic callers (`prodigal`) miss spliced eukaryotic genes. MetaEuk uses
**MMseqs2** searches against protein/profile DBs plus exon-set DP — for
eukaryotic contigs and microeukaryote MAGs.

| vs | Prefer MetaEuk when |
|----|---------------------|
| `prodigal` / `bakta` | Eukaryotic / spliced genes |
| `mmseqs2` alone | Need gene models (FASTA/GFF), not only hits |

## How to run

Use eukaryote-enriched contigs and a frozen protein or profile reference. Keep the
result prefix and temporary database inside a fresh output directory.

```bash
set -Eeuo pipefail
contigs="${1:?usage: run-metaeuk.sh CONTIGS_FASTA REFERENCE OUTPUT_DIR}"
reference="${2:?usage: run-metaeuk.sh CONTIGS_FASTA REFERENCE OUTPUT_DIR}"
out="${3:?usage: run-metaeuk.sh CONTIGS_FASTA REFERENCE OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$contigs" && test -e "$reference" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
metaeuk easy-predict "$contigs" "$reference" "$out/predictions" "$out/tmp" \
  --threads "$threads" >"$out/metaeuk.stdout.log" \
  2>"$out/metaeuk.stderr.log"
for suffix in fas codon.fas gff headersMap.tsv; do
  test -f "$out/predictions.$suffix"
done
n_predictions="$(grep -c '^>' "$out/predictions.fas" || true)"
printf 'predicted_proteins\t%s\n' "$n_predictions" >"$out/validation.tsv"
```

Profile references may require `--exhaustive-search`; multiple exon sets change
identifier semantics and must be handled explicitly.

## Decision tree

```text
Gene calling on contigs?
├─ Prokaryotic → prodigal / bakta / prokka
├─ Eukaryotic metagenomes → metaeuk
└─ Then annotate → mmseqs2 / eggnog-mapper / foldseek
```

## Validation, recovery, and provenance

Require protein/codon FASTAs, GFF, header map, logs, and explicit zero-prediction
contigs. Reconcile coordinates and IDs; inspect strand/exon structure, target and
combined E-values, target coverage, overlapping/redundant calls, short/partial
models, contig edges, reference taxonomic bias, and agreement with independent
eukaryotic gene/QC evidence. Do not apply MetaEuk as a prokaryotic default.

Use fresh outputs after changing contigs, reference, thresholds, or release.
Record MetaEuk/MMseqs2 version/build, reference release/build/checksum, contig
checksum, command/logs, all native outputs, prediction count, filters and any
taxonomic voting. Homology-supported gene models are predictions, not validated
transcripts, expression, or complete genomes.

## Related skills

`mmseqs2` · `prodigal` · `bakta` · `homology-search` · `eggnog-mapper` ·
`eukaryotic-metagenomics` · `tool-selection`
