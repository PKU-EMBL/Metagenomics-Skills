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
---

# Petasearch

Upstream: [steineggerlab/petasearch](https://github.com/steineggerlab/petasearch)

## Citation

See upstream README / releases for the current preferred citation; software at
https://github.com/steineggerlab/petasearch. Cross-link Steinegger-lab search
stack in [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Petasearch targets **very large** protein target sets with create-DB /
preindex / easy workflows and optional selective SW alignment
(`block-aligner`). Use when warehouse-scale protein search is the bottleneck;
for standard MAG catalogues prefer `mmseqs2`, for embedding retrieval `erast`.

Requires Rust toolchain to build from source — follow upstream install notes.
Verify exact binary names/`easy-petasearch` flags against the installed tag
(README examples evolve).

## How to run

```bash
# follow upstream: build → create DBs → preindex → search
# easy workflow pattern (confirm on installed version):
#   … easy-petasearch query.fasta targetlist alignments.m8 tmp
```

## Decision tree

```text
Protein search scale?
├─ Routine / NR catalogues → mmseqs2
├─ Peta-scale / custom huge targets → petasearch
├─ Vector embeddings → erast
└─ Structure → foldseek
```

## Related skills

`homology-search` · `mmseqs2` · `erast` · `foldseek` · `lexicmap` ·
`tool-selection`
