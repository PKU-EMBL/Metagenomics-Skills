---
name: fastani
description: >
  FastANI — alignment-free approximate mapping for high-throughput average nucleotide
  identity (ANI) among prokaryotic genomes/MAGs. Use when: (1) Reproducing literature
  that reports FastANI, (2) Pairwise/species-boundary ANI at moderate catalogue scales,
  (3) Comparing to skani for Methods. Prefer skani for very large MAG sets / incomplete
  genomes unless FastANI is required for compatibility.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ANI, FastANI, comparative-genomics"
  metagenomics.upstream: "https://github.com/ParBLiSS/FastANI"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "FastANI one-to-one/list CLI checked against upstream usage; not executed here"
---

# FastANI

Upstream: [ParBLiSS/FastANI](https://github.com/ParBLiSS/FastANI)

## Citation

Jain, C., Rodriguez-R, L. M., Phillippy, A. M., Konstantinidis, K. T. & Aluru, S.
High throughput ANI analysis of 90K prokaryotic genomes reveals clear species
boundaries. *Nat. Commun.* **9**, 5114 (2018).
https://doi.org/10.1038/s41467-018-07641-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FastANI popularized scalable **~95% ANI species-boundary** analyses. Still widely
cited in Methods even when newer tools are faster.

| Tool | Prefer when |
|------|-------------|
| `skani` | Large MAG catalogues; incomplete MAGs; speed/memory |
| `fastani` | Compatibility with published FastANI thresholds / pipelines |
| `drep` | Dereplication workflow (may call ANI backends) |

State the ANI tool + version + cutoff (commonly 95% species; AF/alignment
fraction matters — report it).

## How to run

The executable is commonly named `fastANI` with this capitalization.

```bash
set -Eeuo pipefail
query="${1:?usage: run-fastani.sh QUERY_FASTA REFERENCE_FASTA OUTPUT_DIR}"
reference="${2:?usage: run-fastani.sh QUERY_FASTA REFERENCE_FASTA OUTPUT_DIR}"
out="${3:?usage: run-fastani.sh QUERY_FASTA REFERENCE_FASTA OUTPUT_DIR}"
threads="${THREADS:-8}"
for input in "$query" "$reference"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

fastANI -q "$query" -r "$reference" -o "$out/fastani.tsv" -t "$threads" \
  >"$out/fastani.stdout.log" 2>"$out/fastani.stderr.log"
test -e "$out/fastani.tsv"
```

For catalogues, use explicit `--ql` and `--rl` path lists with checksums. FastANI
may emit no row for sufficiently distant pairs, so an empty result is not by
itself an execution failure.

## Validation, recovery, and provenance

For every output row require five fields: query, reference, ANI, bidirectional
fragment mappings, and total query fragments. Compute and report alignment
fraction as mappings/total fragments, retain no-hit pairs, and consider the
known query/reference asymmetry. Do not apply a 95% ANI rule without an aligned-
fraction and genome-quality policy.

Use fresh outputs after changing genome sets or thresholds. Record FastANI
version, query/reference roles, list and genome checksums, threads, command,
logs, no-hit pairs, ANI/alignment-fraction table, and clustering rules. ANI is a
similarity estimate, not a phylogeny or proof of formal species identity.

## Related skills

`skani` · `drep` · `gtdb` · `mgnify` · `coverm` · `tool-selection`
