---
name: comebin
description: >
  COMEBin — contrastive multi-view representation learning for metagenomic
  contig binning (composition + coverage). Use when: (1) Running COMEBin as a
  modern single binner, (2) Comparing to SemiBin2/VAMB/MetaBAT2, (3) Co-
  assembly, single-sample, or multi-sample binning modes, (4) Feeding bins into
  ensemble refinement. Upstream: https://github.com/ziyewang/COMEBin.
  Prefer ensemble (basalt ★ / metawrap / dastool) for catalogues.
license: MIT
category: analysis-tools
tags: [binning, COMEBin, contrastive-learning, MAG]
upstream: https://github.com/ziyewang/COMEBin
stage: binning
---

# COMEBin

Upstream: [ziyewang/COMEBin](https://github.com/ziyewang/COMEBin)

## Citation

Wang, Z. *et al.* Effective binning of metagenomic contigs using contrastive
multi-view representation learning. *Nat. Commun.* **15**, 585 (2024).
https://doi.org/10.1038/s41467-023-44290-z

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

COMEBin learns contig embeddings with **contrastive multi-view** learning:
data augmentation creates multiple views per contig; a coverage module maps
variable sample counts to fixed-dimensional coverage embeddings. Benchmarks
(CAMI II and real data) show strong near-complete MAG recovery without
SemiBin1-style taxonomic semi-supervision.

Use as a **diverse single-binner** in ensembles (different inductive bias from
MetaBAT2 / MaxBin2 / VAMB). Prefer multi-coverage inputs when related samples
exist (Mattock & Watson 2023 — single-coverage hides contamination).

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Contigs | Assembly FASTA |
| Coverage | Multi-sample BAM/abundance when available |
| QC | `checkm2` after binning |

## How to run

```bash
# confirm exact CLI in upstream README
COMEBin.sh \
  -a contigs.fa \
  -o temp/bins/comebin \
  -p temp/map \
  -t 32
```

## Decision tree

```text
Single binner choice?
├─ Classical TNF+coverage → metabat2 / concoct / maxbin2
├─ VAE latent → vamb
├─ Self-supervised contrastive → semibin2
├─ Multi-view contrastive → comebin
└─ Catalogue / multi-assembly → basalt ★ (ensemble)
```

## Methods caveats

- Contrastive gains are benchmark-specific; always QC with CheckM2/GUNC.
- Report mode (co-assembly / single / multi-sample) and coverage recipe.
- Combine with ensemble tools rather than publishing one binner’s raw dump.

## Related skills

`semibin2` · `vamb` · `metabat2` · `basalt` · `dastool` · `checkm2` ·
`tool-selection` · `metagenomics-workflow`
