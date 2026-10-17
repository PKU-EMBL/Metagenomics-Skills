---
name: genome-language-model
description: >
  Route genome language models (gLMs) for metagenomics and microbial genomics:
  representation models (Nucleotide Transformer / NTv3, DNABERT-2, Caduceus), generative
  models (Evo / Evo 2), and mixed-modality metagenomic LMs (OMG + gLM2). Use when
  choosing DNA embeddings, generation, or functional-track prediction — not for
  classical profilers or Foldseek. Child skills: omg, nucleotide-transformer, dnabert2,
  caduceus, evo2. Protein LMs via protein-language-model. Trees via phylogenomics /
  lucaphylo.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "genome-language-model, gLM, NTv3, DNABERT, Caduceus, Evo2, OMG, gLM2"
---

# Genome language model

DNA/genome foundation models are a **parallel track** to QC→assembly→binning.
They provide embeddings, likelihoods, generation, or track prediction — they do
**not** replace CheckM2, GTDB-Tk, MetaPhlAn, or Foldseek.

NTv3-style taxonomy of DNA modeling:

| Strategy | Role | Prefer here |
|----------|------|-------------|
| Representation gLM | Embeddings / MLM | `nucleotide-transformer` · `dnabert2` · `caduceus` |
| Generative (AR / diffusion) | Sequence design / long context | `evo2` (± Evo 1) |
| Mixed-modality metagenomic LM | CDS AA + intergenic DNA | `omg` (gLM2) |
| Protein language models | Remote AA homology / embeddings | `protein-language-model` |
| seq2fun tracks (Borzoi-class) | Dense functional genomics | Not default MAG tools |

## Analytical thinking

| Claim | Prefer | Do not treat as |
|-------|--------|-----------------|
| Metagenomic corpus + gLM2 | `omg` | Cohort taxonomy tables |
| Multi-species DNA / NTv3 tracks | `nucleotide-transformer` | Experimental annotation |
| Efficient multi-species DNA LM + GUE | `dnabert2` | Taxonomy profiler |
| Long-range bi-directional DNA (Mamba) | `caduceus` | Contig assembler |
| Generative / 1 Mb-scale DNA design | `evo2` | MAG QC |
| Protein remote homology | `protein-language-model` | Genome LM logits as hits |
| Phylogeny | `phylogenomics` / `lucaphylo` | Raw LM distances as trees |

Hard rules:

1. Pin model name, size, checkpoint, context length, and license (NT often NC)
2. OMG / OpenGenome2 ≠ ENA study reanalysis (`sra-ena` / `mgnify`)
3. Do not merge gLM scores with BLAST/MMseqs/Foldseek tables unlabeled
4. Prefer multi-species / microbial-aware checkpoints for MAG work
5. GPU needs for large gLMs differ from KneadData/MEGAHIT nodes

## Decision tree

```text
Genome language model need?
│
├─ Metagenome mixed AA+DNA / gLM2 → omg
├─ NTv3 / multi-species tracks & NT family → nucleotide-transformer
├─ Efficient multi-species representation / GUE → dnabert2
├─ Long-range RC-aware DNA LM (Caduceus) → caduceus
├─ Generative long-context (all domains) → evo2
├─ Protein language models → protein-language-model
├─ Structure search → foldseek
├─ Trees → phylogenomics
└─ Unsure → this hub + metagenomics-llm
```

## Related skills

`omg` · `nucleotide-transformer` · `dnabert2` · `caduceus` · `evo2` ·
`protein-language-model` · `metagenomics-llm` · `lucaphylo` ·
`homology-search` · `phylogenomics` · `public-databases` · `tool-selection`
