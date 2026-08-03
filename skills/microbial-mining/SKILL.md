---
name: microbial-mining
description: >
  Route microbial / genome mining after assembly or binning: BGCs (antiSMASH,
  BiG-SCAPE), AMR (RGI, DeepARG, ResFinder), mobile elements (geNomad,
  VirSorter2, CheckV, mobileOG-db, ISEScan, IntegronFinder, MOB-suite, CGE
  Finders), antimicrobial peptides (Macrel), element cycling (METABOLIC, MEBS,
  FeGenie), DOM/biosurfactant/HC biodegradation (dbCAN, HADEG, BioSurfDB),
  metabolism (DRAM, gapseq), defense (DefenseFinder, PADLOC), quorum sensing
  (QSAP), and annotation substrates (Bakta/Prokka). Use when the question is
  discovery of functional elements, not community tables alone.
license: MIT
category: orchestration
tags: [genome-mining, BGC, AMR, MGE, virus, metabolism, element-cycling, DOM, biosurfactant, defense, QS, routing]
stage: mining
---

# Microbial mining

Mine assembled contigs and QC-filtered genomes/MAGs for **functional elements**.
Parallel track after assembly/binning — not a replacement for taxonomy tables.

## Analytical thinking

| Claim type | Prefer | Caution |
|------------|--------|---------|
| Natural products / BGCs | `antismash` → `bigscape` | Cluster ≠ characterized compound |
| AMR / resistome | `rgi` (± `deeparg`); isolates also `resfinder` / `staramr` | Hit ≠ expression / phenotype; keep CARD vs ResFinder separate |
| Plasmids / viruses (contig) | `genomad`, `virsorter2`, `checkv`, `vcontact` | CheckV before viral taxonomy |
| MGE protein machinery | `mobileog` | Category hit ≠ complete element |
| Insertion sequences | `isescan` | IS ≠ plasmid |
| Integrons / cassettes | `integronfinder` | Cassette ≠ expressed ARG |
| CGE Finders (+ pMLST / mlst / ABRicate) | `cge-finders` | Best on isolates / HQ MAGs |
| Plasmid MOB / replicon typing | `mob-suite` · `plasmidfinder` | Typing ≠ wet-lab Inc assay |
| Plasmid genome recovery | `plasmaag` | Multi-sample graphs help |
| Antimicrobial peptides | `macrel` | High candidate FDR |
| Element cycling (C/N/S/Fe/P/…) | `element-cycling` → `metabolic` / `mebs` / `fegenie` | Potential ≠ flux |
| DOM / glycans / biosurfactants / HC | `dom-biosurfactant` → `dbcan` / `hadeg` / `biosurfdb` | Hit ≠ assay / rate |
| Distilled metabolism | `dram` | Needs decent completeness |
| CAZymes (glycan DOM) | `dbcan` | Consensus + substrate rules |
| Genome-scale models | `gapseq` (± `vmh` / `alphagem`) | HQ MAGs only |
| Anti-phage defense | `defensefinder` · `padloc` | Annotate proteins first; models differ |
| Quorum sensing / autoinducers | `qsap` | Genes ≠ measured signals |
| De novo conserved clusters | `spacedust` | Complement known-system tools |
| Structure search (AFDB/PDB) | `foldseek` | Via `metagenomics-llm` |
| Annotation substrate | `bakta` / `prokka` | Feed other miners |

## Decision tree

```text
Mining goal?
├─ BGCs → antismash → (many genomes) bigscape
├─ Resistome → rgi (± deeparg); isolates → resfinder / staramr (± pointfinder)
├─ Plasmids / viruses → genomad (± virsorter2) → checkv → vcontact
├─ MGE detail
│   ├─ Protein machinery → mobileog
│   ├─ IS elements → isescan
│   ├─ Integrons → integronfinder
│   ├─ CGE Finders → cge-finders (plasmidfinder · resfinder · abricate · …)
│   └─ Plasmid MOB/replicon typing → mob-suite / plasmidfinder (± pmlst)
├─ Plasmid MAGs → plasmaag (± genomad)
├─ Virulence markers (supported taxa) → virulencefinder / abricate
├─ Named MGEs (CGE library) → mobileelementfinder
├─ Chromosomal / plasmid ST → mlst / pmlst
├─ AMP smORFs → macrel
├─ Element cycling (C, N, S, Fe, P, H₂, CH₄, …) → element-cycling
├─ DOM / biosurfactant / HC biodegradation → dom-biosurfactant
├─ Metabolism distillate → dram (± dbcan)
├─ GEMs → gapseq
├─ Defense systems → bakta/prokka → defensefinder and/or padloc
├─ Quorum sensing → qsap
├─ Dark modules / neighborhoods → spacedust
├─ Structure / motif search → foldseek / folddisco
├─ Vector DB / warehouse search → homology-search
├─ LM remote homology → metagenomics-llm / protein-language-model
└─ Unsure → bakta on HQ MAGs, then branch
```

## Typical order

```text
bins/MAGs (checkm2 / mag-qc / gunc)
   → bakta | prokka
   ├─→ antismash → bigscape
   ├─→ rgi (± deeparg); isolates → cge-finders / staramr
   ├─→ element-cycling → metabolic / mebs / fegenie
   ├─→ dom-biosurfactant → dbcan / hadeg / biosurfdb
   ├─→ dram → dbcan / gapseq
   ├─→ defensefinder / padloc
   └─→ qsap
contigs
   → genomad | virsorter2 → checkv → vcontact
   → mobileog / isescan / integronfinder / mob-suite
   → cge-finders (plasmidfinder · resfinder · virulencefinder · …)
   → plasmaag (multi-sample plasmid recovery)
   → macrel
```

## Never

- Treat antiSMASH regions as proven natural products
- Publish viral genomes without CheckV
- Merge mining hits with HUMAnN abundances unlabeled
- Mine failed/low-quality bins without stating filters
- Claim elemental fluxes from HMM presence alone

## Related skills

`antismash` · `bigscape` · `genomad` · `virsorter2` · `checkv` · `vcontact` ·
`mobileog` · `isescan` · `integronfinder` · `mob-suite` · `plasmaag` ·
`cge-finders` · `plasmidfinder` · `resfinder` · `pointfinder` · `disinfinder` ·
`virulencefinder` · `mobileelementfinder` · `pmlst` · `mlst` · `staramr` ·
`abricate` · `macrel` ·
`element-cycling` · `metabolic` · `mebs` · `fegenie` · `dom-biosurfactant` ·
`hadeg` · `biosurfdb` · `dram` · `dbcan` · `bakta` · `rgi` · `deeparg` ·
`gapseq` · `vmh` · `defensefinder` · `padloc` · `qsap` · `spacedust` ·
`foldseek` · `folddisco` · `homology-search` · `metagenomics-llm` ·
`tool-selection`
