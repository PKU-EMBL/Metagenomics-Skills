---
name: cge-finders
description: >
  Route Center for Genomic Epidemiology (CGE) Finder-style screens on bacterial
  assemblies/isolates: PlasmidFinder, ResFinder, PointFinder, VirulenceFinder,
  MobileElementFinder, plus staramr for combined Res/Point/Plasmid DB scans.
  Use for clinical/One-Health isolate typing and plasmid-borne AMR context —
  not community-wide dark-matter discovery. Child skills: plasmidfinder,
  resfinder, pointfinder, virulencefinder, mobileelementfinder, staramr.
  Complements genomad, mob-suite, rgi, mobileog. Route via microbial-mining.
license: MIT
category: orchestration
tags: [CGE, Finder, PlasmidFinder, ResFinder, PointFinder, VirulenceFinder, MobileElementFinder, staramr, AMR, plasmid, MGE]
stage: mining
---

# CGE Finders

CGE **Finder** tools screen draft assemblies (or reads via KMA) against curated
marker databases for plasmids, acquired AMR, chromosomal AMR SNPs, virulence
genes, and named MGEs. Best for **isolates / HQ MAGs** with known taxa — not a
replacement for metagenome-native contig classifiers (`genomad`) or CARD
catalogues (`rgi`).

Web hub: https://www.genomicepidemiology.org/

## Analytical thinking

| Claim | Prefer | Caution |
|-------|--------|---------|
| Replicon / Inc-style plasmid typing (CGE DB) | `plasmidfinder` | DB bias to Enterobacterales / Gram+ sets; ≠ full plasmid MAG |
| Acquired AMR genes (ResFinder DB) | `resfinder` | Genotype ≠ MIC; different ontology from CARD/`rgi` |
| Chromosomal AMR point mutations | `pointfinder` (± `resfinder -c`) | Species-limited panels |
| Combined Res + Point + Plasmid reports | `staramr` | Convenience wrapper; pin DB versions |
| Virulence gene markers | `virulencefinder` | Species DB coverage is narrow |
| Named IS / Tn / ICE / IME / … | `mobileelementfinder` | Complements `isescan` / `mobileog` |
| Plasmid contig discovery (meta) | `genomad` · `plasmaag` | Different task from replicon typing |
| MOB / relaxase typing | `mob-suite` | Complements PlasmidFinder replicons |
| Broad resistome (CARD) | `rgi` (± `deeparg`) | Do not merge unlabeled with ResFinder |

Hard rules:

1. Pin **software + database** versions for every Finder
2. Prefer assembled contigs for isolate claims; state if using KMA on reads
3. Do not equate Finder hits with phenotype or complete circular plasmids
4. Keep ResFinder and RGI/CARD tables separate unless explicitly cross-mapped

## Decision tree

```text
CGE / isolate Finder screen?
├─ Replicons (PlasmidFinder DB) → plasmidfinder
├─ Acquired AMR genes → resfinder
├─ Chromosomal AMR SNPs → pointfinder (or resfinder with PointFinder DB)
├─ One report: Res+Point+Plasmid → staramr
├─ Virulence markers → virulencefinder
├─ Named MGEs (IS/Tn/ICE/…) → mobileelementfinder
├─ Meta plasmid/virus contigs → genomad (± plasmaag)
├─ MOB/replicon reconstruction → mob-suite
└─ CARD resistome → rgi
```

## Related skills

`plasmidfinder` · `resfinder` · `pointfinder` · `virulencefinder` ·
`mobileelementfinder` · `staramr` · `genomad` · `mob-suite` · `plasmaag` ·
`mobileog` · `isescan` · `integronfinder` · `rgi` · `deeparg` ·
`microbial-mining` · `tool-selection`
