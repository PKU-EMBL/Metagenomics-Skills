---
name: fegenie
description: >
  FeGenie — HMM-based identification of iron-related genes and neighborhoods
  in genomes/metagenome assemblies (acquisition, siderophores, Fe redox,
  storage, magnetosome). Use for Fe cycling potential on contigs or MAGs.
  Upstream: https://github.com/Arkadiy-Garber/FeGenie. Route via
  element-cycling / microbial-mining. Broader C/N/S → metabolic; S scores → mebs.
license: MIT
category: analysis-tools
tags: [FeGenie, iron, Fe, siderophore, biogeochemistry, element-cycling]
upstream: https://github.com/Arkadiy-Garber/FeGenie
stage: mining
---

# FeGenie

Upstream: [Arkadiy-Garber/FeGenie](https://github.com/Arkadiy-Garber/FeGenie)

## Citation

Garber, A. I. *et al.* FeGenie: A Comprehensive Tool for the Identification of
Iron Genes and Iron Gene Neighborhoods in Genome and Metagenome Assemblies.
*Front. Microbiol.* **11**, 37 (2020).
https://doi.org/10.3389/fmicb.2020.00037

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

FeGenie targets **iron**: transport/acquisition, **siderophores**, oxidation /
dissimilatory reduction, storage, magnetosome-related genes, and neighborhoods.
Complements generic KO annotation that often misses Fe redox markers.

| vs | Prefer FeGenie when |
|----|---------------------|
| `metabolic` / `dram` | Fe-specific gene families and operon context |
| `mebs` | Explicit Fe gene calls vs cycle entropy scores |
| `antismash` | Siderophore BGC context vs FeGenie HMM categories |

Hits ≠ demonstrated Fe flux or siderophore production.

## How to run

```bash
# follow upstream README / wiki Tutorial — folder of genome or assembly FASTA
# provide bundled HMM library + bitscore cutoffs; pin FeGenie commit + HMM set
```

## Decision tree

```text
Iron / siderophore genetic potential?
├─ Yes → fegenie
├─ Multi-element C/N/S diagrams → metabolic
├─ S/N/CH₄/Fe scores → mebs
└─ Broad distillate → dram
```

## Related skills

`element-cycling` · `metabolic` · `mebs` · `dram` · `antismash` ·
`microbial-mining` · `tool-selection`
