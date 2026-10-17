---
name: nucleotide-transformer
description: >
  InstaDeep Nucleotide Transformer family — DNA foundation models from NT/NT-v2 through
  NTv3 (multi-species, long-context seq–function and generation). Use when: (1) DNA
  embeddings or MLM scores on contigs/MAGs, (2) Functional-track / genome-annotation
  style prediction with NTv3, (3) Contrasting representation gLMs vs generative Evo 2 or
  metagenomic gLM2. HF: InstaDeepAI. Check CC BY-NC-SA license for your use case.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Nucleotide-Transformer, NTv3, gLM, DNA, InstaDeep, HuggingFace"
  metagenomics.upstream: "https://github.com/instadeepai/nucleotide-transformer"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot 2dc37b8"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Python API reviewed against upstream; not executed here"
---

# Nucleotide Transformer (NT / NTv3)

Upstream: [instadeepai/nucleotide-transformer](https://github.com/instadeepai/nucleotide-transformer) ·
HF: https://huggingface.co/InstaDeepAI

## Citation

Dalla-Torre, H. *et al.* Nucleotide Transformer: building and evaluating robust
foundation models for human genomics. *Nat. Methods* **22**, 287–297 (2025).
https://doi.org/10.1038/s41592-024-02523-z

NTv3: A foundational model for joint sequence-function multi-species modeling at
scale for long-range genomic prediction. *bioRxiv*
https://doi.org/10.64898/2025.12.22.695963 (2025).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

**NT / NT-v2**: representation DNA LMs (embeddings, phenotype-related
fine-tunes). **NTv3**: unifies representation learning, functional-track /
annotation prediction, and controllable generation; U-Net-like, single-base
tokens, contexts up to ~1 Mb; pretrained on OpenGenome2 then post-trained on
multi-species tracks.

| vs | Prefer NT family when |
|----|------------------------|
| `evo2` | Embeddings / tracks / annotation heads (not primarily AR design) |
| `omg` / gLM2 | Multi-species DNA tracks; not specifically OMG mixed AA+DNA corpus |
| `mmseqs2` | Learned DNA features vs classical homology |

License is often **CC BY-NC-SA** — confirm before commercial use. Prefer
multi-species / OpenGenome-pretrained checkpoints for microbes over human-only
variants.

## How to run

This reviewed smoke pattern uses the classic JAX NT-v2 API; it downloads a named checkpoint and verifies the returned embedding tensor.

```bash
python - <<'PY'
import haiku as hk
import jax
import jax.numpy as jnp
from nucleotide_transformer.pretrained import get_pretrained_model

model_name = "250M_multi_species_v2"
parameters, forward_fn, tokenizer, config = get_pretrained_model(
    model_name=model_name, embeddings_layers_to_save=(20,), max_positions=32)
forward_fn = hk.transform(forward_fn)
seqs = ["ATTCCGATTCCGATTCCG", "ATTTCTCTCTCTCTCTGAGATCGATCGATCGAT"]
tokens = jnp.asarray([x[1] for x in tokenizer.batch_tokenize(seqs)], dtype=jnp.int32)
out = forward_fn.apply(parameters, jax.random.PRNGKey(0), tokens)
assert out["embeddings_20"].shape[0] == len(seqs)
print(model_name, out["embeddings_20"].shape)
PY
```

NTv3 uses `nucleotide_transformer_v3.pretrained.get_pretrained_ntv3_model`, single-base tokens, and sequence lengths divisible by `2^num_downsamples`; do not apply NT-v2 code or biological heads to NTv3. Pin repository commit, exact checkpoint revision, layer, chunk/strand pooling and maximum context.

## Decision tree

```text
DNA foundation model need?
├─ Embeddings / NTv3 tracks & annotation → nucleotide-transformer
├─ Efficient multi-species / GUE → dnabert2
├─ Long-range RC-aware → caduceus
├─ Long-context generative design (all domains) → evo2
├─ Metagenomic mixed-modality gLM2 → omg
└─ Protein homology → homology-search / plmsearch
```

## Validation, recovery, and provenance

Validate alphabet, sequence IDs, length/chunk/padding masks, forward and reverse-complement handling, finite tensor shape/dtype, and deterministic behavior under the documented backend. Include controls/held-out labels for any fine-tuned task and compare to homology/baseline models without leakage. A successful tensor operation is not biological validation.

Cache checksummed model artifacts and write embeddings atomically with ID-to-row metadata. Record package/JAX/CUDA versions, device, checkpoint repository and immutable revision/hash, tokenizer/config, code, seeds, input checksums, pooling and output checksum. Embedding similarity, functional tracks and generated sequence are model predictions; microbial transfer requires domain-specific validation.

## Related skills

`genome-language-model` · `dnabert2` · `caduceus` · `evo2` · `omg` ·
`metagenomics-llm` · `homology-search` · `tool-selection`
