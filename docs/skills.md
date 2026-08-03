# Skills

Software-level and orchestration skills in **Metagenomics Skills**.

Install once; categories are organizational only.

---

## Analysis tools — QC & host

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `fastp` | [OpenGene/fastp](https://github.com/OpenGene/fastp) | Short-read QC / trimming |
| `kneaddata` | [biobakery/kneaddata](https://github.com/biobakery/kneaddata) | Host / contaminant depletion |

## Analysis tools — read-based profiling

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metaphlan` | [biobakery/MetaPhlAn](https://github.com/biobakery/MetaPhlAn) | Marker taxonomic profiles |
| `humann` | [biobakery/humann](https://github.com/biobakery/humann) | Gene-family / pathway profiles |
| `kraken2` | [DerrickWood/kraken2](https://github.com/DerrickWood/kraken2) | k-mer classification (+ Bracken) |

## Analysis tools — assembly & genes

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `megahit` | [voutcn/megahit](https://github.com/voutcn/megahit) | Fast metagenome assembly |
| `metaspades` | [ablab/spades](https://github.com/ablab/spades) | metaSPAdes assembly |
| `prodigal` | [hyattpd/Prodigal](https://github.com/hyattpd/Prodigal) | ORF prediction (`-p meta`) |
| `cd-hit` | [weizhongli/cdhit](https://github.com/weizhongli/cdhit) | Gene clustering / NR catalogue |
| `salmon` | [COMBINE-lab/salmon](https://github.com/COMBINE-lab/salmon) | Gene abundance quantification |
| `eggnog-mapper` | [eggnogdb/eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper) | Orthology / function |
| `rgi` | [arpcard/rgi](https://github.com/arpcard/rgi) | CARD AMR annotation |

## Analysis tools — MAGs

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metawrap` | [bxlab/metaWRAP](https://github.com/bxlab/metaWRAP) | Binning + refinement suite |
| `basalt` | [PKU-EMBL/BASALT](https://github.com/PKU-EMBL/BASALT) | Multi-assembly refined MAGs |
| `drep` | [MrOlm/drep](https://github.com/MrOlm/drep) | Genome dereplication |
| `coverm` | [wwood/CoverM](https://github.com/wwood/CoverM) | Genome abundance |
| `gtdbtk` | [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk) | GTDB taxonomy |
| `checkm2` | [chklovski/CheckM2](https://github.com/chklovski/CheckM2) | Completeness / contamination |

## Evaluation

| Skill | Purpose |
|-------|---------|
| `mag-qc` | Acceptance criteria and filtering policy |
| `visualization` | Diversity / composition / MAG figures |

## Utilities

| Skill | Purpose |
|-------|---------|
| `setup` | Environments, databases, BASALT weights |

## Orchestration

| Skill | Purpose |
|-------|---------|
| `tool-selection` | Which software skill to use |
| `metagenomics-workflow` | End-to-end stage order |
| `study-design` | Co-assembly / strata / manifests |

---

## See also

- [Getting started](getting-started.md)
- [Standard pipeline](standard-pipeline.md)
- [Tool selection](tool-selection.md)
- [Multi-platform](multi-platform.md)
