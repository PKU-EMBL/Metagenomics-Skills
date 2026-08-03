---
name: caduceus
description: >
  Caduceus — bi-directional equivariant long-range DNA language model (Mamba /
  RC-aware) for long genomic contexts. Use when: (1) Long DNA sequences where
  transformer gLMs are costly, (2) Reverse-complement equivariant embeddings
  (Caduceus-PS) or RC-augmented Ph models, (3) Comparing long-range DNA LMs to
  DNABERT-2 / NT. Upstream: https://github.com/kuleshov-group/caduceus.
  HF: kuleshov-group/caduceus-*. Route via genome-language-model.
license: MIT
category: analysis-tools
tags: [Caduceus, gLM, genome-language-model, Mamba, DNA, long-range]
upstream: https://github.com/kuleshov-group/caduceus
stage: function
---

# Caduceus

Upstream: [kuleshov-group/caduceus](https://github.com/kuleshov-group/caduceus) ·
HF collection: https://huggingface.co/collections/kuleshov-group/caducues-65dcb89b4f54e416ef61c350

## Citation

Schiff, Y. *et al.* Caduceus: Bi-Directional Equivariant Long-Range DNA Sequence
Modeling. *arXiv* https://doi.org/10.48550/arXiv.2403.03234 (2024).

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Caduceus targets **long-range** DNA modeling with bi-directionality and
**reverse-complement** structure (Ph = RC augmentation; PS = RC-equivariant).
Typical pretrained length scale ~131k in released HF checkpoints — check the
exact `seqlen` in the model id.

| vs | Prefer Caduceus when |
|----|----------------------|
| `dnabert2` | Longer contexts / RC-equivariant inductive bias |
| `nucleotide-transformer` | Mamba-style efficiency on long DNA |
| `evo2` | Bidirectional MLM-style use vs AR generation |

## How to run

```bash
from transformers import AutoModelForMaskedLM, AutoTokenizer
model_name = "kuleshov-group/caduceus-ph_seqlen-131k_d_model-256_n_layer-16"
# or caduceus-ps_… for RC-equivariant
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)
```

Pin checkpoint (`ph` vs `ps`) and sequence length in Methods.

## Decision tree

```text
Long DNA representation LM?
├─ RC-aware / long-range Mamba → caduceus
├─ Multi-species efficient transformer → dnabert2
├─ NTv3 / NT family → nucleotide-transformer
└─ Generative all-domains → evo2
```

## Related skills

`genome-language-model` · `dnabert2` · `nucleotide-transformer` · `evo2` ·
`omg` · `tool-selection`
