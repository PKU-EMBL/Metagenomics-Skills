---
name: plasmaag
description: >
  PlasMAAG — recover plasmids and cellular genomes from metagenomes using
  assembly–alignment graphs and contrastive learning across samples. Use when: (1)
  Plasmid MAG reconstruction beyond circular-path assemblers, (2) Improving plasmid
  contig classification vs geNomad alone, (3) Host–plasmid association across
  multi-sample datasets. Pair with genomad for MGE screening and checkv for viral (not
  plasmid) QC.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "plasmid, MAG, PlasMAAG, MGE, binning"
  metagenomics.upstream: "https://github.com/RasmussenLab/PlasMAAG"
  metagenomics.stage: "mining"
---

# PlasMAAG

Upstream: [RasmussenLab/PlasMAAG](https://github.com/RasmussenLab/PlasMAAG)

## Citation

Piera Líndez, P. *et al.* Accurate plasmid reconstruction from metagenomics data
using assembly–alignment graphs and contrastive learning. *Nat. Biotechnol.*
(2026). https://doi.org/10.1038/s41587-026-03005-7

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Plasmids are under-recovered by chromosome-oriented binning and by single-sample
circular-path assemblers (fragmentation, entanglement, low coverage). PlasMAAG
builds an **assembly–alignment graph** across samples and bins plasmids +
organisms together with contrastive learning.

```text
multi-sample assemblies / graphs + alignments
  → plasmaag (plasmids + cellular bins)
  → genomad (orthogonal MGE labels)
  → resistome on plasmid bins (rgi) as needed
```

geNomad classifies contigs; PlasMAAG aims to **reconstruct plasmid genomes**.
Use both when plasmid biology is a primary claim.

## How to run

```bash
# follow upstream README — multi-sample inputs required for best performance
```

## Related skills

`genomad` · `basalt` · `vamb` · `rgi` · `microbial-mining` · `tool-selection`
