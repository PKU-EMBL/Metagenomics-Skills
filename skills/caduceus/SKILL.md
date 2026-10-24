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
  metagenomics.maturity: "reviewed-experimental"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "pinned Hugging Face masked-LM smoke test statically reviewed; not executed here"
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
import importlib.metadata as md
import json, os, sys
from pathlib import Path
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

if len(sys.argv) != 2:
    raise SystemExit("usage: python smoke_caduceus.py FRESH_OUTPUT_DIR")
out = Path(sys.argv[1])
if out.exists():
    raise SystemExit(f"refusing to overwrite: {out}")
out.mkdir(parents=True)
log = (out / "run.log").open("w")
sys.stdout = log; sys.stderr = log
model_name = os.getenv(
    "CADUCEUS_MODEL",
    "kuleshov-group/caduceus-ph_seqlen-131k_d_model-256_n_layer-16")
revision = os.getenv(
    "CADUCEUS_REVISION", "b0477522ac5d044ad03578aa724ec8e4bdbd405b")
sequence = os.getenv("CADUCEUS_SMOKE_SEQUENCE", "ACGTACGTACGT")
if not sequence or set(sequence.upper()) - set("ACGTN"):
    raise ValueError("smoke sequence must contain only A/C/G/T/N")
tokenizer = AutoTokenizer.from_pretrained(
    model_name, revision=revision, trust_remote_code=True)
model = AutoModelForMaskedLM.from_pretrained(
    model_name, revision=revision, trust_remote_code=True).eval()
batch = tokenizer(sequence, return_tensors="pt", truncation=False)
with torch.inference_mode():
    logits = model(**batch).logits
assert logits.shape[:2] == batch["input_ids"].shape
torch.save(logits.cpu(), out / "smoke-logits.pt")
metadata = {
    "model": model_name, "revision": revision, "sequence_length": len(sequence),
    "token_shape": list(batch["input_ids"].shape), "logit_shape": list(logits.shape),
    "torch": torch.__version__, "transformers": md.version("transformers")}
(out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
assert (out / "smoke-logits.pt").stat().st_size > 0
assert (out / "metadata.json").stat().st_size > 0
print(json.dumps(metadata, sort_keys=True))
log.flush()
sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__
log.close()
```

Run as `python smoke_caduceus.py fresh_output_dir`. Reconfirm and deliberately
update the immutable revision when changing checkpoints. Use the `ps` family only
when reverse-complement equivariance is required; record strand pooling, windowing,
overlap and aggregation for real sequences. The smoke test only verifies loading
and tensor shape, not downstream validity.

## Decision tree

```text
Long DNA representation LM?
├─ RC-aware / long-range Mamba → caduceus
├─ Multi-species efficient transformer → dnabert2
├─ NTv3 / NT family → nucleotide-transformer
└─ Generative all-domains → evo2
```

## Validation, recovery, and provenance

For a real task, require immutable train/validation/test units, leakage checks at
homology/genome level, strand/RC policy, context-window audit, baseline models,
calibration, subgroup metrics, uncertainty and held-out evaluation. Test RC
behavior directly for claims of invariance/equivariance. Do not infer function,
taxonomy or phenotype from embedding proximity without task validation.

Use fresh outputs after any sequence/model/code/device change. Record model family
(`ph`/`ps`), full revision and license, remote-code review, tokenizer/config,
software/container/device/precision, input/split checksums, seeds, window/pooling,
commands/logs, artifacts and metrics. Never silently truncate long sequences.

## Related skills

`genome-language-model` · `dnabert2` · `nucleotide-transformer` · `evo2` ·
`omg` · `tool-selection`
