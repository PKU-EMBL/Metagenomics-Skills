---
name: dnabert2
description: >
  DNABERT-2 — efficient multi-species genome language model (BPE + ALiBi) with
  the Genome Understanding Evaluation (GUE) benchmark. Use when: (1) DNA
  embeddings or fine-tunes on multi-species tasks, (2) Comparing representation
  gLMs without NT/Evo-scale hardware, (3) GUE-style evaluation. Upstream:
  https://github.com/MAGICS-LAB/DNABERT_2. HF: zhihan1996/DNABERT-2-117M.
  Related: DNABERT (v1), DNABERT-S. Route via genome-language-model.
license: MIT
category: analysis-tools
tags: [DNABERT-2, DNABERT, gLM, genome-language-model, GUE, HuggingFace]
upstream: https://github.com/MAGICS-LAB/DNABERT_2
stage: function
---

# DNABERT-2

Upstream: [MAGICS-LAB/DNABERT_2](https://github.com/MAGICS-LAB/DNABERT_2) ·
HF: https://huggingface.co/zhihan1996/DNABERT-2-117M

## Citation

Zhou, Z. *et al.* DNABERT-2: Efficient Foundation Model and Benchmark for
Multi-Species Genome. *arXiv* https://doi.org/10.48550/arXiv.2306.15006 (2023).
(ICLR 2024)

Original DNABERT: Ji, Y. *et al.* DNABERT: pre-trained Bidirectional Encoder
Representations from Transformers model for DNA-language in genome.
*bioRxiv* https://doi.org/10.1101/2020.09.17.301879 (2020).

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

DNABERT-2 replaces k-mer tokenization with **BPE** and uses **ALiBi** for
longer effective context vs DNABERT v1. Trained multi-species; evaluated on
**GUE** (28 datasets). Lighter than NT/Evo for many embedding/fine-tune jobs.

| vs | Prefer DNABERT-2 when |
|----|------------------------|
| `nucleotide-transformer` | Smaller model / GUE-centric workflows |
| `caduceus` | Transformer BPE stack vs Mamba long-range RC models |
| `evo2` | Representation / classification — not AR generation |

Related: **DNABERT-S** (species-separating embeddings), **GenomeOcean**
(generative; see upstream pointers) — cite separately if used.

## How to run

```bash
# HF masked LM / embeddings pattern — verify transformers API for the tag
from transformers import AutoTokenizer, AutoModel
tok = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
model = AutoModel.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
# fine-tune / GUE: follow upstream README sections Finetune & Quick Start
```

## Decision tree

```text
Representation genome LM?
├─ Multi-species efficient / GUE → dnabert2
├─ NTv3 tracks / large NT family → nucleotide-transformer
├─ Long-range Mamba / RC-equivariant → caduceus
└─ Generative → evo2
```

## Related skills

`genome-language-model` · `nucleotide-transformer` · `caduceus` · `evo2` ·
`omg` · `tool-selection`
