---
name: phylign
description: >
  Phylign — BLAST-like alignment of genes, plasmids, or reads against
  phylogeny-compressed microbial genome collections (e.g. pre-2019 661k bacteria) on
  ordinary desktops. Uses phylogenetic compression (MiniPhy for building compressed
  assemblies/COBS indexes; Phylign for search via COBS + Minimap2). Use when searching
  huge genome warehouses without a cluster. Route via homology-search; compare lexicmap.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Phylign, MiniPhy, phylogenetic-compression, search, COBS, genomes"
  metagenomics.upstream: "https://github.com/karel-brinda/phylign"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed-workflow"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Make/Snakemake workflow and 661k collection contract checked upstream; not executed here"
---

# Phylign (phylogenetic compression search)

Upstream: [karel-brinda/phylign](https://github.com/karel-brinda/phylign) ·
Compression builder: [karel-brinda/miniphy](https://github.com/karel-brinda/miniphy) ·
https://brinda.eu/mof

## Citation

Břinda, K. *et al.* Efficient and robust search of microbial genomes via
phylogenetic compression. *Nat. Methods* **22**, 692–697 (2025).
https://doi.org/10.1038/s41592-025-02625-2

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Public microbial collections outgrow BLAST-style local search. **Phylogenetic
compression** reorders genomes by estimated evolutionary history so XZ / COBS /
Minimap2 work on highly compressible batches.

| Component | Role |
|-----------|------|
| **MiniPhy** | Build phylogeny-compressed assemblies / indexes from genome batches |
| **Phylign** | Query compressed 661k-style DBs: COBS match → Minimap2 align |

| vs | Prefer Phylign when |
|----|---------------------|
| `lexicmap` | Using phylogeny-compressed 661k / MOF collections on a laptop |
| `mmseqs2` | Nucleotide genome warehouse search (not protein catalogue) |
| `minimap2` alone | Target set is millions of assemblies (needs compression/index stack) |

Requirements (upstream): ~12 GB RAM, ~120 GB disk for DB + intermediates.
Pin which compressed collection you downloaded.

## How to run

First verify a pinned source checkout with `make test` and download/check the
661k database once. For each analysis, clone the committed workflow into a fresh
run directory and link the frozen shared database.

```bash
set -Eeuo pipefail
source="${1:?usage: run-phylign.sh PINNED_CHECKOUT ABS_QUERY ABS_CONFIG RUN_DIR}"
query="${2:?usage: run-phylign.sh PINNED_CHECKOUT ABS_QUERY ABS_CONFIG RUN_DIR}"
config="${3:?usage: run-phylign.sh PINNED_CHECKOUT ABS_QUERY ABS_CONFIG RUN_DIR}"
run="${4:?usage: run-phylign.sh PINNED_CHECKOUT ABS_QUERY ABS_CONFIG RUN_DIR}"
[[ "$query" = /* && "$config" = /* ]] || exit 2
test -d "$source/.git" && test -d "$source/asms" && test -d "$source/cobs" || exit 2
test -s "$query" && test -s "$config" || exit 2
name="$(basename "$query")"
[[ "$name" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
logs="${run}.logs"
test ! -e "$run" && test ! -e "$logs" || {
  echo "use new run and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$run")" "$logs"
git clone --local --no-hardlinks "$source" "$run" \
  >"$logs/clone.stdout.log" 2>"$logs/clone.stderr.log"
for dbdir in asms cobs; do
  if [[ -d "$run/$dbdir" ]]; then
    find "$run/$dbdir" -mindepth 1 -print -quit | grep -q . && exit 2
    rmdir "$run/$dbdir"
  fi
  ln -s "$(cd "$source/$dbdir" && pwd)" "$run/$dbdir"
done
mkdir -p "$run/input"
find "$run/input" -mindepth 1 -maxdepth 1 -delete
ln -s "$query" "$run/input/$name"
cp "$run/config.yaml" "$run/config.default.yaml"
cp "$config" "$run/config.yaml"
git -C "$source" rev-parse HEAD >"$logs/source-commit.txt"
make -C "$run" >"$logs/phylign.stdout.log" 2>"$logs/phylign.stderr.log"
find "$run/output" -type f -size +0c -print -quit | grep -q .
```

Building new compressed libraries routes to **MiniPhy**. Never run `make cleanall`
on a shared database checkout.

## Decision tree

```text
Search vs huge bacterial genome collections?
├─ Phylogeny-compressed 661k / MOF on desktop → phylign
├─ Custom million-genome nucleotide index → lexicmap
├─ Protein homology → mmseqs2 / erast / foldseek
└─ Short reads → contigs for binning → strobealign / bowtie2
```

## Validation, recovery, and provenance

Require query reconciliation, COBS candidate summaries, final alignments/reports,
workflow logs and a successful DAG. Inspect unique query IDs, non-ACGT handling,
match/map attrition, alignment identity/coverage, repetitive queries, multi-hit
ambiguity, collection QC scope, and representative known controls. No hit in the
QC-filtered COBS index is not proof of biological absence.

Resume only inside the same run with unchanged query, config, source commit and
database links; otherwise use a fresh clone. Record Phylign/MiniPhy commits,
Snakemake/COBS/Minimap2 versions, compressed collection identity/checksums,
query/config checksums, commands/logs, outputs and filters. The historical 661k
collection must not be described as a current universal genome catalogue.

## Related skills

`homology-search` · `lexicmap` · `minimap2` · `progenomes` · `gtdb` ·
`tool-selection`
