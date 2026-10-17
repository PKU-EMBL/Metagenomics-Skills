---
name: cge-finders
description: >
  Route Center for Genomic Epidemiology (CGE) Finder-style screens and related isolate
  typing: PlasmidFinder, ResFinder, PointFinder, DisinFinder, VirulenceFinder,
  MobileElementFinder, pMLST, plus staramr / ABRicate wrappers and chromosomal mlst. Use
  for clinical/One-Health isolate typing and plasmid-borne AMR context — not
  community-wide dark-matter discovery. Child skills: plasmidfinder, resfinder,
  pointfinder, disinfinder, virulencefinder, mobileelementfinder, pmlst, staramr,
  abricate, mlst. Complements genomad, mob-suite, rgi, mobileog.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "CGE, Finder, PlasmidFinder, ResFinder, PointFinder, DisinFinder, VirulenceFinder, MobileElementFinder, pMLST, staramr, ABRicate, MLST, AMR, plasmid, MGE"
  metagenomics.stage: "mining"
---

# CGE Finders

CGE **Finder** tools (and close companions) screen draft assemblies against
curated marker databases for plasmids, acquired AMR, chromosomal AMR SNPs,
biocide genes, virulence genes, named MGEs, and sequence types. Best for
**isolates / HQ MAGs** — not a replacement for metagenome-native contig
classifiers (`genomad`) or CARD catalogues (`rgi`).

Web hub: https://www.genomicepidemiology.org/

## Analytical thinking

| Claim | Prefer | Caution |
|-------|--------|---------|
| Replicon / Inc-style plasmid typing | `plasmidfinder` | ≠ complete plasmid MAG |
| Plasmid scheme ST | `pmlst` | Must pick correct scheme |
| Chromosomal PubMLST ST | `mlst` | Not plasmid ST |
| Acquired AMR genes (ResFinder DB) | `resfinder` | ≠ CARD/`rgi` ontology |
| Chromosomal AMR point mutations | `pointfinder` (± `resfinder -c`) | Species-limited panels |
| Disinfectant / biocide genes | `disinfinder` (via ResFinder) | ≠ antibiotic MIC |
| Combined Res + Point + Plasmid | `staramr` | No VF / DisinFinder / pMLST |
| Multi-DB mass screen | `abricate` | No PointFinder phenotype maps |
| Virulence gene markers | `virulencefinder` (± `abricate --db vfdb`) | Narrow species DBs |
| Named IS / Tn / ICE / IME / … | `mobileelementfinder` | Complements `isescan` / `mobileog` |
| Meta plasmid/virus contigs | `genomad` · `plasmaag` | Different task |
| MOB / relaxase typing | `mob-suite` | Complements replicons |
| Broad resistome (CARD) | `rgi` (± `deeparg`) | Keep separate from ResFinder |

Hard rules:

1. Pin **software + database** versions for every Finder / wrapper
2. Prefer assembled contigs for isolate claims; state if using KMA on reads
3. Do not equate Finder hits with phenotype or complete circular plasmids
4. Keep ResFinder / DisinFinder / RGI-CARD tables separate unless cross-mapped
5. Report chromosomal `mlst` ST and plasmid `pmlst` ST as distinct claims

## Decision tree

```text
Isolate / CGE-style screen?
├─ Replicons → plasmidfinder
├─ Plasmid ST → pmlst
├─ Chromosomal ST → mlst
├─ Acquired AMR → resfinder
├─ Chromosomal AMR SNPs → pointfinder
├─ Biocide genes → disinfinder
├─ One report Res+Point+Plasmid → staramr
├─ Multi-DB BLAST screen → abricate
├─ Virulence markers → virulencefinder
├─ Named MGEs → mobileelementfinder
├─ Meta plasmid/virus contigs → genomad (± plasmaag)
├─ MOB / reconstruction → mob-suite
└─ CARD resistome → rgi
```

## Related skills

`plasmidfinder` · `pmlst` · `mlst` · `resfinder` · `pointfinder` ·
`disinfinder` · `virulencefinder` · `mobileelementfinder` · `staramr` ·
`abricate` · `genomad` · `mob-suite` · `plasmaag` · `mobileog` · `isescan` ·
`integronfinder` · `rgi` · `deeparg` · `microbial-mining` · `tool-selection`
