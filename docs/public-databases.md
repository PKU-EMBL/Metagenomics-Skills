# Public databases

Public metagenomics resources are a **data skill layer** separate from analysis
tools. Start at `skills/public-databases/SKILL.md`, then open the per-resource
skill.

## Resource → skill

| Resource | Skill | Typical use |
|----------|-------|-------------|
| NCBI SRA / EBI ENA | `sra-ena` | Download public shotgun reads |
| MGnify (+ UHGG / biome catalogues) | `mgnify` | Analysed studies; MAG/protein catalogues |
| GTDB releases (e.g. R10-RS226) | `gtdb` | Taxonomy tables, trees, genome reps |
| proGenomes4 | `progenomes` | ~2M QC'd annotated prokaryotic genomes |
| CAMI / CAMI II (+ CAMISIM, AMBER, OPAL) | `cami` | Gold-standard benchmarks & evaluation |
| KEGG (KO / pathways; license applies) | `kegg` | Orthology & pathway reference |
| Virtual Metabolic Human | `vmh` | Human/gut metabolism knowledge for GEMs |
| InSilicoSeq | `insilicoseq` | Illumina metagenome read simulation |
| OMG / gLM2 | `omg` | Metagenomic LM pretraining corpus + mixed-modality gLM |
| ChocoPhlAn / UniRef / MetaCyc | `biobakery-databases` | MetaPhlAn / HUMAnN indexes |
| Kraken2 indexes | `kraken2` | k-mer classification DBs |
| eggNOG | `eggnog-mapper` | Orthology DB for annotation |
| CARD | `rgi` | AMR reference |
| CheckM2 DB | `checkm2` | MAG quality models |
| Host Bowtie2 indexes | `kneaddata` | Host depletion |
| BASALT weights | `basalt` / `setup` | Refinement models |

## Four data layers (do not mix unlabeled)

```text
1. Raw archives          SRA / ENA
2. Genome catalogues     MGnify biomes, GTDB reps, proGenomes
3. Tool indexes          Kraken, ChocoPhlAn, CheckM2, CARD, GTDB-Tk data
4. Benchmarks            CAMI / CAMI II gold standards (CAMISIM simulations)
```

## Quick chooser

| You need… | Open |
|-----------|------|
| Reanalyse a published shotgun study | `sra-ena` (± `mgnify` for analysed context) |
| Compare your MAGs to human-gut species | `mgnify` (UHGG) + `gtdbtk` |
| Cite / update prokaryotic taxonomy | `gtdb` (pin release, e.g. R10) |
| Build a large annotated reference genome set | `progenomes` |
| Benchmark a binner/profiler with truth | `cami` |
| KO / KEGG pathway maps | `kegg` (confirm access rights) |
| Marker + pathway profiling indexes | `biobakery-databases` |

## Thinking checklist

1. Separate **raw archives**, **catalogues**, **tool indexes**, and **benchmarks**
2. Pin release / accession / dataset DOI / download date (checksum when available)
3. Do not merge MetaPhlAn, Kraken, and GTDB labels into one table
4. UHGG/MGnify membership ≠ detection in your sample without abundance evidence
5. CAMI “best tool” is dataset-conditioned — report which challenge set you used
6. Sequence abundance ≠ taxonomic abundance in profiler benchmarks

## AI / language-model & structure-search data

For genome language models start at `genome-language-model` (`omg`,
`nucleotide-transformer`, `dnabert2`, `caduceus`, `evo2`). For PLM-assisted
annotation also see `metagenomics-llm`. For AFDB/PDB/ESM Atlas structure
indexes use `foldseek` /
`folddisco`. For vector-DB homology use `erast`; for phylogeny-compressed
genome search collections use `phylign` (see also `homology-search`). These are
**ML corpora / structure / search indexes**, not substitutes for SRA reanalysis
or GTDB taxonomy claims.

## See also

- [Skills catalog](skills.md)
- [References](references.md)
- [Standard pipeline](standard-pipeline.md)
- [Getting started](getting-started.md)
