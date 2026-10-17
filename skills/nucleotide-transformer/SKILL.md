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

```bash
# install / notebooks: follow upstream docs/ and HF collections
# NT classic: https://huggingface.co/collections/InstaDeepAI/nucleotide-transformer-…
# NTv3: docs/nucleotide_transformer_v3.md · HF Space InstaDeepAI/ntv3
# typical: load HF checkpoint → tokenize DNA → embeddings or task head
```

Pin exact checkpoint (e.g. NT-v2 vs NTv3 size) and max context in Methods.

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

## Related skills

`genome-language-model` · `dnabert2` · `caduceus` · `evo2` · `omg` ·
`metagenomics-llm` · `homology-search` · `tool-selection`
