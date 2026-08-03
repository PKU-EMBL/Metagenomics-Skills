## [1.16.0] - 2026-08-03

### Added
- Element cycling layer: `element-cycling` hub, `metabolic` (METABOLIC),
  `mebs`, `fegenie` (C/N/S/Fe/P/H₂/CH₄/…)
- Defenseome: `padloc` (with DefenseFinder)
- MGE refinement: `mobileog`, `isescan`, `integronfinder`, `mob-suite`
- Quorum sensing: `qsap`
- References 107–114

### Changed
- Expanded `microbial-mining` / `tool-selection` routing
- Skills catalog total: 137; package version 1.16.0

## [1.15.0] - 2026-08-03

### Added
- `esmc` (ESM C / Cambrian) and `saprot` (Westlake SaProt) protein LM skills
- References 105–106

### Changed
- Skills catalog total: 127; package version 1.15.0

## [1.14.0] - 2026-08-03

### Added
- Protein language model layer: `protein-language-model` hub, `esm` (ESM-2),
  `prostt5` (ProstT5 / ProtT5)
- References 102–104

### Changed
- Routed `plmsearch` / `deepblast` / LucaPhylo via `protein-language-model`
- Skills catalog total: 125; package version 1.14.0

## [1.13.0] - 2026-08-03

### Added
- `dnabert2`, `caduceus` genome language model skills
- References 100–101

### Changed
- Renamed hub `genomic-lm` → `genome-language-model` (display: Genome language model)
- Skills catalog total: 122; package version 1.13.0

## [1.12.0] - 2026-08-03

### Added
- Genome language model layer: `genome-language-model` hub,
  `nucleotide-transformer` (NT/NTv3), `evo2`
- Deepened `omg`/gLM2 notes; references 96–99

### Changed
- Skills catalog total: 120; package version 1.12.0

## [1.11.1] - 2026-08-03

### Removed
- `colabfold` skill (deferred; use AFDB / Foldseek+ProstT5 paths instead)

### Changed
- Skills catalog total: 117; package version 1.11.1

## [1.11.0] - 2026-08-03

### Added
- Extended Steinegger/Söding search stack: `hh-suite`, `colabfold`, `plass`,
  `metaeuk`, `foldcomp`, `foldmason`, `petasearch`, `unicore`
- Expanded `homology-search` / `phylogenomics` routing

### Changed
- Skills catalog total: 118; package version 1.11.0

## [1.10.0] - 2026-08-03

### Added
- Homology-search layer: `homology-search` hub, `erast` (vector DB), `phylign`
  (phylogenetic compression / MiniPhy+Phylign)
- Phylogenomics layer: `phylogenomics` hub, `iqtree`, `fasttree`, `phylophlan`,
  `lucaphylo`
- References 84–89

### Changed
- Wired search/tree routing into tool-selection, workflow, mining, LLM hub, docs
- Skills catalog total: 110; package version 1.10.0

## [1.9.0] - 2026-08-03

### Added
- Steinegger structure-search layer: `foldseek` (3Di search, Multimer, ProstT5,
  clustering), `folddisco` (structural motifs)
- References 80–83 (Foldseek, Foldseek-Multimer, Folddisco, AFDB clustering)

### Changed
- Expanded `metagenomics-llm` routing (sequence → fold → multimer → motif)
- Deepened `mmseqs2` as sequence counterpart; cross-links in mining/tool-selection
- Skills catalog total: 102; package version 1.9.0

## [1.8.0] - 2026-08-03

### Added
- AI / language-model layer: `metagenomics-llm`, `omg` (OMG+gLM2), `plmsearch`,
  `deepblast` (TM-Vec), `spacedust`, `alphagem`
- Docs/routing hooks in public-databases, tool-selection, microbial-mining, README
- References 74–79

### Changed
- Skills catalog total: 100; package version 1.8.0

## [1.7.0] - 2026-08-03

### Changed
- Quality/consistency pass: synced pipeline, workflow, tool-selection, README,
  getting-started, and troubleshooting with the full skill set
- Removed misleading ensemble-binning Decision notes from non-binning skills
- Deepened high-traffic skills: kaiju, maxbin2, prokka, bakta, eggnog-mapper,
  rgi, mmseqs2, quast, salmon, mag-qc
- Cross-linked SingleM/Bin Chicken, vConTACT/CheckV, Deepurify/Anvi'o, ANI tools

### Fixed
- Duplicate Related skills headers introduced during cleanup

## [1.6.0] - 2026-08-03

### Added
- Priority skills: `anvio`, `singlem`, `vcontact`, `deepurify`, `fastani`
- Secondary skills: `vmh`, `insilicoseq`, `plasmaag`, `aamb`, `taxvamb`, `metabinner`, `lexicmap`
- skani↔FastANI comparison; mining/tool-selection/public-data routes updated
- References 61–73

### Changed
- Skills catalog total: 94; package version 1.6.0

## [1.5.0] - 2026-08-03

### Added
- Data-layer skills: `cami` (CAMI/CAMI II + CAMISIM/AMBER/OPAL), `progenomes`, `kegg`
- Expanded `public-databases` hub and `docs/public-databases.md` (four data layers)
- GTDB release 10 notes; richer MGnify catalogue guidance
- References 51–60 (CAMI stack, GTDB R10, proGenomes4, KEGG, profiler abundance types)

### Changed
- Skills catalog total: 82; package version 1.5.0

## [1.4.0] - 2026-08-03

### Added
- New skills from curated literature: `lorbin`, `comebin`, `binchicken`, `metabuli`
- Literature-grounded expansions for ensemble binning, QC, taxonomy, coverage,
  strain, and viral QC skills (BASALT, MetaWRAP, DAS Tool, SemiBin2, VAMB,
  CoverM, CheckM2, GUNC, MetaPhlAn, Kraken2/Bracken, mOTUs, sylph, inStrain,
  CheckV, CONCOCT, GTDB-Tk, DIAMOND)
- Study-design notes on multi-coverage binning and targeted coassembly
- References 39–50 in `docs/references.md`

### Changed
- Tool-selection routes updated for long-read binning, Metabuli, Bin Chicken
- Skills catalog total: 79

## [1.3.1] - 2026-08-03

### Added
- Deepened mapping skills: `bowtie2`, `strobealign`, `bwa-mem2`, `samtools`
- Deepened mining/binning: `antismash`, `genomad`, `dram`, `metabat2`
- New skills: `racon`, `pilon`, `skani`, `dbcan`, `bigscape`
- Expanded troubleshooting and compute-setup by stage

### Changed
- Tool-selection / pipeline / references updated for polish, ANI, CAZyme, BGC networks

# Changelog

## [1.3.0] - 2026-08-03

### Added
- Mapping-stage tools (Bowtie2, BWA, BWA-MEM2, Minimap2, strobealign, Samtools, …)
- Single binners (MetaBAT2, MaxBin2, CONCOCT, SemiBin2, VAMB) and long-read assemblers
- Microbial mining skills: `microbial-mining`, `antismash`, `genomad`, `virsorter2`,
  `checkv`, `macrel`, `dram`, `bakta`, `deeparg`, `gapseq`, `defensefinder`
- Nature-style `docs/references.md` entries for mapping and mining papers

### Changed
- Pipeline framed as QC → assembly → mapping → binning → taxonomy → function → mining
- Removed third-party list branding from skill/docs surfaces

## [1.2.0] - 2026-08-03

### Added
- Public database skills: `public-databases`, `sra-ena`, `mgnify`, `gtdb`,
  `biobakery-databases`
- Ensemble binning peer skill: `dastool`
- Docs: `docs/public-databases.md`

### Changed
- Reframed the package around five stages: **QC → assembly → binning →
  taxonomic annotation → functional annotation** (bins/MAGs are binning
  outcomes, not the sole pipeline axis)
- Positioned `basalt`, `metawrap`, and `dastool` as an ensemble binning family
  with **BASALT recommended**
- Updated catalogs, workflow, README, SVG, and manifests (30 skills)

## [1.1.0] - 2026-08-03

### Added
- Per-software analysis skills with upstream GitHub links and analytical-thinking sections:
  `fastp`, `kneaddata`, `metaphlan`, `humann`, `kraken2`, `megahit`, `metaspades`,
  `prodigal`, `cd-hit`, `salmon`, `eggnog-mapper`, `rgi`, `metawrap`, `drep`,
  `coverm`, `gtdbtk`, `checkm2` (plus existing `basalt`)
- Expanded `basalt` skill against the official BASALT guide CLI

### Changed
- Replaced composite stage skills (`preprocessing`, `read-based`, `gene-catalogue`,
  `mag-classical`) with tool-level skills
- Updated catalogs, pipeline docs, and manifests for 24 skills total

## [1.0.0] - 2026-08-03

### Added
- Initial Metagenomics Skills package (Agent Skills layout)
- Multi-platform manifests and `scripts/install-platforms.sh`
