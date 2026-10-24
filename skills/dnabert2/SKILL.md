---
name: dnabert2
description: >
  DNABERT-2 — efficient multi-species genome language model (BPE + ALiBi) with the
  Genome Understanding Evaluation (GUE) benchmark. Use when: (1) DNA embeddings or
  fine-tunes on multi-species tasks, (2) Comparing representation gLMs without
  NT/Evo-scale hardware, (3) GUE-style evaluation. HF: zhihan1996/DNABERT-2-117M.
  Related: DNABERT (v1), DNABERT-S.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "DNABERT-2, DNABERT, gLM, genome-language-model, GUE, HuggingFace"
  metagenomics.upstream: "https://github.com/MAGICS-LAB/DNABERT_2"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-experimental"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "pinned Hugging Face embedding smoke test statically reviewed; not executed here"
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

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

DNABERT-2 replaces k-mer tokenization with **BPE** and uses **ALiBi** for
longer effective context vs DNABERT v1. Trained multi-species; evaluated on
**GUE** (28 datasets). Lighter than NT/Evo for many embedding/fine-tune jobs.

| vs | Prefer DNABERT-2 when |
|----|------------------------|
| `nucleotide-transformer` | Smaller model / GUE-centric workflows |
| `caduceus` | Transformer BPE stack vs Mamba long-range RC models |
| `evo2` | Representation / classification — not AR generation |

Related models such as **DNABERT-S** (species-separating embeddings) and **GenomeOcean** (generative) are distinct checkpoints/methods and require their own immutable source, license and citation.

## How to run

```python
import importlib.metadata as md
import json, os, sys
from pathlib import Path
import torch
from transformers import AutoModel, AutoTokenizer

if len(sys.argv) != 2:
    raise SystemExit("usage: python smoke_dnabert2.py FRESH_OUTPUT_DIR")
out_dir = Path(sys.argv[1])
if out_dir.exists():
    raise SystemExit(f"refusing to overwrite: {out_dir}")
out_dir.mkdir(parents=True)
log = (out_dir / "run.log").open("w")
sys.stdout = log; sys.stderr = log
model_name = "zhihan1996/DNABERT-2-117M"
revision = os.getenv(
    "DNABERT2_REVISION", "7bce263b15377fc15361f52cfab88f8b586abda0")
sequence = os.getenv("DNABERT2_SMOKE_SEQUENCE", "ACGTACGTACGT")
if not sequence or set(sequence.upper()) - set("ACGTN"):
    raise ValueError("smoke sequence must contain only A/C/G/T/N")
tok = AutoTokenizer.from_pretrained(
    model_name, revision=revision, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name, revision=revision, trust_remote_code=True).eval()
batch = tok(sequence, return_tensors="pt", truncation=False)
with torch.inference_mode():
    hidden = model(**batch)[0]
assert hidden.shape[:2] == batch["input_ids"].shape
mask = batch["attention_mask"].unsqueeze(-1)
pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)
torch.save(pooled.cpu(), out_dir / "smoke-embedding.pt")
metadata = {
    "model": model_name, "revision": revision, "sequence_length": len(sequence),
    "token_shape": list(batch["input_ids"].shape),
    "embedding_shape": list(pooled.shape), "torch": torch.__version__,
    "transformers": md.version("transformers")}
(out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
assert (out_dir / "smoke-embedding.pt").stat().st_size > 0
print(json.dumps(metadata, sort_keys=True))
log.flush()
sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__
log.close()
```

Run as `python smoke_dnabert2.py fresh_output_dir`. Reconfirm and deliberately
update the immutable revision when changing checkpoints. The shown masked mean is
a smoke artifact, not a universally optimal representation. Fine-tuning requires
a frozen split, labels, preprocessing, leakage checks, seeds and held-out
comparison; loading a checkpoint is not task validation.

## Decision tree

```text
Representation genome LM?
├─ Multi-species efficient / GUE → dnabert2
├─ NTv3 tracks / large NT family → nucleotide-transformer
├─ Long-range Mamba / RC-equivariant → caduceus
└─ Generative → evo2
```

## Validation, recovery, and provenance

For a real task, inspect token/window lengths, truncation, strand/RC augmentation,
pooling/layer choice, class balance, contamination and homology leakage, baseline
models, calibration, subgroup performance, uncertainty and external or held-out
results. Species clustering in a related model does not validate DNABERT-2 for
taxonomy or novelty claims.

Use fresh outputs after changing sequence, checkpoint, preprocessing, split,
code, or device. Record full model revision/license, trusted remote-code review,
tokenizer/config, software/container/device/precision, dataset/split checksums,
seeds, window/pooling, commands/logs, artifacts and complete metrics. Preserve
failed runs and never silently truncate inputs.

## Related skills

`genome-language-model` · `nucleotide-transformer` · `caduceus` · `evo2` ·
`omg` · `tool-selection`
