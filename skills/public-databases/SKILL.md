---
name: public-databases
description: >
  Route shotgun metagenomics work to the right public databases and catalogues.
  Use this skill when: (1) Choosing which public resource to download or cite,
  (2) Distinguishing raw-read archives vs genome catalogues vs tool reference DBs,
  (3) Planning reproducible DB pinning for Methods, (4) Comparing UHGG/MGnify,
  GTDB, SRA/ENA, bioBakery, CARD, eggNOG, Kraken, CheckM2.
  For fetching reads use sra-ena. For biome MAG catalogues use mgnify.
  For taxonomy releases use gtdb. For MetaPhlAn/HUMAnN indexes use
  biobakery-databases. For software install, use setup.
license: MIT
category: utilities
tags: [database, catalogue, UHGG, GTDB, MGnify, SRA, ENA, CARD, eggNOG]
---

# Public databases

Metagenomics needs **data archives**, **genome catalogues**, and **tool reference
indexes**. Mixing these layers without labels is a common Methods error.

## Analytical thinking

Ask three questions before downloading anything:

1. **What claim am I supporting?** Community composition ≠ MAG novelty ≠ AMR
   gene presence.
2. **Is this a primary public resource or a tool-bundled index?** GTDB release
   files ≠ `GTDBTK_DATA_PATH` package; UHGG genomes ≠ Kraken UHGG DB.
3. **Which release/version will I pin?** Always record accession + release ID +
   download date/checksum when claims depend on the DB.

## Map by purpose

| Purpose | Prefer | Skill |
|---------|--------|-------|
| Public shotgun reads / study accession | NCBI SRA / EBI ENA | `sra-ena` |
| Analysed microbiome studies + biome MAG catalogues (UHGG, …) | MGnify | `mgnify` |
| Bacterial/archaeal taxonomy + representative genomes | GTDB | `gtdb` (+ `gtdbtk`) |
| Marker taxonomy / pathway indexes | ChocoPhlAn, UniRef, MetaCyc | `biobakery-databases` |
| k-mer classification indexes | Kraken2 Standard / PlusPF / custom | `kraken2` |
| Orthology / function | eggNOG | `eggnog-mapper` |
| AMR reference | CARD | `rgi` |
| MAG completeness models | CheckM2 DB | `checkm2` |
| Host depletion indexes | Bowtie2 host genomes | `kneaddata` |
| BASALT refinement weights | `BASALT_WEIGHT` | `basalt` / `setup` |

## Decision tree

```text
Need public metagenomics data/reference?
│
├─ Download / cite raw reads for a study
│     → sra-ena
├─ Browse analysed studies or biome MAG catalogues (e.g. UHGG)
│     → mgnify
├─ Taxonomy release, species reps, trees for genomes
│     → gtdb  (classify with gtdbtk)
├─ Run MetaPhlAn / HUMAnN
│     → biobakery-databases
├─ Run Kraken2 / Bracken
│     → kraken2 (DB choice is the scientific lever)
├─ Annotate genes / AMR / MAG QC
│     → eggnog-mapper / rgi / checkm2
└─ Unsure
      → this skill + tool-selection
```

## Hard rules

1. Never merge MetaPhlAn, Kraken, and GTDB labels into one unlabeled taxonomy table
2. Never treat MGnify catalogue membership as experimental proof for *your* sample
3. Pin DB versions next to software versions in the provenance bundle
4. Prefer official FTP/API over mirrored unofficial dumps unless checksums match

## Related skills

`sra-ena` · `mgnify` · `gtdb` · `biobakery-databases` · `setup` · `tool-selection` ·
`kraken2` · `metaphlan` · `humann` · `eggnog-mapper` · `rgi` · `gtdbtk` · `checkm2`
