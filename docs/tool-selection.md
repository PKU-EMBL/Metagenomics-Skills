# Tool selection

Route by **scientific stage**, then deliverable. Full detail:
`skills/tool-selection/SKILL.md`. Also see `public-databases`,
`microbial-mining`, `research-analysis`, `homology-search`,
`genome-language-model`, `protein-language-model`.

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
| 7 Mining | BGCs / MGE / CGE Finders / cycling / DOM / defense | `microbial-mining` · `cge-finders` |
| Report | Stats / figures / networks | `research-analysis` |
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

See [public-databases.md](public-databases.md).
