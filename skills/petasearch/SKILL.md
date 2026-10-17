---
name: petasearch
description: >
  Petasearch — efficient parallelized peta-scale protein database search (Steinegger
  lab). Use when: (1) Searching enormous protein collections beyond routine MMseqs2
  setups, (2) Preindexing large target lists for repeated queries, (3) Selective
  Smith–Waterman after coarse filters. Route via homology-search; compare mmseqs2 /
  erast.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Petasearch, protein-search, peta-scale, homology"
  metagenomics.upstream: "https://github.com/steineggerlab/petasearch"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-experimental"
  metagenomics.upstream-version: "snapshot c9cfaf0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream source; not executed here"
---

# Petasearch

Upstream: [steineggerlab/petasearch](https://github.com/steineggerlab/petasearch)

## Citation

No preferred peer-reviewed citation was declared in the reviewed upstream snapshot; cite the software repository, immutable commit, and access date without inventing a paper. Cross-link the Steinegger-lab search stack in [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Petasearch targets **very large** protein target sets with create-DB /
preindex / easy workflows and optional selective SW alignment
(`block-aligner`). Use when warehouse-scale protein search is the bottleneck;
for standard MAG catalogues prefer `mmseqs2`, for embedding retrieval `erast`.

The reviewed build requires CMake, C++ and Rust because the `blockalign` module uses `block-aligner`. Treat this as experimental and pin a commit.

## Inputs and run

Each target is converted to Petasearch's compressed DB and preindexed; `targetlist` has `<kmer_table><TAB><target_db>` per line.

```bash
set -euo pipefail
command -v srasearch >/dev/null
[[ -s query.faa && -s target.faa ]] || exit 2
mkdir -p db tmp result
srasearch convert2sradb target.faa db/targetDB
srasearch createkmertable db/targetDB db/target_kmertable
printf '%s\t%s\n' "$PWD/db/target_kmertable" "$PWD/db/targetDB" > db/targetlist.tsv
srasearch easy-petasearch query.faa db/targetlist.tsv result/alignments.m8 tmp \
  >result/petasearch.stdout.log 2>result/petasearch.stderr.log
test -f result/alignments.m8
```

The upstream README contained a spelling error (`sraserach`) in one easy-workflow example; the built binary and source command table use `srasearch`.

## Decision tree

```text
Protein search scale?
├─ Routine / NR catalogues → mmseqs2
├─ Peta-scale / custom huge targets → petasearch
├─ Vector embeddings → erast
└─ Structure → foldseek
```

## Validation, recovery, and provenance

Require all DB/index component files, completed logs and a parseable alignment table. Confirm query/target IDs, column schema, finite scores, coordinate bounds and expected control homologs; distinguish a legitimate no-hit result from absent/truncated output. Benchmark recall and runtime against a pinned MMseqs2 search before relying on warehouse-scale claims.

Indexes are target- and commit-coupled; rebuild after target/software changes and rerun into a fresh temp/result path after failure. Record source commit/build flags/CPU ISA/Rust, target-list order, FASTA and DB hashes, command, thresholds and output checksum. Search hits support homology evidence, not automatic function transfer.

## Related skills

`homology-search` · `mmseqs2` · `erast` · `foldseek` · `lexicmap` ·
`tool-selection`
