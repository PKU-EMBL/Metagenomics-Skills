## [1.24.0] - 2026-10-18

### Added
- Six evidence-aware workflow Skills for resistome analysis, mobilome analysis,
  ARG–MGE–host linkage, horizontal gene transfer, strain transmission, and typed
  transfer-network analysis
- Nineteen reviewed tool Skills: AMRFinderPlus, ARGs-OAP, PathoFact 2.0, PlasX,
  MobMess, MetaCHIP2, WAAFLE, HGTector2, MetaTOR, HiCBin, ViralCC,
  SpacePHARER, MIDAS2, StrainGE, StrainFacts, PopPUNK, Gubbins,
  SourceTracker2, and TransPhylo
- A bundled edge-schema validator and the ARG–MGE–host–strain evidence guide,
  including resistome R0–R5, linkage L0–L5, and transmission T0–T4 ladders
- `resistome-mobilome` and `transmission` installation profiles plus six OpenAI
  UI manifests for the new workflow Skills

### Changed
- Updated DeepARG to the 2.0.0 `deeparg predict` contract and pinned the reviewed
  Hugging Face model/database bundle revision
- Expanded mining, strain, source-tracking, statistics, and end-to-end routers so
  ARG detection, abundance, physical co-location, host linkage, HGT, source
  contribution, strain sharing, and direct transmission remain separate claims
- Added evidence-typed network semantics for containment, host, Hi-C, sequence,
  gene-sharing, co-occurrence, source, HGT, strain-sharing, and transmission edges
- Synchronized the catalog, profiles, documentation, installer metadata, and all
  platform manifests at package version 1.24.0 (226 Skills)

## [1.23.0] - 2026-10-18

### Added
- 38 Skills for contamination control, long-read QC, viral/vOTU analysis,
  strain resolution, microbial eukaryotes, pangenomes, absolute abundance,
  metatranscriptomics, source tracking, compositional statistics, and community
  metabolic modeling
- Executable tool guidance for decontam, NanoPlot, Chopper, Filtlong, Hostile,
  HiFiAdapterFilt, sourmash, iPHoP, VIBRANT, StrainPhlAn, metaSNV, Tiara,
  EukCC, Whokaryote, Panaroo, PPanGGOLiN, ALDEx2, corncob, NetCoMi,
  SortMeRNA, CarveMe, MICOM, FEAST, MetaCoAG, and two pinned nf-core workflows
- Nine task-focused installation profiles: `contamination`, `long-read`,
  `virome`, `strain-resolved`, `eukaryotic`, `pangenome`,
  `metatranscriptomics`, `metabolic-modeling`, and `workflows`
- OpenAI UI manifests for 13 new workflow/orchestration Skills

### Changed
- Hardened core QC, assembly, mapping, binning, taxonomy, function, viral,
  statistics, and reporting Skills with input/output gates, recovery,
  provenance, database coupling, and interpretation limits
- Added scientific-stage metadata to all 37 previously unclassified Skills and
  review/command-status metadata to new and priority legacy Skills
- Replaced the audited guidance-only placeholder blocks with reviewed command
  contracts or explicit web/research-code boundaries; all Bash/Python examples
  now pass static syntax checks
- Extended the validator to enforce workflow stages, coherent review metadata,
  ISO review dates, non-empty executable fences, and Bash/Python syntax
- Synchronized the complete catalog, profiles, installer output, and every
  platform manifest at package version 1.23.0 (201 Skills)
- Marked new command examples by review status; upstream-reviewed examples are
  not represented as locally executed validation

## [1.22.0] - 2026-10-17

### Added
- Native packaging for ZCode (`.zcode-plugin/plugin.json` + marketplace), Qwen
  Code (`qwen-extension.json`), Claude plugin metadata, and portable Agent
  Plugins v1 (`plugin.json`)
- Cross-platform Python installer with safe link/copy modes, custom targets,
  project roots, dry runs, conflict backups, managed pruning, and seven
  context-aware profiles
- Simplified Chinese quick start (`README.zh-CN.md`)
- Platform-neutral coding-agent execution playbook and bundled multi-stage
  preflight/quality-gate reference
- Agent Skills/frontmatter, manifest, profile, resource-link, and Markdown-link
  validator with CI smoke tests

### Changed
- Normalized all 163 skills to the Agent Skills frontmatter specification;
  package fields now use string-valued `metadata` keys
- Reduced catalog metadata by removing duplicated upstream/routing boilerplate
  from descriptions while retaining task-specific trigger guidance
- Normalized 75 Codex/OpenAI UI entries with complete short descriptions,
  explicit skill invocation, input checks, and verified-output language
- Made repository-wide documentation links portable for copied skill bundles
- Expanded study design, setup, workflow execution, fastp verification, and
  statistical-analysis guidance with controls, confounding, provenance, pilots,
  output gates, and truthful execution status
- Synchronized the `metagenomics` plugin ID across Claude, Codex, Cursor,
  ZCode, Qwen, and Agent Plugins v1 manifests for marketplace validation
- Updated platform docs for Kimi Code, ZCode, Qwen Code, shared `.agents`,
  Windows copy mode, and metadata-budget-aware profiles
- Package version 1.22.0 (163 skills)

## [1.21.0] - 2026-08-03

### Added
- CGE / isolate typing extensions: `disinfinder`, `pmlst`, `mlst`, `abricate`
- References 136–138

### Changed
- Expanded `cge-finders` routing for biocide genes, plasmid/chromosomal ST,
  and multi-DB mass screens
- Skills catalog total: 163; package version 1.21.0

## [1.20.0] - 2026-08-03

### Added
- CGE Finder layer: `cge-finders` hub, `plasmidfinder`, `resfinder`,
  `pointfinder`, `virulencefinder`, `mobileelementfinder`, `staramr`
- References 129–135

### Changed
- Skills catalog total: 159; package version 1.20.0
- Wired CGE Finders into microbial-mining / tool-selection / docs

## [1.19.1] - 2026-08-03

### Changed
- Polished routing docs: README, getting-started, docs/tool-selection aligned
  with research-analysis / LM / mining hubs
- Clarified OMG → `genome-language-model`; Foldseek family → homology-search
- Catalogued `busco` in docs/skills.md; refreshed workflow/tool-selection blurbs
- Package version 1.19.1 (152 skills)

## [1.19.0] - 2026-08-03

### Added
- Research analysis extensions: `ancombc`, `sparcc`, `spieceasi`, `stamp`,
  `phyloseq`, `nextflow`, `snakemake`
- References 122–128

### Changed
- Skills catalog total: 152; package version 1.19.0

## [1.18.0] - 2026-08-03

### Added
- Research analysis layer: `research-analysis` hub, `microeco`, `maaslin2`,
  `lefse`, `multiqc`; deepened `visualization`
- References 118–121

### Changed
- Skills catalog total: 145; package version 1.18.0

## [1.17.0] - 2026-08-03

### Added
- DOM / biosurfactant layer: `dom-biosurfactant` hub, `hadeg`, `biosurfdb`
- Deepened `dbcan` for glycan DOM substrate / CGC prediction
- References 115–117

### Changed
- Skills catalog total: 140; package version 1.17.0

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
