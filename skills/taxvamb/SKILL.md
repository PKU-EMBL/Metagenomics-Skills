---
name: taxvamb
description: >
  TaxVAMB — semisupervised bimodal VAE binning that integrates TNF,
  coabundance, and contig taxonomy for improved MAG recovery (incl. incomplete
  genomes and long-read sets). Use when: (1) Taxonomy-informed binning,
  (2) Comparing to VAMB/AAMB/SemiBin2, (3) Single-sample setups needing more
  HQ bins. Upstream: https://github.com/RasmussenLab/vamb. Taxonomy labels are
  an input feature — garbage taxonomy in, garbage bins out.
license: MIT
category: analysis-tools
tags: [binning, TaxVAMB, VAMB, taxonomy, deep-learning]
upstream: https://github.com/RasmussenLab/vamb
stage: binning
---

# TaxVAMB

Upstream: [RasmussenLab/vamb](https://github.com/RasmussenLab/vamb)

## Citation

Kutuzova, S. *et al.* Improving metagenome binning by integrating intrinsic
features and taxonomy. *Nat. Biotechnol.* (2026).
https://doi.org/10.1038/s41587-026-03098-0

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

TaxVAMB adds **contig-level taxonomy** into a VAMB-style VAE. Strong reported
gains on CAMI2 human sets and long-read data, and on incomplete genomes — but
performance inherits taxonomy DB bias. Prefer high-quality taxonomic inputs;
do not circularly claim novelty from taxonomy-informed bins without independent
QC (`checkm2`, `gunc`, `gtdbtk`).

## How to run

```bash
# taxonomy table + contigs + abundances — follow TaxVAMB section of VAMB docs
```

## Related skills

`vamb` · `aamb` · `metabuli` · `mmseqs2` · `basalt` · `checkm2` · `tool-selection`
