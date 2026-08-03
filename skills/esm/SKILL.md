---
name: esm
description: >
  ESM family protein language models (ESM-2 primary; note ESMFold / ESM Atlas /
  later ESM variants). Use when: (1) Amino-acid embeddings or MLM scores for
  metagenomic proteins, (2) Single-sequence structure context (ESMFold) or
  ESM Metagenomic Atlas structures via Foldseek, (3) Backbone embeddings for
  PLMSearch / LucaPhylo-style workflows. Upstream:
  https://github.com/facebookresearch/esm. Route via protein-language-model.
license: MIT
category: analysis-tools
tags: [ESM, ESM-2, ESMFold, PLM, protein-language-model, embeddings, HuggingFace]
upstream: https://github.com/facebookresearch/esm
stage: function
---

# ESM (ESM-2 / ESMFold)

Upstream: [facebookresearch/esm](https://github.com/facebookresearch/esm) ·
Atlas: https://esmatlas.com

## Citation

Lin, Z. *et al.* Evolutionary-scale prediction of atomic-level protein structure
with a language model. *Science* **379**, 1123–1130 (2023).
https://doi.org/10.1126/science.ade2574

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

**ESM-2** is the workhorse representation PLM for many metagenomic embedding /
remote-homology pipelines. Scaling enables **ESMFold** (single-sequence
structure) and the **ESM Metagenomic Atlas** (hundreds of millions of predicted
metagenomic structures — search via `foldseek`, not by re-folding every ORF).

| vs | Prefer ESM when |
|----|-----------------|
| `prostt5` | AA embeddings / MLM; not AA↔3Di translation |
| `plmsearch` / `deepblast` | Need the foundation model itself vs a search wrapper |
| `foldseek` | Embedding/property tasks; use Foldseek for Atlas/AFDB hits |
| `lucaphylo` | Raw ESM embeddings vs hyperbolic placement product |

Pin checkpoint (e.g. `esm2_t33_650M_UR50D` vs larger), truncation length, and that
Atlas/pLDDT structures remain computational. Later ESM releases (ESM3 / ESM C)
— cite their papers separately if used.

## How to run

```bash
# install per upstream README (fair-esm / torch); or HF ports of ESM-2
# typical: load esm2_* checkpoint → per-residue / mean embeddings
# structure: ESMFold API / local — heavy GPU; prefer AFDB/Atlas + foldseek for catalogues
```

Do not invent CLI flags — follow the installed package docs for the pinned tag.

## Decision tree

```text
Protein LM / structure from sequence?
├─ AA embeddings / scores → esm
├─ Sequence → 3Di for Foldseek → prostt5
├─ Remote homology wrappers → plmsearch / deepblast
├─ Search Atlas / AFDB structures → foldseek
└─ DNA gLMs → genome-language-model
```

## Related skills

`protein-language-model` · `prostt5` · `plmsearch` · `deepblast` · `lucaphylo` ·
`foldseek` · `metagenomics-llm` · `tool-selection`
