---
name: esmc
description: >
  ESM C / ESM Cambrian (ESMC) — next-generation protein representation language models
  scaling beyond ESM-2 (300M / 600M open weights; larger tiers may need Forge/API). Use
  when: (1) Stronger AA embeddings than ESM-2 for metagenomic proteins, (2)
  Representation learning (not ESM3-style controllable generation), (3) Downstream heads
  that benefit from Cambrian checkpoints. Keep ESM-2 workflows on esm when pinned for
  reproducibility.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ESMC, ESM-C, ESM-Cambrian, PLM, protein-language-model, EvolutionaryScale"
  metagenomics.upstream: "https://github.com/evolutionaryscale/esm"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "esm 3.4.1.post1; ESMC-600M revision fcc9d36f"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "local Hugging Face API reviewed; not executed here"
---

# ESM C (ESM Cambrian / ESMC)

Upstream: [evolutionaryscale/esm](https://github.com/evolutionaryscale/esm) ·
Blog: https://www.evolutionaryscale.ai/blog/esm-cambrian ·
Biohub: https://biohub.org/blog/esm-cambrian-unsupervised-learning

## Citation

Candido, S. *et al.* Language Modeling Materializes a World Model of Protein
Biology. *bioRxiv* https://doi.org/10.64898/2026.06.03.729735 (2026).

Interim blog (if preprint not yet cited in Methods): ESM Team. ESM Cambrian:
Revealing the mysteries of proteins with unsupervised learning (2024).
https://www.evolutionaryscale.ai/blog/esm-cambrian

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

**ESM C** is the representation-learning sibling of generative **ESM3**. It
targets embeddings / biological understanding with a new scaling frontier vs
**ESM-2**. Open weights commonly discussed: **300M** and **600M**; larger
(e.g. 6B) tiers may require Forge / commercial endpoints — pin license and
access path.

| vs | Prefer ESMC when |
|----|------------------|
| `esm` (ESM-2) | New embedding jobs that can adopt Cambrian checkpoints |
| `saprot` | Sequence-only representation; not Foldseek SA-token PLM |
| `prostt5` | Embeddings / property heads — not AA↔3Di for Foldseek DB build |
| ESM3 | Representation vs multimodal controllable generation |

Do not silently swap ESM-2 for ESMC in published PLMSearch/LucaPhylo-style
pipelines without re-benchmarking. Check academic vs commercial terms for each
size.

## How to run

Use the local Hugging Face path for reproducible weights; platform/API execution has separate credentials, terms and remote-service provenance.

```python
import torch
from esm.models.esmc import EsmcForMaskedLM, EsmcTokenizer

repo = "biohub/ESMC-600M"
revision = "fcc9d36f5fff97d9bb69a36e3252de61cc78c968"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = EsmcForMaskedLM.from_pretrained(repo, revision=revision, device=device).eval()
tokenizer = EsmcTokenizer()
inputs = tokenizer(["MKTIIALSYIFCLVFADYKDDDDK"], return_tensors="pt", padding=True)
inputs = {k: v.to(device) for k, v in inputs.items()}
with torch.inference_mode():
    output = model(**inputs)
assert output.last_hidden_state.shape[:2] == inputs["input_ids"].shape
assert torch.isfinite(output.last_hidden_state).all()
print(repo, revision, tuple(output.last_hidden_state.shape))
```

Pin checkpoint size, dtype, hidden layer, pooling and token budget. Do not silently substitute a 6B/platform result for the open 600M local model.

## Decision tree

```text
Need modern protein embeddings?
├─ ESM C / Cambrian checkpoints → esmc
├─ Legacy / pinned ESM-2 pipelines → esm
├─ Structure-aware AA+3Di tokens → saprot
├─ Foldseek 3Di from FASTA → prostt5
└─ Remote homology wrappers → plmsearch / deepblast
```

## Validation, recovery, and provenance

Validate input alphabet/IDs, truncation, padding and special-token masks, finite per-residue/pooled tensors, output row order and known controls. Benchmark any downstream head on identity-aware held-out splits and repeat published ESM-2 comparisons if switching models. A forward pass does not validate biological performance.

Record `esm`/PyTorch/CUDA versions, model repository and immutable revision, tokenizer/config hashes, access route/license, device/dtype, pooling/batching, code/seeds and input/output checksums. Embedding proximity remains model-derived evidence, not direct homology, structure or function.

## Related skills

`protein-language-model` · `esm` · `saprot` · `prostt5` · `plmsearch` ·
`deepblast` · `foldseek` · `metagenomics-llm` · `tool-selection`
