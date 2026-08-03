---
name: integronfinder
description: >
  IntegronFinder — detect integrons (intI, attC, cassettes) in bacterial
  genomes/assemblies, including AMR cassette context. Use for integron-focused
  MGE mining. Upstream: https://github.com/gem-pasteur/Integron_Finder.
  Route via microbial-mining; pair with rgi / mobileog / genomad.
license: MIT
category: analysis-tools
tags: [IntegronFinder, integron, MGE, AMR, cassette, genome-mining]
upstream: https://github.com/gem-pasteur/Integron_Finder
stage: mining
---

# IntegronFinder

Upstream: [gem-pasteur/Integron_Finder](https://github.com/gem-pasteur/Integron_Finder)

## Citation

Néron, B. *et al.* IntegronFinder 2.0: Identification and Analysis of Integrons
across Bacteria, with a Focus on Antibiotic Resistance in Klebsiella.
*Microorganisms* **10**, 700 (2022).
https://doi.org/10.3390/microorganisms10040700

Original: Cury, J. *et al.* Identification and analysis of integrons and cassette
arrays in bacterial genomes. *Nucleic Acids Res.* **44**, 4539–4550 (2016).
https://doi.org/10.1093/nar/gkw319

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Integrons capture and express gene cassettes (often AMR). IntegronFinder
locates complete/CALIN/In0-style architectures. Intersect cassette genes with
`rgi` / `deeparg` for resistome context; do not equate integron presence with
expression.

## How to run

```bash
# bioconda / pip per upstream; example
integron_finder genome.fna --outdir integron_out
# optional functional annotation flags — follow IntegronFinder 2 docs
```

## Decision tree

```text
Integrons / cassettes?
├─ Yes → integronfinder
├─ IS elements → isescan
├─ MGE protein machinery → mobileog
├─ Plasmid/virus contigs → genomad
└─ ARG catalogue → rgi (± deeparg)
```

## Related skills

`rgi` · `deeparg` · `mobileog` · `isescan` · `genomad` · `microbial-mining` ·
`tool-selection`
