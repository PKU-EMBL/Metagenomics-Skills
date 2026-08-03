---
name: homology-search
description: >
  Route all homology / similarity search paradigms for shotgun metagenomics:
  sequence heuristics (MMseqs2, DIAMOND), structure/motif (Foldseek, Folddisco),
  PLM embeddings (PLMSearch, DeepBLAST), vector-database retrieval (ERAST),
  phylogeny-compressed genome search (Phylign), and gene-vs-million-genomes
  (LexicMap). Use when choosing how to search proteins, genes, or genomes —
  not for read abundance profilers or MAG taxonomy placement (gtdbtk).
license: MIT
category: orchestration
tags: [homology, search, vector-DB, Foldseek, MMseqs2, ERAST, Phylign, routing]
stage: function
---

# Homology search routing

Shotgun projects need **many search paradigms**. This hub chooses among them.
For LM/structure dark-matter framing also see `metagenomics-llm`. For trees /
placement see `phylogenomics`.

## Analytical thinking

| Paradigm | Prefer | Typical claim |
|----------|--------|---------------|
| Sequence heuristics (AA) | `mmseqs2` · `diamond` | Catalogue hits, NR, contig taxonomy |
| Structure / fold | `foldseek` | AFDB/PDB remote homologs |
| Structural motif | `folddisco` | Active-site / metal geometry |
| PLM embedding (sequence-only) | `plmsearch` · `deepblast` | Twilight-zone without structures |
| Vector DB + LLM rerank | `erast` | Billion-scale protein/nt retrieval |
| Phylogeny-compressed genomes | `phylign` | BLAST-like vs ~661k bacteria on a laptop |
| Gene/plasmid vs million genomes | `lexicmap` | Nucleotide alignment at warehouse scale |

Hard rules:

1. Do **not** merge BLAST/MMseqs, Foldseek, PLM, and vector-DB tables unlabeled
2. Hits are hypotheses — pin software **and** database/index release
3. Vector / PLM rankings ≠ experimental function
4. Genome-scale search (`phylign` / `lexicmap`) ≠ short-read→contig mapping for binning

## Decision tree

```text
What are you searching?
│
├─ Proteins / ORFs
│   ├─ Close / catalogue-scale → mmseqs2 / diamond
│   ├─ Have structures or ProstT5 → foldseek (± folddisco)
│   ├─ Sequence-only remote homology → plmsearch / deepblast
│   └─ Billion-scale vector retrieval → erast
├─ Genes / plasmids / long queries vs huge genome sets
│   ├─ Phylogeny-compressed 661k-style BLAST-like → phylign
│   └─ Million-genome nucleotide index → lexicmap
├─ Dark modules / neighborhoods → spacedust (via metagenomics-llm)
└─ Unsure → this hub + tool-selection
```

## Related skills

`mmseqs2` · `diamond` · `foldseek` · `folddisco` · `plmsearch` · `deepblast` ·
`erast` · `phylign` · `lexicmap` · `metagenomics-llm` · `phylogenomics` ·
`eggnog-mapper` · `tool-selection`
