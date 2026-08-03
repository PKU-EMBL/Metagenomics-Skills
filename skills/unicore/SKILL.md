---
name: unicore
description: >
  Unicore — universal structure-based core-gene phylogeny using Foldseek and
  ProstT5 (Steinegger lab). Use when: (1) Building phylogenies from proteomes
  via structural core genes, (2) 3Di MSAs for tree inference, (3) Scaling beyond
  sequence-only marker sets. Upstream: https://github.com/steineggerlab/unicore.
  Route via phylogenomics; depends on foldseek (± GPU ProstT5).
license: MIT
category: analysis-tools
tags: [Unicore, Foldseek, ProstT5, phylogeny, core-genes, 3Di]
upstream: https://github.com/steineggerlab/unicore
stage: taxonomy
---

# Unicore

Upstream: [steineggerlab/unicore](https://github.com/steineggerlab/unicore)

## Citation

Kim, D., Park, S. & Steinegger, M. Unicore enables scalable and accurate
phylogenetic reconstruction with structural core genes. *Genome Biol. Evol.*
**17**, evaf109 (2025). https://doi.org/10.1093/gbe/evaf109

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Unicore finds **structural core genes** across proteomes (Foldseek clustering /
ProstT5 3Di) and builds phylogenies — a Steinegger-stack alternative/complement
to sequence-marker workflows (`phylophlan` + `iqtree`).

| vs | Prefer Unicore when |
|----|---------------------|
| `phylophlan` / `iqtree` | Want structure/3Di core genes |
| `gtdbtk` | Custom structural phylogeny, not only GTDB labels |
| `lucaphylo` | Proteome-scale core-gene trees vs single-protein PLM placement |

GPU: `--gpu` with Foldseek≥10 / ProstT5 on Turing+ NVIDIA (see upstream).

## How to run

```bash
conda install -c bioconda unicore
# proteomes → structural cores → tree
unicore easy-core example/data example/results weights tmp
# GPU ProstT5 path
unicore easy-core --gpu example/data example/results weights tmp
```

## Decision tree

```text
Phylogeny from many proteomes/MAGs?
├─ GTDB taxonomy only → gtdbtk
├─ Sequence markers → phylophlan → iqtree
├─ Structural core genes / 3Di → unicore
└─ Single divergent protein family → lucaphylo / foldmason + iqtree
```

## Related skills

`phylogenomics` · `foldseek` · `foldmason` · `phylophlan` · `iqtree` ·
`gtdbtk` · `tool-selection`
