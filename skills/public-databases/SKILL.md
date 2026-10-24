---
name: public-databases
description: >
  Route shotgun metagenomics work to the right public databases, catalogues, and
  benchmark datasets. Use when: (1) Choosing SRA/ENA vs MGnify vs GTDB vs proGenomes vs
  CAMI, (2) Distinguishing raw archives, genome warehouses, biome catalogues, tool
  indexes, and gold-standard benchmarks, (3) Pinning data releases for Methods, (4)
  Planning downloads for UHGG, current GTDB releases, KEGG, CARD, bioBakery, Kraken, CheckM2. Child
  skills: sra-ena, mgnify, gtdb, progenomes, cami, kegg, biobakery-databases. For
  software install use setup.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, catalogue, UHGG, GTDB, MGnify, CAMI, proGenomes, SRA, ENA, KEGG"
  metagenomics.stage: "utilities"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "resource routing and provenance requirements reviewed; downloads are delegated to child skills"
---

# Public databases

Metagenomics “data” is not one thing. Separate these **layers** in Methods and
in your disk layout:

| Layer | Examples | Skills |
|-------|----------|--------|
| Raw / submitted reads | NCBI SRA, EBI ENA | `sra-ena` |
| Analysed studies + biome MAG/protein catalogues | MGnify, UHGG | `mgnify` |
| Rank-normalized taxonomy + species reps | GTDB (for example R11-RS232) | `gtdb` · `gtdbtk` |
| Uniformly annotated genome warehouse | proGenomes4 | `progenomes` |
| Gold-standard benchmarks / simulators | CAMI / CAMI II, CAMISIM | `cami` |
| Pathway / ortholog knowledge bases | KEGG, eggNOG, MetaCyc | `kegg` · `eggnog-mapper` · `biobakery-databases` |
| Tool runtime indexes | Kraken, CheckM2, ChocoPhlAn, CARD | tool skills |
| Genome language model corpora / checkpoints | OMG, OpenGenome2, gLM2 / NT / DNABERT-2 / Caduceus / Evo | `genome-language-model` · `omg` · `evo2` |
| Protein language model checkpoints | ESM-2, ESM C, SaProt, ProstT5 / ProtT5, PLMSearch | `protein-language-model` · `esm` · `esmc` · `saprot` |
| Structure search indexes | AFDB, PDB, ESM Atlas (via Foldseek/Folddisco) | `foldseek` · `folddisco` · `metagenomics-llm` |
| Vector / embedding homology DBs | ERAST public vector DB | `erast` · `homology-search` |
| Phylogeny-compressed genome search sets | 661k / MOF collections | `phylign` · `homology-search` |

## Analytical thinking

Ask before downloading:

1. **Claim type?** Reanalysis of public runs ≠ MAG novelty vs UHGG ≠ CAMI tool
   ranking ≠ KO pathway reconstruction.
2. **Primary resource vs tool-bundled index?** GTDB release files ≠
   `GTDBTK_DATA_PATH`; UHGG genomes ≠ a Kraken UHGG DB; KEGG website ≠ a
   redistributable local dump.
3. **Which release?** Pin accession / catalogue version / GTDB release /
   CAMI dataset DOI + download date (+ checksum).

## Map by purpose

| Purpose | Prefer | Skill |
|---------|--------|-------|
| Public shotgun reads | SRA / ENA | `sra-ena` |
| Analysed studies + biome MAG catalogues (UHGG, …) | MGnify | `mgnify` |
| Bacterial/archaeal taxonomy release | GTDB | `gtdb` (+ `gtdbtk`) |
| ~2M QC'd annotated prokaryotic genomes | proGenomes4 | `progenomes` |
| Benchmark with gold standards | CAMI / CAMI II | `cami` |
| Marker taxonomy / pathway indexes | ChocoPhlAn, UniRef, MetaCyc | `biobakery-databases` |
| KO / KEGG pathways (licensed access) | KEGG | `kegg` |
| Human/gut metabolic knowledge | VMH | `vmh` |
| k-mer classification indexes | Kraken2 Standard / custom | `kraken2` |
| Orthology (eggNOG) | eggNOG | `eggnog-mapper` |
| AMR reference | CARD | `rgi` |
| MAG completeness models | CheckM2 DB | `checkm2` |
| Host depletion indexes | Bowtie2 host genomes | `kneaddata` |
| BASALT refinement weights | `BASALT_WEIGHT` | `basalt` / `setup` |

## Decision tree

```text
Need public metagenomics data/reference?
│
├─ Raw FASTQ for a study / BioProject
│     → sra-ena
├─ Analysed MGnify study or biome MAG/protein catalogue (UHGG, …)
│     → mgnify
├─ GTDB taxonomy tables / reps / classify my MAGs
│     → gtdb / gtdbtk
├─ Large consistently annotated genome set / pan-genomes
│     → progenomes
├─ Gold-standard benchmark or simulator
│     → cami
├─ MetaPhlAn / HUMAnN indexes
│     → biobakery-databases
├─ KEGG KO / pathways (check license)
│     → kegg
├─ Kraken2 / Bracken indexes
│     → kraken2
├─ eggNOG / CARD / CheckM2
│     → eggnog-mapper / rgi / checkm2
├─ Genome language model corpus / gLM2
│     → omg / genome-language-model
├─ Protein language model checkpoints (ESM / ESMC / SaProt / ProstT5)
│     → protein-language-model / esm / esmc / saprot / prostt5
└─ Unsure
      → this skill + tool-selection
```

## Acquisition and acceptance contract

Before transfer, record license/access terms, expected bytes/files, destination,
available space, official URL/API, release identifier, published checksums, and
whether credentials or controlled-access handling apply. Download into a staging
area, verify size/checksum/archive integrity, inventory records, then atomically
promote to a read-only release directory. Never update an index in place during
an analysis.

For a derived tool index, retain both the primary-resource manifest and the
exact build command/software version. Acceptance requires a representative query
or tool-specific integrity check; a completed transfer alone is not validation.

## Provenance checklist (pin in Methods)

- Resource name + **release / catalogue version / dataset ID**
- Download URL or DOI + **date** (+ checksum)
- Any filters (completeness, biome, habitat, ANI)
- Whether you used primary files vs a **tool index** built from them

## Hard rules

1. Never merge MetaPhlAn, Kraken, GTDB, and MGnify labels into one unlabeled table
2. MGnify/UHGG membership ≠ detection in *your* sample without abundance evidence
3. CAMI rankings ≠ production defaults for every biome
4. Prefer official FTP/API; verify mirrors with checksums
5. Respect KEGG and other license-restricted resources

## Related skills

`sra-ena` · `mgnify` · `gtdb` · `progenomes` · `cami` · `kegg` ·
`biobakery-databases` · `omg` · `genome-language-model` ·
`protein-language-model` · `metagenomics-llm` · `setup` · `tool-selection` ·
`kraken2` · `metaphlan` · `humann` · `eggnog-mapper` · `rgi` · `gtdbtk` ·
`checkm2`
