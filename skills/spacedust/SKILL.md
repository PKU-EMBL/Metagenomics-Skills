---
name: spacedust
description: >
  Spacedust — de novo discovery of conserved gene clusters in microbial genomes
  using Foldseek structure comparison plus clustering/order-conservation
  statistics. Use when: (1) Finding conserved neighborhoods / modules in MAG
  collections, (2) Annotating dark genes via genomic context, (3) Recovering
  defense or other systems as clusters. Upstream:
  https://github.com/soedinglab/Spacedust. Route via metagenomics-llm;
  complement defensefinder / antismash for known systems.
license: MIT
category: analysis-tools
tags: [Spacedust, gene-cluster, Foldseek, annotation, structure]
upstream: https://github.com/soedinglab/Spacedust
stage: mining
---

# Spacedust

Upstream: [soedinglab/Spacedust](https://github.com/soedinglab/Spacedust)

## Citation

Zhang, R., Mirdita, M. & Söding, J. De novo discovery of conserved gene clusters
in microbial genomes with Spacedust. *Nat. Methods* (2025).
https://doi.org/10.1038/s41592-025-02816-x

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

In prokaryotes/viruses, **gene neighborhood conservation** signals functional
association. Spacedust finds conserved clusters de novo with sensitive
**Foldseek** structure comparison and order-conservation statistics — useful
when sequence annotation covers only a fraction of genes.

Paper-scale demonstration: all-vs-all on >1k bacterial genomes recovered large
fractions of genes in conserved clusters and most PADLOC-annotated antiviral
defense clusters — still validate priority systems with specialized tools
(`defensefinder`, `antismash`, experiments).

| vs | Notes |
|----|-------|
| `antismash` | Known BGC rules vs de novo neighborhoods |
| `defensefinder` | Known defense HMMs vs de novo clusters |
| `eggnog-mapper` | Per-gene orthology vs multi-gene context |

## How to run

```bash
# follow upstream docs — typically genomes/proteomes → Foldseek → Spacedust clustering
```

## Decision tree

```text
Dark genes / modules in MAG sets?
├─ Conserved neighborhoods de novo → spacedust
├─ Known BGCs → antismash
├─ Known defense → defensefinder
└─ Per-gene orthology → eggnog-mapper
```

## Related skills

`metagenomics-llm` · `defensefinder` · `antismash` · `eggnog-mapper` ·
`deepblast` · `microbial-mining` · `tool-selection`
