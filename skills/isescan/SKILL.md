---
name: isescan
description: >
  ISEScan — automated annotation of insertion sequence (IS) elements in prokaryotic
  genomes via profile HMMs. Use for IS family catalogues on MAGs or contigs as part of
  MGE refinement beyond geNomad. Route via microbial-mining; pair with mobileog /
  integronfinder.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ISEScan, IS, insertion-sequence, MGE, genome-mining"
  metagenomics.upstream: "https://github.com/xiezhq/ISEScan"
  metagenomics.stage: "mining"
---

# ISEScan

Upstream: [xiezhq/ISEScan](https://github.com/xiezhq/ISEScan)

## Citation

Xie, Z. & Tang, H. ISEScan: automated identification of insertion sequence
elements in prokaryotic genomes. *Bioinformatics* **33**, 3340–3347 (2017).
https://doi.org/10.1093/bioinformatics/btx433

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

IS elements drive rearrangements and can flank ARGs/BGCs. ISEScan reports IS
families/copies; it does **not** replace plasmid/virus classifiers (`genomad`)
or integron detection (`integronfinder`).

## How to run

```bash
# install per upstream; typical pattern
isescan.py genome.fna output_dir
# pin ISEScan + HMM library versions
```

## Decision tree

```text
Need IS annotation?
├─ Yes → isescan
├─ Broader MGE proteins → mobileog
├─ Integrons → integronfinder
└─ Plasmid/virus contigs → genomad
```

## Related skills

`mobileog` · `integronfinder` · `genomad` · `rgi` · `microbial-mining` ·
`tool-selection`
