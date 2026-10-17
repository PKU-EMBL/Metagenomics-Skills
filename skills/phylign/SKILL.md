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

```bash
# install deps (conda: python, snakemake, mamba) — see upstream README
git clone https://github.com/karel-brinda/phylign.git
cd phylign
make test
make download          # compressed assemblies + COBS indexes

# put/symlink queries, edit config, then:
make                   # or: make match && make map
```

Building new compressed libraries: use **MiniPhy**
(https://github.com/karel-brinda/miniphy), then search with Phylign-style
workflows.

## Decision tree

```text
Search vs huge bacterial genome collections?
├─ Phylogeny-compressed 661k / MOF on desktop → phylign
├─ Custom million-genome nucleotide index → lexicmap
├─ Protein homology → mmseqs2 / erast / foldseek
└─ Short reads → contigs for binning → strobealign / bowtie2
```

## Related skills

`homology-search` · `lexicmap` · `minimap2` · `progenomes` · `gtdb` ·
`tool-selection`
