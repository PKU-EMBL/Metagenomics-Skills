---
name: genomic-lm
description: >
  Route DNA / genomic language models (gLMs) for metagenomics and microbial
  genomics: representation models (Nucleotide Transformer / NTv3, DNABERT-class),
  generative genome models (Evo / Evo 2), and mixed-modality metagenomic LMs
  (OMG + gLM2). Use when choosing embeddings, generation, or functional-track
  prediction — not for classical profilers or Foldseek structure search.
  Child skills: omg, nucleotide-transformer, evo2. Protein LMs via
  metagenomics-llm / plmsearch. Trees via phylogenomics / lucaphylo.
license: MIT
category: orchestration
tags: [gLM, genomic-LM, Nucleotide-Transformer, Evo2, OMG, gLM2, foundation-model]
---

# Genomic language models (gLMs)

DNA/genome foundation models are a **parallel track** to QC→assembly→binning.
They provide embeddings, likelihoods, generation, or track prediction — they do
**not** replace CheckM2, GTDB-Tk, MetaPhlAn, or Foldseek.

NTv3-style taxonomy of DNA modeling (InstaDeep):

| Strategy | Role | Prefer here |
|----------|------|-------------|
| Representation gLM | Embeddings / MLM likelihoods | `nucleotide-transformer` (NT / NTv3) |
| Generative (AR / diffusion) | Sequence design / long-context modeling | `evo2` (± Evo 1) |
| Mixed-modality metagenomic LM | CDS AA + intergenic DNA context | `omg` (gLM2) |
| Protein LM search | Remote AA homology | `plmsearch` / `deepblast` (not gLMs) |
| seq2fun tracks (Borzoi-class) | Dense functional genomics | Mention only — not default MAG tools |

## Analytical thinking

| Claim | Prefer | Do not treat as |
|-------|--------|-----------------|
| Metagenomic pretrain corpus + gLM2 | `omg` | Your cohort’s taxonomy table |
| Multi-species DNA embeddings / tracks / NTv3 | `nucleotide-transformer` | Experimental annotation |
| Long-context DNA modeling & design (all domains) | `evo2` | Assembled MAG quality |
| Protein remote homology | `plmsearch` / `homology-search` | Genome LM output |
| Phylogeny from sequences | `phylogenomics` / `lucaphylo` | Raw LM logits as a tree |

Hard rules:

1. Pin model name, size, checkpoint URL, context length, and license (NT is often NC)
2. OMG / OpenGenome2 corpora ≠ ENA study reanalysis (`sra-ena` / `mgnify`)
3. Do not merge gLM scores with BLAST/MMseqs/Foldseek tables unlabeled
4. GPU/memory for 7B–40B genome LMs differ from KneadData nodes
5. Microbial MAGs: prefer models trained with microbial/OpenGenome diversity; human-only NT variants are a mismatch

## Decision tree

```text
Genomic / DNA LM need?
│
├─ Metagenome-scale mixed AA+DNA corpus / gLM2 → omg
├─ DNA embeddings, annotation tracks, NTv3 multi-species → nucleotide-transformer
├─ Long-context generation / likelihood across domains of life → evo2
├─ Protein sequence LM search only → plmsearch / deepblast / homology-search
├─ Structure search → foldseek (homology-search)
├─ Trees → phylogenomics
└─ Unsure → this hub + metagenomics-llm
```

## Related skills

`omg` · `nucleotide-transformer` · `evo2` · `metagenomics-llm` · `lucaphylo` ·
`homology-search` · `phylogenomics` · `public-databases` · `tool-selection`
