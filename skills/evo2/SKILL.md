---
name: evo2
description: >
  Evo 2 — long-context DNA language model for genome modeling and design across all
  domains of life (Arc Institute; StripedHyena 2 / OpenGenome2). Use when: (1)
  Autoregressive DNA likelihoods or embeddings at up to ~1 Mb context, (2) Sequence
  generation / design, (3) Contrasting generative gLMs with Nucleotide Transformer or
  gLM2. Predecessor: Evo (Science 2024). Heavy GPU requirements.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Evo2, Evo, gLM, DNA, generative, OpenGenome2, Arc-Institute"
  metagenomics.upstream: "https://github.com/ArcInstitute/evo2"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-experimental"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "current Vortex forward-pass interface checked against upstream README; not executed here"
---

# Evo 2

Upstream: [ArcInstitute/evo2](https://github.com/ArcInstitute/evo2) ·
Dataset: https://huggingface.co/datasets/arcinstitute/opengenome2

## Citation

Brixi, G. *et al.* Genome modelling and design across all domains of life with
Evo 2. *Nature* https://doi.org/10.1038/s41586-026-10176-5 (2026).

Nguyen, E. *et al.* Sequence modeling and design from molecular to genome scale
with Evo. *Science* **386**, eado9336 (2024).
https://doi.org/10.1126/science.ado9336

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Evo 2 is a **generative / long-context** DNA LM (single-nucleotide resolution,
contexts up to ~1M bp) pretrained on **OpenGenome2** (~8.8T tokens, all domains).
Checkpoints include `evo2_7b` (widest hardware reach) through `evo2_40b` (FP8 /
Hopper-class for full accuracy per upstream).

| vs | Prefer Evo 2 when |
|----|-------------------|
| `nucleotide-transformer` | Generation / long AR likelihoods across domains |
| `omg` / gLM2 | Pure DNA generative modeling vs mixed AA+DNA metagenomic LM |
| Classical assemblers | Design/scoring sequences — not contig assembly |

Intermediate-layer embeddings often work better than final layer (per paper).
Validate outputs after hardware/config changes (upstream tests).

## How to run

```python
import importlib.metadata as md
import json, os, sys
from pathlib import Path
import torch
from evo2 import Evo2

if len(sys.argv) != 2:
    raise SystemExit("usage: python smoke_evo2.py FRESH_OUTPUT_DIR")
out = Path(sys.argv[1])
if out.exists():
    raise SystemExit(f"refusing to overwrite: {out}")
out.mkdir(parents=True)
log = (out / "run.log").open("w")
sys.stdout = log; sys.stderr = log
if not torch.cuda.is_available():
    raise RuntimeError("Evo 2 local inference requires a supported CUDA GPU")
model_name = os.getenv("EVO2_MODEL", "evo2_7b")
sequence = os.getenv("EVO2_SMOKE_SEQUENCE", "ACGT")
if not sequence or set(sequence.upper()) - set("ACGTN"):
    raise ValueError("smoke sequence must contain only A/C/G/T/N")
model = Evo2(model_name)
input_ids = torch.tensor(model.tokenizer.tokenize(sequence), dtype=torch.int)
input_ids = input_ids.unsqueeze(0).to("cuda:0")
with torch.inference_mode():
    outputs, _ = model(input_ids)
logits = outputs[0]
torch.save(logits.cpu(), out / "smoke-logits.pt")
metadata = {
    "model": model_name, "sequence_length": len(sequence),
    "input_shape": list(input_ids.shape), "logit_shape": list(logits.shape),
    "evo2_package": md.version("evo2"), "torch": torch.__version__,
    "gpu": torch.cuda.get_device_name(0)}
(out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
assert (out / "smoke-logits.pt").stat().st_size > 0
print(json.dumps(metadata, sort_keys=True))
log.flush()
sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__
log.close()
```

Run as `python smoke_evo2.py fresh_output_dir` in a pinned CUDA/container stack.
The smoke test verifies a forward pass only. Embedding work must name the layer;
generation must freeze prompt, sampling parameters and seed, retain all outputs,
and follow institutional sequence-design governance. Hosted API/NIM use must
record endpoint/model version and data-governance terms.

## Decision tree

```text
Long DNA LM / design?
├─ Generative + all-domains pretrain → evo2
├─ Multi-species tracks / NTv3 representation → nucleotide-transformer
├─ Efficient / long-range representation → dnabert2 / caduceus
├─ Metagenomic gLM2 / OMG corpus → omg
└─ Classical search → homology-search
```

## Validation, recovery, and provenance

Run upstream hardware/configuration tests, then validate task outputs with frozen
positive/negative controls, classical baselines, leakage-aware splits, multiple
seeds, calibration and external or held-out data. Inspect context boundaries,
strand treatment, layer choice, numerical precision, likelihood normalization,
generation diversity/validity and hardware reproducibility. Model likelihood or
generation is not biological function, fitness, safety or experimental success.

Use fresh outputs after changing sequence, model, package, kernels, device or
settings. Record model name/weights identity and license, Evo2/Vortex/container
commits, CUDA/cuDNN/driver/GPU/precision, input/split checksums, layer/prompt,
seeds/sampling, commands/logs, raw artifacts and metrics. Never claim a 1 Mb
context was used unless the actual tokenized length and memory path were logged.

## Related skills

`genome-language-model` · `nucleotide-transformer` · `dnabert2` · `caduceus` ·
`omg` · `metagenomics-llm` · `lucaphylo` · `tool-selection`
