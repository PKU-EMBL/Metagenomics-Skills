---
name: esm
description: >
  ESM-2 family protein language models (ESMFold / ESM Atlas). Use when: (1)
  Amino-acid embeddings or MLM scores pinned to ESM-2, (2) Single-sequence
  structure context (ESMFold) or ESM Metagenomic Atlas via Foldseek, (3)
  Backbone embeddings for PLMSearch / LucaPhylo-style workflows. For ESM C /
  Cambrian prefer esmc. Upstream: https://github.com/facebookresearch/esm.
  Route via protein-language-model.
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

```bash
# install per upstream README (fair-esm / torch); or HF ports of ESM-2
# typical: load esm2_* checkpoint → per-residue / mean embeddings
# structure: ESMFold API / local — heavy GPU; prefer AFDB/Atlas + foldseek for catalogues
```

Do not invent CLI flags — follow the installed package docs for the pinned tag.

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

## Related skills

`protein-language-model` · `esmc` · `saprot` · `prostt5` · `plmsearch` ·
`deepblast` · `lucaphylo` · `foldseek` · `metagenomics-llm` · `tool-selection`
