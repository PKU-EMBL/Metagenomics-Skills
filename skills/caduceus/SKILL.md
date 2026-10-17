---
name: caduceus
description: >
  Caduceus — bi-directional equivariant long-range DNA language model (Mamba / RC-aware)
  for long genomic contexts. Use when: (1) Long DNA sequences where transformer gLMs are
  costly, (2) Reverse-complement equivariant embeddings (Caduceus-PS) or RC-augmented Ph
  models, (3) Comparing long-range DNA LMs to DNABERT-2 / NT. HF:
  kuleshov-group/caduceus-*.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Caduceus, gLM, genome-language-model, Mamba, DNA, long-range"
  metagenomics.upstream: "https://github.com/kuleshov-group/caduceus"
  metagenomics.stage: "function"
---

# Caduceus

Upstream: [kuleshov-group/caduceus](https://github.com/kuleshov-group/caduceus) ·
HF collection: https://huggingface.co/collections/kuleshov-group/caducues-65dcb89b4f54e416ef61c350

## Citation

Schiff, Y. *et al.* Caduceus: Bi-Directional Equivariant Long-Range DNA Sequence
Modeling. *arXiv* https://doi.org/10.48550/arXiv.2403.03234 (2024).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

```python
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

model_name = "kuleshov-group/caduceus-ph_seqlen-131k_d_model-256_n_layer-16"
revision = "b0477522ac5d044ad03578aa724ec8e4bdbd405b"  # reviewed 2026-10-18
tokenizer = AutoTokenizer.from_pretrained(
    model_name, revision=revision, trust_remote_code=True)
model = AutoModelForMaskedLM.from_pretrained(
    model_name, revision=revision, trust_remote_code=True).eval()
batch = tokenizer("ACGTACGTACGT", return_tensors="pt")
with torch.inference_mode():
    logits = model(**batch).logits
assert logits.shape[:2] == batch["input_ids"].shape
print(model_name, revision, tuple(logits.shape))
```

Reconfirm and deliberately update the immutable revision when changing checkpoints. Use the `ps` family only when reverse-complement equivariance is required and record strand pooling.

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
