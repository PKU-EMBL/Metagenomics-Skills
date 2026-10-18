# Tool selection

Route by **scientific stage**, then deliverable. Full detail:
`skills/tool-selection/SKILL.md`. Also see `public-databases`,
`microbial-mining`, `resistome-analysis`, `mobilome-analysis`,
`arg-mge-host-linkage`, `horizontal-gene-transfer`, `strain-transmission`,
`transfer-network-analysis`, `research-analysis`, and `homology-search`.

## Stage → skill (summary)

| Stage | Deliverable | Skill(s) |
|-------|-------------|----------|
| Design | Strata / co-assembly plan | `study-design` |
| 1 QC | Adapter/quality trim | `fastp` (± `fastqc` / `multiqc`) |
| 1 QC | Host depletion | `kneaddata` |
| 2 Assembly | Fast contigs | `megahit` |
| 2 Assembly | Heavier / hybrid | `metaspades` / `metaflye` |
| 3 Mapping | Contig coverage | `strobealign` / `bowtie2` / `bwa-mem2` |
| 4 Binning | Recommended ensemble | `basalt` |
| 4 Binning | Suite / consensus | `metawrap` / `dastool` → `drep` |
| 4 Binning | QC / abundance | `checkm2` · `gunc` · `mag-qc` · `coverm` |
| 5 Taxonomy | Read-based | `metaphlan` / `singlem` / `kraken2` |
| 5 Taxonomy | Genome taxonomy | `gtdbtk` (+ `gtdb`) |
| 6 Function | Read pathways | `humann` (+ `biobakery-databases`) |
| 6 Function | Orthology / AMR | `eggnog-mapper` · `rgi` (± `resfinder` isolates) |
| 7 Mining | BGCs / CGE Finders / cycling / DOM / defense | `microbial-mining` · `cge-finders` |
| 7 Mining | ARG detection/quantity | `resistome-analysis` |
| 7 Mining | MGE boundaries/typing/hosts | `mobilome-analysis` → `arg-mge-host-linkage` |
| Evolution | HGT candidates by timescale | `horizontal-gene-transfer` |
| Strain | Microdiversity and sharing | `strain-resolved-analysis` → `strain-transmission` |
| Report | Stats / figures / association networks | `research-analysis` |
| Report | Typed transfer/propagation graph | `transfer-network-analysis` |
| Data | Public raw reads | `sra-ena` |
| Workflows | Portable DAGs | `nextflow` / `snakemake` |

## Parallel hubs (not a linear stage)

| Hub | When |
|-----|------|
| `homology-search` | Sequence / structure / vector-DB / warehouse search |
| `phylogenomics` | Trees / evolutionary placement |
| `element-cycling` | C/N/S/Fe/P biogeochemistry |
| `dom-biosurfactant` | Glycan DOM / biosurfactants / HC degradation |
| `cge-finders` | PlasmidFinder / ResFinder / PointFinder / DisinFinder / VF / MEF / pMLST / mlst / staramr / ABRicate |
| `resistome-analysis` | Curated/model ARG calls, quantification, context, and phenotype boundaries |
| `mobilome-analysis` | Plasmid/phage/integron/ICE boundaries, architecture, typing, and hosts |
| `arg-mge-host-linkage` | Coordinate, long-read, Hi-C, CRISPR, and host evidence ladder |
| `horizontal-gene-transfer` | MetaCHIP/WAAFLE/HGTector/Gubbins by timescale |
| `strain-transmission` | Callability/background/epidemiology and transmission models |
| `transfer-network-analysis` | Preserve typed edge semantics and provenance |
| `genome-language-model` | DNA gLMs |
| `protein-language-model` | Protein LMs |
| `metagenomics-llm` | LM + Foldseek stack overview |

## Binning family

| Situation | Skill |
|-----------|-------|
| **Recommended** related multi-assembly refinement | `basalt` |
| Classical multi-binner + CheckM-style refinement | `metawrap` |
| Aggregate existing contig2bin predictions | `dastool` |

## Public databases

See [public-databases.md](public-databases.md) and the
[ARG–MGE–host–strain evidence guide](arg-mge-host-strain.md).
