---
name: evo2
description: >
  Evo 2 — long-context DNA language model for genome modeling and design across
  all domains of life (Arc Institute; StripedHyena 2 / OpenGenome2). Use when:
  (1) Autoregressive DNA likelihoods or embeddings at up to ~1 Mb context,
  (2) Sequence generation / design, (3) Contrasting generative gLMs with
  Nucleotide Transformer or gLM2. Upstream: https://github.com/ArcInstitute/evo2.
  Predecessor: Evo (Science 2024). Route via genome-language-model. Heavy GPU requirements.
license: MIT
category: analysis-tools
tags: [Evo2, Evo, gLM, DNA, generative, OpenGenome2, Arc-Institute]
upstream: https://github.com/ArcInstitute/evo2
stage: function
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

See also [docs/references.md](../../docs/references.md).

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

```bash
# light path: 7B without Transformer Engine — see upstream Installation
pip install evo2   # after system CUDA / deps per README
python - <<'PY'
from evo2 import Evo2
import torch
evo2_model = Evo2('evo2_7b')
sequence = 'ACGT'
input_ids = torch.tensor(
    evo2_model.tokenizer.tokenize(sequence), dtype=torch.int
).unsqueeze(0).to('cuda:0')
# forward / embeddings / generation — see upstream Usage sections
PY
```

Also: NVIDIA hosted API / NIM options documented upstream.

## Decision tree

```text
Long DNA LM / design?
├─ Generative + all-domains pretrain → evo2
├─ Multi-species tracks / NTv3 representation → nucleotide-transformer
├─ Efficient / long-range representation → dnabert2 / caduceus
├─ Metagenomic gLM2 / OMG corpus → omg
└─ Classical search → homology-search
```

## Related skills

`genome-language-model` · `nucleotide-transformer` · `dnabert2` · `caduceus` ·
`omg` · `metagenomics-llm` · `lucaphylo` · `tool-selection`
