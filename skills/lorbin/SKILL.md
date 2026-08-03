---
name: lorbin
description: >
  LorBin — unsupervised long-read metagenome binning with multiscale adaptive
  clustering (DBSCAN + BIRCH) and single-copy-gene evaluation. Use when:
  (1) Binning long-read / HiFi metagenome assemblies, (2) Recovering MAGs from
  species-rich or abundance-imbalanced communities, (3) Comparing LorBin to
  SemiBin2/VAMB long-read modes, (4) Feeding LorBin bins into ensemble
  refinement (BASALT `-e l` needs the PKU-EMBL LorBin fork). Upstream:
  https://github.com/LorMeBioAI/LorBin. For ensemble recovery use basalt.
  For short-read defaults use metabat2 / semibin2 / vamb.
license: MIT
category: analysis-tools
tags: [binning, long-read, LorBin, MAG, DBSCAN]
upstream: https://github.com/LorMeBioAI/LorBin
stage: binning
---

# LorBin

Upstream: [LorMeBioAI/LorBin](https://github.com/LorMeBioAI/LorBin)

## Citation

Xue, W. *et al.* LorBin: efficient binning of long-read metagenomes by
multiscale adaptive clustering and evaluation. *Nat. Commun.* **16**, 9353
(2025). https://doi.org/10.1038/s41467-025-64916-8

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Long-read assemblies differ from short-read graphs: fewer, longer contigs,
sharper abundance separation, and often **unknown / imbalanced** taxa. Short-read
binners (and some DL tools trained mainly on short-read CAMI) under-recover
novel lineages in that regime.

LorBin is an **unsupervised** long-read binner: multiscale adaptive DBSCAN then
BIRCH, with iterative single-copy-gene evaluation to accept/recluster bins. The
paper reports large gains in high-quality MAGs and novel taxa vs several
competitors on oral, gut, and marine long-read sets — treat those as
**benchmark-conditioned**, not universal guarantees.

Within this package:

| Role | Skill |
|------|--------|
| Long-read single binner | `lorbin` (or SemiBin2 long-read mode) |
| Short-read single binners | `metabat2` · `semibin2` · `vamb` · `comebin` |
| Ensemble refinement | `basalt` ★ · `metawrap` · `dastool` |

If using **BASALT** with LorBin as an extra binner (`-e l`), use the
**PKU-EMBL LorBin fork commit** documented in the BASALT guide — not an
arbitrary upstream tip.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Assembly | Long-read / hybrid contigs (metaFlye, metaMDBG, …) |
| Coverage | BAM or abundance table as required by upstream CLI |
| QC | Always follow with `checkm2` (+ `gunc` for chimera risk) |

## How to run

Verify flags against upstream README/`--help` (CLI evolves):

```bash
# illustrative — confirm exact subcommands in LorBin docs
lorbin \
  --contigs long_contigs.fa \
  --bam temp/map/*.bam \
  --outdir temp/bins/lorbin \
  --threads 32
```

## Decision tree

```text
Long-read MAG recovery?
├─ Dedicated long-read binner → lorbin
├─ SemiBin2 long-read / ensemble-DBSCAN path → semibin2
├─ Multi-binner + refinement (related samples) → basalt ★
└─ Only short reads → prefer metabat2 / semibin2 / vamb (+ ensemble)
```

## Methods caveats

- Unsupervised clustering + SCG gates ≠ experimental species proof.
- Report assembler, read type (ONT/HiFi), LorBin version, and CheckM2 gates.
- Do not claim “novel phylum” from LorBin alone — require GTDB-Tk + literature
  placement and chimera screens (`gunc`).

## Related skills

`metaflye` · `metamdbg` · `semibin2` · `vamb` · `basalt` · `checkm2` · `gunc` ·
`tool-selection` · `metagenomics-workflow`
