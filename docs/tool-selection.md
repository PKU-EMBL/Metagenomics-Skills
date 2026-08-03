# Tool selection

Route by **scientific stage**, then deliverable. Details:
`skills/tool-selection/SKILL.md`, `skills/public-databases/SKILL.md`.

## Stage → skill

| Stage | Deliverable | Skill(s) |
|-------|-------------|----------|
| 1 QC | Adapter/quality trim | `fastp` |
| 1 QC | Host depletion | `kneaddata` |
| 2 Assembly | Fast contigs | `megahit` |
| 2 Assembly | Heavier / hybrid | `metaspades` |
| 3 Binning | Recommended ensemble | `basalt` |
| 3 Binning | Suite multi-binner | `metawrap` → `drep` |
| 3 Binning | Contig2bin consensus | `dastool` |
| 3 Binning | Dereplicate / abundance / QC | `drep`, `coverm`, `checkm2`, `mag-qc` |
| 4 Taxonomy | Read-based markers | `metaphlan` |
| 4 Taxonomy | Read-based k-mers | `kraken2` |
| 4 Taxonomy | Genome taxonomy | `gtdbtk` (+ `gtdb`) |
| 4 Taxonomy | Biome catalogue context | `mgnify` |
| 5 Function | Read pathways | `humann` (+ `biobakery-databases`) |
| 5 Function | Gene catalogue | `prodigal` → `cd-hit` → `salmon` |
| 5 Function | Orthology / AMR | `eggnog-mapper`, `rgi` |
| Data | Public raw reads | `sra-ena` |
| Report | Figures | `visualization` |

## Binning family (stage 3)

| Situation | Skill |
|-----------|-------|
| **Recommended** related multi-assembly refinement | `basalt` |
| Classical multi-binner + CheckM-style refinement | `metawrap` |
| Aggregate existing contig2bin predictions | `dastool` |

## Public databases

See [public-databases.md](public-databases.md).
