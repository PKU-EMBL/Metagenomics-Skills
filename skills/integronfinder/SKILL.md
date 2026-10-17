---
name: integronfinder
description: >
  IntegronFinder — detect integrons (intI, attC, cassettes) in bacterial
  genomes/assemblies, including AMR cassette context. Use for integron-focused MGE
  mining. Route via microbial-mining; pair with rgi / mobileog / genomad.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "IntegronFinder, integron, MGE, AMR, cassette, genome-mining"
  metagenomics.upstream: "https://github.com/gem-pasteur/Integron_Finder"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.6"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream usage; not executed here"
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

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Integrons capture and express gene cassettes (often AMR). IntegronFinder
locates complete/CALIN/In0-style architectures. Intersect cassette genes with
`rgi` / `deeparg` for resistome context; do not equate integron presence with
expression.

## How to run

```bash
set -euo pipefail
[[ -s genome.fna ]] || exit 2
mkdir -p integron_out
integron_finder genome.fna --outdir integron_out --cpu 4 --func-annot
find integron_out -name '*.summary' -size +0c | grep -q .
find integron_out -name '*.integrons' -size +0c | grep -q .
```

This targets IntegronFinder 2.0.6. Functional annotation requires its compatible NCBIfam-AMRFinder profiles; omit `--func-annot` rather than using mismatched assets. Preserve complete, CALIN and In0 calls separately and validate element coordinates on each contig.

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
