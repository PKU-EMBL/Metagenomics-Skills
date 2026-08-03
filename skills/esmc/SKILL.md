---
name: esmc
description: >
  ESM C / ESM Cambrian (ESMC) — next-generation protein representation language
  models scaling beyond ESM-2 (300M / 600M open weights; larger tiers may need
  Forge/API). Use when: (1) Stronger AA embeddings than ESM-2 for metagenomic
  proteins, (2) Representation learning (not ESM3-style controllable generation),
  (3) Downstream heads that benefit from Cambrian checkpoints. Upstream:
  https://github.com/evolutionaryscale/esm (Biohub/esm). Route via
  protein-language-model. Keep ESM-2 workflows on esm when pinned for
  reproducibility.
license: MIT
category: analysis-tools
tags: [ESMC, ESM-C, ESM-Cambrian, PLM, protein-language-model, EvolutionaryScale]
upstream: https://github.com/evolutionaryscale/esm
stage: function
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

See also [docs/references.md](../../docs/references.md).

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

```bash
# install current EvolutionaryScale / Biohub esm package per upstream README
# typical: load esmc_300m / esmc_600m (exact IDs change — verify README tag)
# embed sequences → mean / per-residue vectors for clustering or classifiers
```

Do not invent API method names — follow the installed `esm` package docs.

## Decision tree

```text
Need modern protein embeddings?
├─ ESM C / Cambrian checkpoints → esmc
├─ Legacy / pinned ESM-2 pipelines → esm
├─ Structure-aware AA+3Di tokens → saprot
├─ Foldseek 3Di from FASTA → prostt5
└─ Remote homology wrappers → plmsearch / deepblast
```

## Related skills

`protein-language-model` · `esm` · `saprot` · `prostt5` · `plmsearch` ·
`deepblast` · `foldseek` · `metagenomics-llm` · `tool-selection`
