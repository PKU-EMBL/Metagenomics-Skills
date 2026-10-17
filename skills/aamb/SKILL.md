---
name: aamb
description: >
  AAMB / AVAMB — adversarial autoencoder metagenomic binning and its ensemble with VAMB
  for improved near-complete MAG recovery. Use when: (1) Running AAMB as a DL single
  binner, (2) AVAMB ensemble (VAMB+AAMB) for extra NC genomes, (3) Diversifying bins
  before DAS Tool/BASALT. Still QC with checkm2; prefer basalt ★ for multi-assembly
  catalogues.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, AAMB, AVAMB, VAMB, deep-learning"
  metagenomics.upstream: "https://github.com/RasmussenLab/vamb"
  metagenomics.stage: "binning"
---

# AAMB / AVAMB

Upstream: [RasmussenLab/vamb](https://github.com/RasmussenLab/vamb) (AAMB/AVAMB
paths documented in the VAMB repository)

## Citation

Piera Líndez, P. *et al.* Adversarial and variational autoencoders improve
metagenomic binning. *Commun. Biol.* **6**, 1073 (2023).
https://doi.org/10.1038/s42003-023-05452-3

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

AAMB uses **adversarial autoencoders** on coabundance + TNF; AVAMB ensembles
AAMB with VAMB and recovered substantially more near-complete genomes in the
paper vs VAMB alone. Treat as a **diverse DL binner** for ensembles — not a
replacement for `basalt` multi-assembly refinement.

Related VAMB-family tools: `vamb`, `taxvamb`.

## How to run

```bash
# see VAMB docs for aamb / avamb entry points for your installed version
# typical: provide contigs + BAM abundance as with VAMB
```

## Related skills

`vamb` · `taxvamb` · `semibin2` · `dastool` · `basalt` · `tool-selection`
