# EasyMetagenome protocol distillation

Upstream repository: [YongxinLiu/EasyMetagenome](https://github.com/YongxinLiu/EasyMetagenome) (v1.24+)  
Citation: Bai et al. (2025). *iMeta* 4: e70001. https://doi.org/10.1002/imt2.70001

This document summarises the community-scale shotgun workflow implemented by
EasyMetagenome: read preprocessing, taxonomic and functional profiling, gene
catalogue construction, and MetaWRAP-based MAG recovery. It is complementary to
BASALT-centred genome refinement. MetaWRAP parameter defaults must not be treated
as operationally equivalent to BASALT.

## Script map

| Script | Role |
|---|---|
| `0Install.sh` | Conda/mamba envs + databases (1–3 days, once) |
| `1Pipeline.sh` | Analysis stages 1–6 |
| `2StatPlot.sh` | R/bash visualization (alpha/beta, heatmaps, STAMP, MAGs plots) |
| `3Init.sh` | Small init helpers |

Project layout expected by the pipeline:

```text
$wd/
├── 1Pipeline.sh
├── seq/                 # SampleID_1.fq.gz, SampleID_2.fq.gz
├── temp/                # intermediates (deletable after success)
└── result/
    └── metadata.txt     # tab-delimited; SampleID in column 1
```

Canonical path variables (must be set every session):

```bash
soft=~/miniconda3   # conda root
db=~/db             # databases + EasyMicrobiome
wd=~/meta           # project
PATH=$soft/bin:$soft/condabin:$PATH:$db/EasyMicrobiome/linux:$db/EasyMicrobiome/script
```

Convert Windows metadata newlines before use: `sed -i 's/\r//' result/metadata.txt`.

## Stage decision tree

```text
raw PE reads + metadata
  → 1. QC (fastp) + host removal (KneadData)
  → branch A: read-based taxonomy/function (HUMAnN4 / MetaPhlAn4 / Kraken2)
  → branch B: co-assembly gene catalogue (MEGAHIT → Prodigal → cd-hit → salmon → eggNOG/CARD)
  → branch C: MAG recovery (MetaWRAP → dRep → CoverM → GTDB-Tk)
  → optional: isolate genomes / pangenome
  → 2StatPlot visualization
```

Run A alone for composition tables; B for gene/function catalogues; C when depth
supports MAGs. Prefer **BASALT** over MetaWRAP when the scientific goal is
PKU-EMBL-style multi-assembly refinement (see [basalt-cli.md](basalt-cli.md)).

## 1. Preprocessing

### Inputs

- `result/metadata.txt` (Excel → TSV; first column = sample IDs used in filenames)
- `seq/${SampleID}_1.fq.gz` and `_2.fq.gz`
- Check Phred33 vs Phred64; fix PE ID collisions before KneadData/MetaWRAP

### fastp

```bash
fastp -i seq/${i}_1.fq.gz -I seq/${i}_2.fq.gz \
  -j temp/qc/${i}_fastp.json -h temp/qc/${i}_fastp.html \
  -o temp/qc/${i}_1.fastq -O temp/qc/${i}_2.fastq
```

Batch with `rush` over `metadata.txt` column 1. Expect ~5× temporary space.

### KneadData host removal

Default human DB path in the pipeline: `${db}/kneaddata/human/hg_39`.

```bash
kneaddata -i1 temp/qc/${i}_1.fastq -i2 temp/qc/${i}_2.fastq \
  -o temp/hr --bypass-trim --bypass-trf --reorder \
  --bowtie2-options '--very-sensitive --dovetail' \
  -db ${db}/kneaddata/human/hg_39 \
  --remove-intermediate-output -v -t 3
```

- Use `--reorder` to keep PE IDs matched (MetaWRAP fails on mismatched pairs).
- Custom hosts: build a Bowtie2 index for the host genome of interest (plant,
  animal, etc.) per `0Install.sh`.
- Publish **dehosted** human-associated data when possible.
- After success, delete intermediates (`*contam*`, unmatched, QC FASTQs) to reclaim
  space (high-host samples can save >90%).

## 2. Read-based analysis

Primary stack: **HUMAnN4 + MetaPhlAn4**; parallel **Kraken2 + Bracken**.

| Product | Typical tools | Notes |
|---|---|---|
| Species profiles | MetaPhlAn4 (via HUMAnN) | Marker-based; not 16S OTUs |
| Pathway / gene families | HUMAnN4 | Needs merged PE input |
| k-mer taxonomy | Kraken2 + Bracken | DB choice dominates results |
| Biomarkers | LEfSe | Group labels must be in metadata |
| Trees | GraPhlAn / export2graphlan | Visualization, not classification |

Evidence boundaries:

- Marker vs k-mer vs assembly-derived taxonomy are **different claims**—do not
  average them into one “truth” table without labeling the method.
- HUMAnN pathway abundance ≠ enzyme activity.
- LEfSe/STAMP/MaAsLin2 need appropriate grouping and multiple-testing caution.

## 3. Assembly-based gene catalogue

| Step | Default tool / params | Output cue |
|---|---|---|
| Assemble | MEGAHIT (default); metaSPAdes optional (more RAM/time) | `temp/megahit/final.contigs.fa` |
| Evaluate | QUAST; metaQUAST optional | `result/megahit/quast` |
| Genes | Prodigal `-p meta` | `temp/prodigal/gene.fa` |
| Optional filter | `partial=00` full-length genes | reduces catalogue size |
| Dereplicate genes | `cd-hit-est -aS 0.9 -c 0.95 -G 0 -g 0` | `result/NR/nucleotide.fa` |
| Translate | `seqkit translate --trim` | `result/NR/protein.fa` |
| Quantify | salmon index + `salmon quant --meta` | `result/salmon/gene.TPM`, `gene.count` |
| Function | eggNOG-mapper (DIAMOND) → COG/KO/CAZy tables | `result/eggnog/` |
| AMR | RGI / CARD on proteins (optional nucleotides/contigs) | `result/card/` |
| Gene taxonomy | Kraken2 on NR genes | `result/NR/tax*` |

Notes:

- Co-assembly of all samples is the EasyMetagenome default for the gene catalogue;
  for stratified biology, assemble within strata (aligns with study-design rules).
- Large contig sets: length-filter before gene prediction (appendix megahit).
- Hybrid Illumina+long-read assembly is documented in the pipeline appendix
  (metaSPAdes / OPERA-MS)—record read roles explicitly.

## 4. Binning and MAG catalogue (MetaWRAP path)

Depth guidance from the pipeline authors: **≥~6 Gb/sample** for MAG mining;
complex soils often need **≥~30 Gb**. Tiny demos will not yield usable MAGs.

| Step | Default | Key params |
|---|---|---|
| Binning | MetaWRAP `binning` | `--metabat2 --maxbin2` (± CONCOCT costly) |
| Refine | MetaWRAP `bin_refinement` | `-c 50 -x 10` |
| Modes | mixed / single-sample / subgroup | rename prefixes `Mx_`, `Sg_`, `Gp_` |
| Dereplicate | dRep | species `-sa 0.95 -nc 0.30 -comp 50 -con 10`; strain `-sa 0.99` |
| QC refresh | CheckM2 | especially if dRep used `--ignoreGenomeQuality` |
| Quantify | CoverM `genome --coupled` | relative abundance table |
| Taxonomy | GTDB-Tk `classify_wf` | set `GTDBTK_DATA_PATH` |
| Tree | GTDB-Tk `infer` + iTOL annotations | merge tax + Widb + CoverM |

Subgroup binning when samples **>30** or data **>~300 Gb**: split by similar
condition/site into separate `metadata` files to avoid week-long fat-node jobs.

**Hand-off to BASALT:** when assemblies + PE (± long) reads exist and the goal is
cross-assembly refined MAGs, prefer BASALT/BASALT-Air. MetaWRAP remains the
EasyMetagenome classical route and a useful baseline.

## 5–6. Optional modules

- **Isolate / single-bacterium genomes:** fastp → metaSPAdes → CheckM → optional
  MetaWRAP if mixed → dRep → GTDB → eggNOG/dbCAN/ARG/antiSMASH.
- **Pangenome:** download NCBI genomes → CONTIGS library → pan-genome analysis
  (pipeline §6). Keep isolate claims separate from MAG claims.

## Visualization (`2StatPlot.sh`)

Typical figures (via EasyMicrobiome R scripts):

- MetaPhlAn4 / Kraken2: alpha boxplots, beta PCoA, heatmaps, stacked bars, Venn,
  STAMP, MaAsLin2 volcano, SparCC networks
- HUMAnN: grouped functional heatmaps
- MAGs: rarefaction, UpSet of annotation DBs, Sankey pathways, completeness vs
  contamination, phylogeny, ARG heatmaps
- Trees: table2itol annotations

Prefer publishing figures with explicit method labels (MetaPhlAn vs Kraken vs MAG).

## Rough runtime (from pipeline appendix)

On large servers (guidance only):

| Step | Small (~6 Gb × 3) | Large (~10 Gb × 20) |
|---|---|---|
| fastp | seconds | ~40 min |
| kneaddata | ~25 s | ~5 h |
| HUMAnN | ~34 min | ~30 h |
| MEGAHIT | ~39 s | ~15 h |
| MetaWRAP binning | ~6 h | ~16 h |
| bin refine | ~2 h | ~3 h |
| CoverM | ~4 min | ~30 min |

Recommend ≥60 cores: ~16 threads per parallel sample job; ~32 threads for mixed
assembly/binning.

## Install and China mirrors

- Prefer `0Install.sh` order; many envs are packed (`conda-pack`) with NMDC /
  Baidu backups (`ftp://download.nmdc.cn/tools/conda/`, Baidu link in README).
- Databases: KneadData hosts, HUMAnN/MetaPhlAn, Kraken2, eggNOG, CARD, GTDB-Tk,
  EasyMicrobiome script/annotation packs under `$db`.
- Common pitfalls: Java/Trimmomatic for KneadData, Perl `PERL5LIB` mismatches,
  PE rename for SRA-style IDs, MetaWRAP `shorten_contig_names.py` / blast version
  issues—see pipeline appendices before inventing fixes.

## Provenance minimum for EasyMetagenome runs

- EasyMetagenome git commit / version (e.g. v1.24)
- `metadata.txt` + raw/dehosted checksums
- Host genome identity used in KneadData
- Conda env names + `conda env export` for each stage env
- Database names/versions (MetaPhlAn, Kraken, eggNOG, CARD, GTDB)
- Assembly mode (co- vs per-sample vs subgroup)
- Binning/refine thresholds; dRep ANI; CoverM and GTDB-Tk commands
- Citation: Bai et al., *iMeta* 2025
