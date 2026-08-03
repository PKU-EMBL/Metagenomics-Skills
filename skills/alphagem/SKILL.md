---
name: alphagem
description: >
  AlphaGEM — genome-scale metabolic modelling aided by protein structure
  alignment and deep-learning dark-metabolism mining. Use when: (1) Building
  or refining GEMs beyond sequence-only gap filling, (2) Integrating structure
  signals into metabolic networks, (3) Comparing to gapseq / VMH workflows.
  Upstream: https://github.com/hongzhonglu/AlphaGEM. Route via
  metagenomics-llm; pair with gapseq / vmh for classical GEM context.
license: MIT
category: analysis-tools
tags: [AlphaGEM, GEM, metabolism, structure, deep-learning]
upstream: https://github.com/hongzhonglu/AlphaGEM
stage: mining
---

# AlphaGEM

Upstream: [hongzhonglu/AlphaGEM](https://github.com/hongzhonglu/AlphaGEM)

## Citation

Han, W. *et al.* AlphaGEM enables precise genome-scale metabolic modelling by
integrating protein structure alignment with deep-learning-based dark
metabolism mining. *Nat. Commun.* (2026).
https://doi.org/10.1038/s41467-026-75549-w

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Sequence-only GEM reconstruction misses “dark” metabolism. AlphaGEM combines
**structure alignment** with DL mining to improve genome-scale models. Use on
high-quality genomes/MAGs after `mag-qc`; interpret human/gut context with
`vmh` when relevant.

Models remain computational — not measured fluxes. Pin AlphaGEM version,
structure sources (e.g. AFDB), and gap-filling rules.

## How to run

```bash
# follow upstream README for structure DBs and GEM reconstruction steps
```

## Decision tree

```text
Metabolic modelling need?
├─ Classical pathway/GEM from MAG → gapseq
├─ Structure + dark metabolism mining → alphagem
├─ Human/gut knowledge integration → vmh
└─ Annotation distillate only → dram
```

## Related skills

`metagenomics-llm` · `gapseq` · `vmh` · `dram` · `deepblast` · `mag-qc` ·
`microbial-mining` · `tool-selection`
