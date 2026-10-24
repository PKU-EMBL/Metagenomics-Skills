---
name: skani
description: >
  Fast robust average nucleotide identity (ANI) for metagenomic genomes and MAG
  comparisons. Use for species-level clustering, novelty vs GTDB/UHGG, and scalable ANI
  matrices.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ANI, comparative-genomics, MAG"
  metagenomics.upstream: "https://github.com/bluenote-1577/skani"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "skani triangle/dist CLI checked against upstream quick start; not executed here"
---

# skani

Upstream: [bluenote-1577/skani](https://github.com/bluenote-1577/skani)

## Citation

Shaw, J. & Yu, Y. W. Fast and robust metagenomic sequence comparison through
sparse chaining with skani. *Nat. Methods* **20**, 1661–1665 (2023).
https://doi.org/10.1038/s41592-023-02018-3

## Analytical thinking

skani estimates **ANI** quickly on incomplete MAGs better than many classic
tools that assume near-complete genomes. Use for:

- Dereplication cross-checks vs `drep` · `fastani`
- Novelty vs GTDB reps / UHGG (`mgnify`)
- All-vs-all MAG similarity heatmaps

95% ANI remains a common species-level heuristic — state your cutoff.

## vs FastANI

| | `skani` | `fastani` |
|--|---------|------------|
| Strength | Speed/robustness on incomplete MAGs; large catalogues | Classic literature-compatible ANI |
| Prefer | New large MAG studies | Reproducing FastANI-based Methods |
| Skill | this | `fastani` |

Do not mix FastANI and skani values in one unlabeled matrix.

## How to run

Use an explicit one-path-per-line manifest so catalogue membership and ordering
remain auditable.

```bash
set -Eeuo pipefail
list="${1:?usage: skani-triangle.sh GENOMES_LIST OUTPUT_DIR}"
out="${2:?usage: skani-triangle.sh GENOMES_LIST OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$list" || exit 2
mapfile -t genomes < <(awk 'NF && $1 !~ /^#/ {print $0}' "$list")
((${#genomes[@]} >= 2)) || { echo "need at least two genomes" >&2; exit 2; }
for genome in "${genomes[@]}"; do test -s "$genome" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

skani triangle -t "$threads" "${genomes[@]}" \
  >"$out/skani.triangle.tsv" 2>"$out/skani.stderr.log"
test -s "$out/skani.triangle.tsv"
```

For query-to-reference comparisons use `skani dist -q ... -r ... -o ...`; for
large reusable references prefer `skani sketch` plus `skani search`.

## Validation, recovery, and provenance

Validate matrix dimensions and unique genome labels, retain missing/low-
alignment comparisons, and apply ANI together with reported aligned fraction and
MAG quality. Inspect threshold sensitivity near cluster boundaries and never mix
skani/FastANI values in an unlabeled matrix.

Use a fresh directory after changing genomes, sketch parameters, or release.
Record skani version, manifest and genome checksums, command, threads, logs,
output schema, ANI/alignment-fraction rules, clustering code, and representative
selection. ANI supports operational clustering; it is not a phylogeny.

## Related skills

`fastani` · `drep` · `gtdb` · `mgnify` · `checkm2` · `gtdbtk` · `mag-qc`
