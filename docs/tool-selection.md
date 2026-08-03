# Tool selection

Per-software routing for Metagenomics Skills. Detailed rationale lives in
`skills/tool-selection/SKILL.md`.

## Deliverable → skill

| Deliverable | Skill(s) |
|-------------|----------|
| Adapter/QC trim | `fastp` |
| Host depletion | `kneaddata` |
| Marker taxonomy | `metaphlan` |
| Pathways from reads | `humann` |
| k-mer taxonomy | `kraken2` |
| Fast assembly | `megahit` |
| Heavier / hybrid assembly | `metaspades` |
| ORF calling | `prodigal` |
| NR gene catalogue | `cd-hit` |
| Gene abundance | `salmon` |
| Orthology/function | `eggnog-mapper` |
| AMR genes | `rgi` |
| Classical MAG binning | `metawrap` |
| Refined multi-assembly MAGs | `basalt` |
| Dereplicate genomes | `drep` |
| Genome abundance | `coverm` |
| GTDB taxonomy | `gtdbtk` |
| Completeness/contamination | `checkm2` |
| Filter policy | `mag-qc` |
| Figures | `visualization` |

## Classical MAG vs BASALT

| Situation | Skill |
|-----------|-------|
| MetaWRAP binning + refinement catalogue | `metawrap` then `drep` |
| Related samples, cross-assembly refinement | `basalt` |
| Absolute paths / new deployment | BASALT-Air via `basalt` |
