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
