---
name: padloc
description: >
  PADLOC (Prokaryotic Antiviral Defence LOCator) — HMM + synteny detection of antiviral
  defence systems (CRISPR-Cas and many other systems) in prokaryotic genomes. Use as a
  complement or alternative to DefenseFinder for defenseome surveys. Route via
  microbial-mining; pair with genomad/virsorter2 for MGE context.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PADLOC, defense, defenseome, CRISPR, antiviral, genome-mining"
  metagenomics.upstream: "https://github.com/padlocbio/padloc"
  metagenomics.stage: "mining"
---

# PADLOC

Upstream: [padlocbio/padloc](https://github.com/padlocbio/padloc) ·
DB: [padloc-db](https://github.com/padlocbio/padloc-db) ·
Web: https://padloc.otago.ac.nz/padloc/

## Citation

Payne, L. J. *et al.* Identification and classification of antiviral defence
systems in bacteria and archaea with PADLOC reveals new system types.
*Nucleic Acids Res.* **49**, 10868–10878 (2021).
https://doi.org/10.1093/nar/gkab883

Web server: Payne, L. J. *et al.* PADLOC: a web server for the identification
of antiviral defence systems in microbial genomes. *Nucleic Acids Res.* **50**,
W541–W550 (2022). https://doi.org/10.1093/nar/gkac400

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

PADLOC finds defence systems via **HMM homology + system architecture/synteny**.
Complements `defensefinder` (different model sets / system coverage). For dark
neighborhood discovery without known system models use `spacedust`.

| vs | Prefer PADLOC when |
|----|---------------------|
| `defensefinder` | PADLOC-DB models / web precomputes; cross-check both for surveys |
| `spacedust` | Known antiviral system types vs de novo clusters |
| `genomad` | Host defenseome vs MGE/virus contigs |

Annotate proteins first (`bakta` / `prokka`). Pin **padloc-db** version.

## How to run

```bash
# install padloc + download padloc-db per upstream README
padloc --fna genome.fna --outdir padloc_out
# or: padloc --faa proteins.faa --gff features.gff --outdir padloc_out
```

## Decision tree

```text
Defenseome / antiviral systems?
├─ PADLOC models → padloc
├─ DefenseFinder models → defensefinder
├─ Prefer both for Methods robustness → padloc + defensefinder
├─ Dark conserved neighborhoods → spacedust
└─ Virus/plasmid contigs → genomad → checkv
```

## Related skills

`defensefinder` · `spacedust` · `genomad` · `virsorter2` · `bakta` ·
`microbial-mining` · `tool-selection`
