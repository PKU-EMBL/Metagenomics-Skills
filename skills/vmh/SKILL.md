---
name: vmh
description: >
  Virtual Metabolic Human (VMH) database — human and gut microbiome metabolism
  integrated with nutrition and disease knowledge for GEM interpretation.
  Use when: (1) Contextualizing gapseq / AGORA-style models, (2) Linking
  metabolites, microbes, and nutrition, (3) Browsing human–microbiome metabolic
  resources. Portal: https://www.vmh.life. Pair with gapseq for reconstruction;
  do not treat VMH entries as measured fluxes in your sample.
license: MIT
category: utilities
tags: [VMH, GEMs, metabolism, database, gut]
upstream: https://www.vmh.life
---

# Virtual Metabolic Human (VMH)

Portal: https://www.vmh.life

## Citation

Noronha, A. *et al.* The Virtual Metabolic Human database: integrating human and
gut microbiome metabolism with nutrition and disease. *Nucleic Acids Res.*
**47**, D614–D624 (2019). https://doi.org/10.1093/nar/gky992

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

VMH is a **knowledge/integration database** (human + gut microbial metabolism,
nutrition, disease links), not a shotgun profiler. Use it to interpret
genome-scale models and metabolites after `gapseq` (or related GEM tools).

| Resource | Role |
|----------|------|
| `gapseq` | Build/fill models from your genomes/MAGs |
| `vmh` | Browse/integrate human–microbiome metabolic knowledge |
| `kegg` / `dram` | Pathway annotation alternatives |

## Decision tree

```text
Metabolic modeling need?
├─ Reconstruct model from MAG → gapseq
├─ Interpret vs human/gut/nutrition knowledge → vmh
├─ Distill annotations without full GEM → dram
└─ KO maps → kegg (license)
```

## Related skills

`gapseq` · `dram` · `kegg` · `public-databases` · `microbial-mining`
