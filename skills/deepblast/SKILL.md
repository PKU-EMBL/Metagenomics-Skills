---
name: deepblast
description: >
  TM-Vec and DeepBLAST — deep learning for protein remote homology and
  structural alignment from sequences (predict TM-scores; align homologous
  regions without solved structures). Use when: (1) Searching structure-like
  similarity in large sequence DBs, (2) Aligning remote homologs for annotation,
  (3) Complementing PLMSearch / Foldseek workflows. Upstream:
  https://github.com/tymor22/tm-vec and
  https://github.com/flatironinstitute/deepblast. Route via protein-language-model.
license: MIT
category: analysis-tools
tags: [DeepBLAST, TM-Vec, remote-homology, structure, PLM]
upstream: https://github.com/flatironinstitute/deepblast
stage: function
---

# TM-Vec / DeepBLAST

Upstream: [tm-vec](https://github.com/tymor22/tm-vec) ·
[deepblast](https://github.com/flatironinstitute/deepblast)

## Citation

Hamamsy, T. *et al.* Protein remote homology detection and structural alignment
using deep learning. *Nat. Biotechnol.* **42**, 975–985 (2024).
https://doi.org/10.1038/s41587-023-01917-2

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

| Component | Role |
|-----------|------|
| **TM-Vec** | Predict structural similarity (TM-score-like) from sequence pairs; search large DBs |
| **DeepBLAST** | Structurally align proteins from sequence by identifying homologous regions |

Designed for the metagenomic reality that many proteins lack close sequence
neighbors but retain structural homology. Complementary to `plmsearch` and to
structure search (Foldseek) when structures/pLDDT models exist.

## How to run

```bash
# install per wiki: https://github.com/flatironinstitute/deepblast/wiki/Installation
# typical: TM-Vec search → DeepBLAST align top hits
```

## Decision tree

```text
Remote homology workflow?
├─ Fast PLM embedding search → plmsearch
├─ TM-score search + structural alignment → deepblast (TM-Vec)
├─ Have structures / AFDB → foldseek (± folddisco / spacedust)
└─ Close homologs → mmseqs2 / diamond
```

## Related skills

`protein-language-model` · `esm` · `plmsearch` · `metagenomics-llm` ·
`foldseek` · `folddisco` · `spacedust` · `mmseqs2` · `eggnog-mapper` ·
`tool-selection`
