# Public databases

Public metagenomics resources are a separate skill layer from analysis tools.
Details live in `skills/public-databases/` and the per-resource skills below.

## Resource → skill

| Resource | Skill | Typical use |
|----------|-------|-------------|
| NCBI SRA / EBI ENA | `sra-ena` | Download public shotgun reads |
| MGnify (+ UHGG / biome catalogues) | `mgnify` | Analysed studies; MAG/protein catalogues |
| GTDB releases | `gtdb` | Taxonomy tables, trees, genome reps |
| ChocoPhlAn / UniRef / MetaCyc | `biobakery-databases` | MetaPhlAn / HUMAnN indexes |
| Kraken2 indexes | `kraken2` | k-mer classification DBs |
| eggNOG | `eggnog-mapper` | Orthology DB for annotation |
| CARD | `rgi` | AMR reference |
| CheckM2 DB | `checkm2` | MAG quality models |
| Host Bowtie2 indexes | `kneaddata` | Host depletion |
| BASALT weights | `basalt` / `setup` | Refinement models |

## Thinking checklist

1. Separate **raw archives**, **genome catalogues**, and **tool indexes** in Methods
2. Pin release / accession / download date (and checksum when available)
3. Do not merge MetaPhlAn, Kraken, and GTDB labels into one table
4. UHGG/MGnify membership ≠ detection in your sample without abundance evidence

## See also

- [Skills catalog](skills.md)
- [Tool selection](tool-selection.md)
- [Standard pipeline](standard-pipeline.md)
- [References](references.md)
