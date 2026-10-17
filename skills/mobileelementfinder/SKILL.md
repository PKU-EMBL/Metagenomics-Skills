---
name: mobileelementfinder
description: >
  MobileElementFinder — CGE detection of named mobile genetic elements (MITEs, IS, Tn,
  ComTn, ICE, IME, CIME, …) in assembled bacterial genomes, with optional ARG/virulence
  context. Use for isolate mobilome screens. Upstream: PyPI MobileElementFinder / CGE
  web service. Route via cge-finders / microbial-mining; complement isescan, mobileog,
  integronfinder, genomad.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MobileElementFinder, CGE, MGE, IS, transposon, ICE, IME, mobilome"
  metagenomics.upstream: "https://pypi.org/project/MobileElementFinder/"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.upstream-version: "1.1.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "mefinder CLI reviewed against upstream source; not executed here"
---

# MobileElementFinder

Upstream: [MobileElementFinder (PyPI)](https://pypi.org/project/MobileElementFinder/) ·
CGE service historically at genomicepidemiology.org · DB shipped with the tool

## Citation

Johansson, M. H. K. *et al.* Detection of mobile genetic elements associated
with antibiotic resistance in *Salmonella enterica* using a newly developed web
tool: MobileElementFinder. *J. Antimicrob. Chemother.* **76**, 101–109 (2021).
https://doi.org/10.1093/jac/dkaa390

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

MobileElementFinder aligns assemblies to a curated library of **named** MGEs
and can flag putative composite transposons. Complements:

| Tool | Role |
|------|------|
| `isescan` | Broad IS HMM/annotation scan |
| `mobileog` | MGE life-cycle protein families |
| `integronfinder` | Integron architectures |
| `genomad` | Plasmid/virus contig scores (meta) |
| `plasmidfinder` | Replicon typing |

Hit ≠ proven mobilization event. Short-read assemblies under-resolve large ICE/IME.

## How to run

```bash
set -euo pipefail
[[ -s assembly.fasta ]] || exit 2
mkdir -p result/mefinder temp/mefinder
mefinder --version
mefinder find --contig assembly.fasta --threads 8 --json --gff \
  --temp-dir temp/mefinder result/mefinder/sample
test -s result/mefinder/sample.csv
test -s result/mefinder/sample.json
test -s result/mefinder/sample.gff
```

This targets MobileElementFinder 1.1.2's `mefinder find` entry point. Pin package and bundled MGEdb versions/checksums; reconcile all hits to input contig coordinates and retain explicit no-hit output.

## Decision tree

```text
Named MGE screen?
├─ CGE MGE library → mobileelementfinder
├─ IS-focused scan → isescan
├─ MGE protein machinery → mobileog
├─ Integrons → integronfinder
├─ Plasmid/virus contigs → genomad
└─ Replicons → plasmidfinder / mob-suite
```

## Related skills

`cge-finders` · `isescan` · `mobileog` · `integronfinder` · `plasmidfinder` ·
`genomad` · `resfinder` · `virulencefinder` · `microbial-mining` ·
`tool-selection`
