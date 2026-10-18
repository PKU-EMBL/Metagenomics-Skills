---
name: microbial-mining
description: >
  Route microbial / genome mining after assembly or binning: BGCs (antiSMASH,
  BiG-SCAPE), resistomes and ARG context, mobile elements and plasmid systems,
  ARG–MGE–host linkage, viruses (geNomad, VirSorter2, CheckV), antimicrobial
  peptides (Macrel), element cycling (METABOLIC, MEBS, FeGenie), DOM/biosurfactant/HC
  biodegradation (dbCAN, HADEG, BioSurfDB), metabolism (DRAM, gapseq), defense
  (DefenseFinder, PADLOC), quorum sensing (QSAP), and annotation substrates
  (Bakta/Prokka). Use when the question is discovery of functional elements, not
  community tables alone.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "genome-mining, BGC, AMR, MGE, virus, metabolism, element-cycling, DOM, biosurfactant, defense, QS, routing"
  metagenomics.stage: "mining"
---

# Microbial mining

Mine assembled contigs and QC-filtered genomes/MAGs for **functional elements**.
Parallel track after assembly/binning — not a replacement for taxonomy tables.

## Analytical thinking

| Claim type | Prefer | Caution |
|------------|--------|---------|
| Natural products / BGCs | `antismash` → `bigscape` | Cluster ≠ characterized compound |
| AMR / resistome | `resistome-analysis` → `rgi` / `amrfinderplus` / `args-oap` / `deeparg` / `pathofact`; isolates also `resfinder` / `staramr` | Detection, abundance, phenotype, mobility and host are separate layers |
| ARG–MGE–host evidence | `arg-mge-host-linkage` | Co-occurrence ≠ physical linkage; host link ≠ transfer |
| Mobilome / plasmid systems | `mobilome-analysis` → `genomad` / `plasx` / `mobmess` / `mob-suite` | Plasmid-like ≠ complete or conjugative |
| HGT candidates | `horizontal-gene-transfer` → `metachip` / `waafle` / `hgtector` / `gubbins` | Historical candidate ≠ observed transfer |
| Viral contigs, vOTUs, taxonomy, hosts | `virome-analysis` → `genomad`/`virsorter2`/`vibrant` → `checkv` → `votu-workflow` → `vcontact`/`iphop`/`spacepharer` | Quality and host links remain computational evidence |
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
| Genome/community metabolic models | `community-metabolic-modeling` → `carveme`/`gapseq`/`micom` (± `vmh`/`alphagem`) | Gap filling and flux are assumption-dependent |
| Anti-phage defense | `defensefinder` · `padloc` | Annotate proteins first; models differ |
| Quorum sensing / autoinducers | `qsap` | Genes ≠ measured signals |
| De novo conserved clusters | `spacedust` | Complement known-system tools |
| Structure search (AFDB/PDB) | `foldseek` | Via `metagenomics-llm` |
| Annotation substrate | `bakta` / `prokka` | Feed other miners |

## Decision tree

```text
Mining goal?
├─ BGCs → antismash → (many genomes) bigscape
├─ Resistome → resistome-analysis → rgi / amrfinderplus / args-oap / deeparg / pathofact
├─ ARG–MGE–host linkage → arg-mge-host-linkage → coordinate/long-read/Hi-C/CRISPR gates
├─ HGT → horizontal-gene-transfer → metachip / waafle / hgtector / gubbins
├─ Viruses → virome-analysis → genomad/virsorter2/vibrant → checkv → votu-workflow → vcontact/iphop/spacepharer
├─ Plasmids → mobilome-analysis → genomad / plasx → mobmess / mob-suite / plasmidfinder / plasmaag
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
├─ GEMs/community simulation → community-metabolic-modeling → carveme/gapseq/micom
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
   ├─→ resistome-analysis → rgi / amrfinderplus / deeparg / pathofact
   ├─→ element-cycling → metabolic / mebs / fegenie
   ├─→ dom-biosurfactant → dbcan / hadeg / biosurfdb
   ├─→ dram → dbcan / gapseq
   ├─→ defensefinder / padloc
   └─→ qsap
contigs
   → virome-analysis → genomad | virsorter2 | vibrant → checkv → votu-workflow → vcontact / iphop / spacepharer
   → mobilome-analysis → genomad / plasx / mobmess / mob-suite
   → arg-mge-host-linkage → metator / hicbin / viralcc / spacepharer
   → horizontal-gene-transfer → metachip / waafle / hgtector
   → mobileog / isescan / integronfinder
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

`antismash` · `bigscape` · `resistome-analysis` · `mobilome-analysis` ·
`arg-mge-host-linkage` · `horizontal-gene-transfer` · `transfer-network-analysis` ·
`amrfinderplus` · `args-oap` · `pathofact` · `plasx` · `mobmess` · `metachip` ·
`waafle` · `hgtector` · `metator` · `hicbin` · `viralcc` · `spacepharer` ·
`virome-analysis` · `votu-workflow` · `genomad` ·
`virsorter2` · `vibrant` · `checkv` · `vcontact` · `iphop` ·
`mobileog` · `isescan` · `integronfinder` · `mob-suite` · `plasmaag` ·
`cge-finders` · `plasmidfinder` · `resfinder` · `pointfinder` · `disinfinder` ·
`virulencefinder` · `mobileelementfinder` · `pmlst` · `mlst` · `staramr` ·
`abricate` · `macrel` ·
`element-cycling` · `metabolic` · `mebs` · `fegenie` · `dom-biosurfactant` ·
`hadeg` · `biosurfdb` · `dram` · `dbcan` · `bakta` · `rgi` · `deeparg` ·
`community-metabolic-modeling` · `carveme` · `gapseq` · `micom` · `vmh` ·
`defensefinder` · `padloc` · `qsap` · `spacedust` ·
`foldseek` · `folddisco` · `homology-search` · `metagenomics-llm` ·
`tool-selection`
