---
name: homology-search
description: >
  Route all homology / similarity search paradigms for shotgun metagenomics,
  including the Steinegger/Söding stack (MMseqs2, HH-suite, Foldseek family,
  PLASS, MetaEuk, Petasearch), vector DB (ERAST), and genome warehouse search
  (Phylign, LexicMap). Use when choosing how to search proteins, genes, or
  genomes.
license: MIT
category: orchestration
tags: [homology, search, Steinegger, Foldseek, MMseqs2, vector-DB, routing]
stage: function
---

# Homology search routing

Shotgun projects need **many search paradigms**. This hub chooses among them.
For LM dark-matter framing also see `metagenomics-llm`. For trees see
`phylogenomics`.

## Steinegger / Söding search stack

| Role | Prefer |
|------|--------|
| Sequence search / cluster / taxonomy | `mmseqs2` |
| Profile HMM remote homology | `hh-suite` |
| Protein-level assembly from reads | `plass` |
| Eukaryotic gene call via homology | `metaeuk` |
| Structure compress/index | `foldcomp` |
| Structure search / multimer / ProstT5 | `foldseek` |
| Structural motifs | `folddisco` |
| Multiple structure alignment | `foldmason` |
| Peta-scale protein search | `petasearch` |
| Conserved gene neighborhoods | `spacedust` |
| Taxonomy (DNA/protein) | `metabuli` (separate taxonomy skill) |

## Other paradigms

| Paradigm | Prefer |
|----------|--------|
| PLM embedding search | `plmsearch` · `deepblast` |
| Vector DB + rerank | `erast` |
| Phylogeny-compressed genomes | `phylign` |
| Gene vs million genomes | `lexicmap` |
| Catalogue AA aligner | `diamond` |

Hard rules:

1. Do not merge BLAST/MMseqs, HH-suite, Foldseek, PLM, and vector-DB tables unlabeled
2. Pin software **and** database/index release
3. Low pLDDT structures inflate Foldseek false positives
4. `plass` proteins ≠ binnable contigs; `metaeuk` is for eukaryotes

## Decision tree

```text
What are you searching / recovering?
│
├─ Proteins / ORFs
│   ├─ Close / catalogue-scale → mmseqs2 / diamond
│   ├─ Profile remote homology / MSA for folding → hh-suite
│   ├─ Structures or ProstT5 / AFDB → foldseek (± folddisco / foldmason / foldcomp)
│   ├─ Peta-scale protein targets → petasearch
│   ├─ Sequence-only PLM → plmsearch / deepblast
│   └─ Billion-scale vector retrieval → erast
├─ Recover more proteins from reads → plass
├─ Eukaryotic genes on contigs → metaeuk
├─ Genes / plasmids vs huge genome sets
│   ├─ Phylogeny-compressed 661k-style → phylign
│   └─ Million-genome nucleotide index → lexicmap
├─ Dark modules / neighborhoods → spacedust
└─ Unsure → this hub + tool-selection
```

## Related skills

`mmseqs2` · `hh-suite` · `plass` · `metaeuk` · `foldcomp` · `foldseek` ·
`folddisco` · `foldmason` · `petasearch` · `spacedust` ·
`plmsearch` · `deepblast` · `erast` · `phylign` · `lexicmap` · `diamond` ·
`metagenomics-llm` · `phylogenomics` · `unicore` · `tool-selection`
