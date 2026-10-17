---
name: esm
description: >
  ESM-2 family protein language models (ESMFold / ESM Atlas). Use when: (1) Amino-acid
  embeddings or MLM scores pinned to ESM-2, (2) Single-sequence structure context
  (ESMFold) or ESM Metagenomic Atlas via Foldseek, (3) Backbone embeddings for PLMSearch
  / LucaPhylo-style workflows. For ESM C / Cambrian prefer esmc.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ESM, ESM-2, ESMFold, PLM, protein-language-model, embeddings, HuggingFace"
  metagenomics.upstream: "https://github.com/facebookresearch/esm"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "ESM-2 checkpoint revision 08e4846e"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Transformers API reviewed; not executed here"
---

# ESM (ESM-2 / ESMFold)

Upstream: [facebookresearch/esm](https://github.com/facebookresearch/esm) ·
Atlas: https://esmatlas.com

## Citation

Lin, Z. *et al.* Evolutionary-scale prediction of atomic-level protein structure
with a language model. *Science* **379**, 1123–1130 (2023).
https://doi.org/10.1126/science.ade2574

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

**ESM-2** is the workhorse representation PLM for many metagenomic embedding /
remote-homology pipelines. Scaling enables **ESMFold** (single-sequence
structure) and the **ESM Metagenomic Atlas** (hundreds of millions of predicted
metagenomic structures — search via `foldseek`, not by re-folding every ORF).

| vs | Prefer ESM-2 when |
|----|-------------------|
| `esmc` | Reproducible / published ESM-2 pipelines |
| `saprot` | Sequence-only embeddings without SA tokens |
| `prostt5` | AA embeddings / MLM; not AA↔3Di translation |
| `plmsearch` / `deepblast` | Need the foundation model itself vs a search wrapper |
| `foldseek` | Embedding/property tasks; use Foldseek for Atlas/AFDB hits |

Pin checkpoint (e.g. `esm2_t33_650M_UR50D` vs larger), truncation length, and that
Atlas/pLDDT structures remain computational. For ESM C see `esmc`; generative
ESM3 — cite separately if used.

## How to run

This sequence-embedding smoke pattern uses a fixed Hugging Face ESM-2 revision; production code should batch by token budget and retain the attention mask and ID order.

```python
import torch
from transformers import AutoTokenizer, EsmModel

repo = "facebook/esm2_t33_650M_UR50D"
revision = "08e4846e537177426273712802403f7ba8261b6c"
tok = AutoTokenizer.from_pretrained(repo, revision=revision)
model = EsmModel.from_pretrained(repo, revision=revision).eval()
batch = tok(["MKTIIALSYIFCLVFADYKDDDDK"], return_tensors="pt", padding=True)
with torch.inference_mode():
    out = model(**batch).last_hidden_state
assert out.shape[:2] == batch["input_ids"].shape and torch.isfinite(out).all()
print(repo, revision, tuple(out.shape))
```

For ESMFold, pin its distinct model/dependencies and archive PDB plus per-residue confidence. At catalogue scale, search existing AFDB/ESM Atlas structures with `$foldseek` before deciding to refold every ORF.

## Decision tree

```text
Protein LM / structure from sequence?
├─ Pinned ESM-2 embeddings → esm
├─ ESM C / Cambrian → esmc
├─ Structure-aware AA+3Di → saprot
├─ Sequence → 3Di for Foldseek → prostt5
├─ Remote homology wrappers → plmsearch / deepblast
├─ Search Atlas / AFDB structures → foldseek
└─ DNA gLMs → genome-language-model
```

## Validation, recovery, and provenance

Validate protein alphabet, unique IDs, truncation/chunking, special-token exclusion, pooling denominator, finite tensors, row order and deterministic controls. Compare embeddings/heads on leakage-resistant held-out proteins; loading the checkpoint is only a software smoke test. Structure predictions require pLDDT/PAE-aware checks and should not be labeled experimental structures.

Record Transformers/PyTorch/CUDA versions, model repository and immutable revision, tokenizer/config hashes, device/dtype, batching/pooling/strand-independent protein policy, code/seeds, input/output checksums and failed sequences. Embeddings and structures are model predictions and do not independently establish homology or function.

## Related skills

`protein-language-model` · `esmc` · `saprot` · `prostt5` · `plmsearch` ·
`deepblast` · `lucaphylo` · `foldseek` · `metagenomics-llm` · `tool-selection`
