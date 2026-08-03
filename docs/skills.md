# Skills

Skills grouped by scientific stage (QC → assembly → mapping → binning → taxonomy → function → microbial mining).

Total: **100** skills.

---

## 1. Quality control

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `fastp` | [fastp](https://github.com/OpenGene/fastp) | Ultra-fast FASTQ QC/adapter trimming for Illumina/MGI short reads. |
| `kneaddata` | [kneaddata](https://github.com/biobakery/kneaddata) | QC wrapper focused on host (and contaminant) read removal via Bowtie2. |
| `fastqc` | [fastqc](https://github.com/s-andrews/FastQC) | QC reports for Illumina FASTQ before/after trimming. |
| `cutadapt` | [cutadapt](https://github.com/marcelm/cutadapt) | Adapter/primer trimming for short and long reads. |
| `trimmomatic` | [trimmomatic](https://github.com/usadellab/Trimmomatic) | Flexible Illumina adapter/quality trimmer. |

## 2. Assembly

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `megahit` | [megahit](https://github.com/voutcn/megahit) | Ultra-fast memory-efficient metagenome assembler. |
| `metaspades` | [metaspades](https://github.com/ablab/spades) | More sensitive metagenomic assembly via SPAdes meta mode. |
| `metaflye` | [metaflye](https://github.com/fenderglass/Flye) | Long-read metagenome assembly with Flye/metaFlye. |
| `metamdbg` | [metamdbg](https://github.com/GaetanBenoitDev/metaMDBG) | High-quality metagenome assembly from long accurate reads. |
| `racon` | [racon](https://github.com/lbcb-sci/racon) | Ultrafast consensus polishing of assemblies using mapped long (or short) reads. |
| `pilon` | [pilon](https://github.com/broadinstitute/pilon) | Polish genome assemblies and fix small errors using short-read BAM evidence. |
| `quast` | [quast](https://github.com/ablab/quast) | Assembly quality assessment (contiguity, misassemblies; metaQUAST for metagenomes). |
| `binchicken` | [binchicken](https://github.com/AroneyS/binchicken) | Targeted coassembly planning (SingleM markers) to recover low-abundance / novel genomes. |

## 3. Mapping

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `bowtie2` | [bowtie2](https://github.com/BenLangmead/bowtie2) | Gapped short-read alignment to contigs/genomes for coverage used in binning and abundance. |
| `strobealign` | [strobealign](https://github.com/ksahlin/strobealign) | Ultra-fast short-read alignment with flexible seed size for metagenome coverage mapping. |
| `bwa` | [bwa](https://github.com/lh3/bwa) | Burrows–Wheeler short-read alignment (BWA-MEM) to contigs/genomes. |
| `bwa-mem2` | [bwa-mem2](https://github.com/bwa-mem2/bwa-mem2) | Architecture-aware faster BWA-MEM for Illumina reads to contigs/genomes. |
| `minimap2` | [minimap2](https://github.com/lh3/minimap2) | Fast pairwise alignment for long reads and genome-to-genome maps. |
| `lexicmap` | [lexicmap](https://github.com/shenwei356/LexicMap) | Align genes/plasmids/long queries against millions of prokaryotic genomes. |
| `samtools` | [samtools](https://github.com/samtools/samtools) | SAM/BAM/CRAM processing for metagenomic mapping outputs — sort, index, flagstat, coverage, and filtering. |
| `bbmap` | [bbmap](https://sourceforge.net/projects/bbmap/) | Fast splice-aware aligner and BBTools suite utilities (BBMerge, etc. |
| `diamond` | [diamond](https://github.com/bbuchfink/diamond) | Ultra-fast protein alignment (BLASTP/X alternative) for functional/taxonomic searches. |

## 4. Binning

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metabat2` | [metabat2](https://bitbucket.org/berkeleylab/metabat) | Adaptive contig binning from tetranucleotide composition and multi-sample coverage. |
| `maxbin2` | [maxbin2](https://sourceforge.net/projects/maxbin2/) | Automated multi-metagenome contig binning. |
| `concoct` | [concoct](https://github.com/BinPro/CONCOCT) | Composition and coverage binning of metagenomic contigs. |
| `semibin2` | [semibin2](https://github.com/BigDataBiology/SemiBin) | Self-supervised contrastive learning binning for short- and long-read assemblies. |
| `vamb` | [vamb](https://github.com/RasmussenLab/vamb) | Deep variational autoencoder binning of metagenome contigs. |
| `comebin` | [comebin](https://github.com/ziyewang/COMEBin) | Contrastive multi-view representation learning for contig binning. |
| `lorbin` | [lorbin](https://github.com/LorMeBioAI/LorBin) | Unsupervised long-read metagenome binning with multiscale adaptive clustering. |
| `aamb` | [aamb](https://github.com/RasmussenLab/vamb) | AAMB/AVAMB adversarial autoencoder binning (VAMB family ensemble). |
| `taxvamb` | [taxvamb](https://github.com/RasmussenLab/vamb) | Taxonomy-informed VAMB-family binning (TaxVAMB). |
| `metabinner` | [metabinner](https://github.com/ziyewang/MetaBinner) | Stand-alone multi-feature ensemble contig binning. |
| `anvio` | [anvio](https://github.com/merenlab/anvio) | Interactive multi-omics platform for MAG refinement and visualization. |
| `deepurify` | [deepurify](https://github.com/ericcombiolab/Deepurify) | Deep-learning MAG decontamination / chimera splitting. |
| `fastani` | [fastani](https://github.com/ParBLiSS/FastANI) | Classic high-throughput ANI (pair with skani). |
| `basalt` | [basalt](https://github.com/PKU-EMBL/BASALT) | PKU-EMBL BASALT and BASALT-Air — recommended ensemble MAG recovery across one or more assemblies (multi-binner + refinement). |
| `metawrap` | [metawrap](https://github.com/bxlab/metaWRAP) | MetaWRAP suite for multi-binner MAG recovery and CheckM-style bin refinement — one option in the ensemble binning family (with DAS Tool and BASALT). |
| `dastool` | [dastool](https://github.com/cmks/DAS_Tool) | DAS Tool (Dereplication, Aggregation and Scoring) integrates multiple binning predictions into one non-redundant MAG set for a single assembly. |
| `drep` | [drep](https://github.com/MrOlm/drep) | Dereplicate microbial genomes by ANI to species/strain catalogues. |
| `skani` | [skani](https://github.com/bluenote-1577/skani) | Fast robust average nucleotide identity (ANI) for metagenomic genomes and MAG comparisons. |
| `coverm` | [coverm](https://github.com/wwood/CoverM) | Calculate coverage/relative abundance of genomes or contigs. |
| `checkm2` | [checkm2](https://github.com/chklovski/CheckM2) | ML-based MAG completeness and contamination estimation. |
| `gunc` | [gunc](https://github.com/grp-bork/gunc) | Detect chimerism/contamination in prokaryotic genomes/MAGs. |
| `mag-qc` | — | Quality thresholds after binning (completeness/contamination, dRep ANI, publication vs refinement gates). |

## 5. Taxonomic annotation

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metaphlan` | [metaphlan](https://github.com/biobakery/MetaPhlAn) | Marker-gene taxonomic profiling of metagenomes. |
| `kraken2` | [kraken2](https://github.com/DerrickWood/kraken2) | k-mer taxonomic classification; pair with Bracken for abundance. |
| `bracken` | [bracken](https://github.com/jenniferlu717/Bracken) | Bayesian re-estimation of abundance from Kraken2 reports. |
| `motus` | [motus](https://github.com/motu-tool/mOTUs) | Marker-gene taxonomic profiling across environments (mOTUs3). |
| `sylph` | [sylph](https://github.com/bluenote-1577/sylph) | Rapid species-level metagenome profiling and containment estimation. |
| `singlem` | [singlem](https://github.com/wwood/singlem) | Marker-window profiling including species without genomes; Sandpiper. |
| `metabuli` | [metabuli](https://github.com/steineggerlab/Metabuli) | Joint DNA + amino-acid metagenomic taxonomic classification (metamers). |
| `kaiju` | [kaiju](https://github.com/bioinformatics-centre/kaiju) | Fast sensitive taxonomic classification via protein-level matches. |
| `gtdbtk` | [gtdbtk](https://github.com/Ecogenomics/GTDBTk) | Assign bacterial/archaeal taxonomy to MAGs with GTDB. |
| `gtdb` | [gtdb](https://gtdb.ecogenomic.org/) | Use the Genome Taxonomy Database (GTDB) public releases (e.g. R10) — taxonomy tables, trees, metadata, and representative genomes. |
| `mgnify` | [mgnify](https://github.com/EBI-Metagenomics) | Use EMBL-EBI MGnify for analysed microbiome studies and biome genome catalogues (including UHGG / human-gut and other biomes). |

## 6. Functional annotation

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `humann` | [humann](https://github.com/biobakery/humann) | Gene-family and pathway abundance profiling from metagenomes. |
| `prodigal` | [prodigal](https://github.com/hyattpd/Prodigal) | Protein-coding gene prediction; use -p meta for metagenomes. |
| `prokka` | [prokka](https://github.com/tseemann/prokka) | Rapid prokaryotic genome annotation (CDS/rRNA/tRNA). |
| `bakta` | [bakta](https://github.com/oschwengers/bakta) | Rapid standardized annotation of bacterial genomes (alignment-free ID). |
| `cd-hit` | [cd-hit](https://github.com/weizhongli/cdhit) | Cluster genes/proteins to build non-redundant catalogues. |
| `mmseqs2` | [mmseqs2](https://github.com/soedinglab/MMseqs2) | Ultra-fast protein search, clustering, and contig taxonomy (Steinegger stack). |
| `salmon` | [salmon](https://github.com/COMBINE-lab/salmon) | Fast quantification of gene/transcript abundance; use --meta for metagenomes. |
| `eggnog-mapper` | [eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper) | Orthology-based functional annotation (COG/KEGG/CAZy via eggNOG). |
| `rgi` | [rgi](https://github.com/arpcard/rgi) | Antibiotic resistance gene annotation against CARD. |
| `barrnap` | [barrnap](https://github.com/tseemann/barrnap) | Basic rapid ribosomal RNA predictor for genomes. |
| `biobakery-databases` | [biobakery-databases](https://github.com/biobakery/biobakery) | Install and pin bioBakery reference databases for MetaPhlAn and HUMAnN (ChocoPhlAn markers, UniRef gene families, MetaCyc pathways, utility mapping). |

## 7. Microbial mining

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `microbial-mining` | — | Route microbial / genome mining after assembly or binning: biosynthetic gene clusters (antiSMASH, BiG-SCAPE), AMR (RGI, DeepARG), mobile elements and viruses (geNomad, VirSorter2, CheckV), antimicrobial peptides (Macrel), metabolism (DRAM, gapseq, dbCAN), defense systems (DefenseFinder), and genome annotation substrates (Bakta/Prokka). |
| `antismash` | [antismash](https://github.com/antismash/antismash) | Detect and annotate biosynthetic gene clusters (BGCs) on genomes and MAGs. |
| `bigscape` | [bigscape](https://github.com/medema-group/BiG-SCAPE) | Cluster and compare biosynthetic gene clusters across genomes with BiG-SCAPE (similarity networks of antiSMASH regions). |
| `genomad` | [genomad](https://github.com/apcamargo/genomad) | Identify plasmids, viruses, and other mobile genetic elements in assemblies or genomes. |
| `virsorter2` | [virsorter2](https://github.com/jiarong/VirSorter2) | Viral sequence identification from metagenomic assemblies. |
| `checkv` | [checkv](https://bitbucket.org/berkeleylab/checkv) | Quality assessment of metagenome-assembled viral genomes. |
| `vcontact` | [vcontact](https://bitbucket.org/MAVERICLab/vcontact3) | vConTACT2/3 gene-sharing / ML hierarchical virus taxonomy. |
| `plasmaag` | [plasmaag](https://github.com/RasmussenLab/PlasMAAG) | Plasmid and organism reconstruction via assembly–alignment graphs. |
| `macrel` | [macrel](https://github.com/BigDataBiology/macrel) | Screen genomes and metagenomes for antimicrobial peptides (AMPs). |
| `dram` | [dram](https://github.com/WrightonLabCSU/DRAM) | Distill microbial metabolism annotations for MAGs/genomes into curated product tables (DRAM annotate + distill). |
| `dbcan` | [dbcan](https://github.com/linnabrown/run_dbcan) | Annotate carbohydrate-active enzymes (CAZymes) with dbCAN/run_dbcan on genomes or protein sets. |
| `gapseq` | [gapseq](https://github.com/jotech/gapseq) | Predict bacterial metabolic pathways and reconstruct genome-scale metabolic models. |
| `deeparg` | [deeparg](https://github.com/gaarangoa/DeepARG) | Deep-learning prediction of antibiotic resistance genes from metagenomic data. |
| `defensefinder` | [defensefinder](https://github.com/mdmparis/defense-finder) | Detect anti-phage defense systems in prokaryotic genomes. |

## Strain / microdiversity

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `instrain` | [instrain](https://github.com/MrOlm/inStrain) | Strain-level microdiversity and shared-strain detection from metagenomes. |

## Public data

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `public-databases` | — | Route shotgun metagenomics work across raw archives, catalogues, tool indexes, and CAMI benchmarks. |
| `sra-ena` | [sra-ena](https://github.com/ncbi/sra-tools) | Fetch and cite public shotgun metagenomic reads from NCBI SRA and EBI ENA. |
| `cami` | [cami](https://cami-challenge.org/) | CAMI / CAMI II gold-standard benchmarks plus CAMISIM, AMBER, and OPAL evaluation. |
| `progenomes` | [progenomes](https://progenomes.embl.de/) | proGenomes4 — ~2M consistently annotated high-quality prokaryotic genomes. |
| `kegg` | [kegg](https://www.kegg.jp/) | KEGG KO / pathway reference for gene and protein annotation (license applies). |
| `vmh` | [vmh](https://www.vmh.life) | Virtual Metabolic Human — human/gut metabolism knowledge for GEM interpretation. |
| `insilicoseq` | [insilicoseq](https://github.com/HadrienG/InSilicoSeq) | Simulate Illumina metagenomic reads (pair with CAMI/CAMISIM). |
| `mgnify` | [mgnify](https://github.com/EBI-Metagenomics) | MGnify analysed studies and biome genome catalogues (UHGG and others) — also under Taxonomy. |
| `gtdb` | [gtdb](https://gtdb.ecogenomic.org/) | GTDB public releases — also under Taxonomy. |
| `biobakery-databases` | [biobakery](https://github.com/biobakery/biobakery) | MetaPhlAn / HUMAnN reference indexes — also under Function. |

## Report & utilities

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `visualization` | — | Statistical visualization for shotgun metagenomics across QC, taxonomy, function, and binning outputs. |
| `setup` | — | First-time environment and database setup for shotgun metagenomics tool skills. |


## AI / language models & structure search

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metagenomics-llm` | — | Route genomic/protein LMs and Steinegger structure/sequence search. |
| `omg` | [OMG](https://github.com/TattaBio/OMG) | Open MetaGenomic corpus + gLM2 mixed-modality genomic language model. |
| `mmseqs2` | [MMseqs2](https://github.com/soedinglab/MMseqs2) | Sequence search, Linclust NR, contig taxonomy — also under Function. |
| `foldseek` | [Foldseek](https://github.com/steineggerlab/foldseek) | Ultrafast 3Di structure search, clustering, Foldseek-Multimer, ProstT5. |
| `folddisco` | [Folddisco](https://github.com/steineggerlab/folddisco) | Fast discontinuous structural motif search (AFDB/PDB/ESM30). |
| `plmsearch` | [PLMSearch](https://github.com/maovshao/PLMSearch) | PLM embeddings for fast remote homology protein search. |
| `deepblast` | [DeepBLAST](https://github.com/flatironinstitute/deepblast) | TM-Vec + DeepBLAST remote homology and structural alignment from sequence. |
| `spacedust` | [Spacedust](https://github.com/soedinglab/Spacedust) | De novo conserved gene clusters via Foldseek-aware neighborhood discovery. |
| `alphagem` | [AlphaGEM](https://github.com/hongzhonglu/AlphaGEM) | GEMs with structure alignment and DL dark-metabolism mining. |

## Orchestration

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `tool-selection` | — | Choose shotgun tools by stage: QC, assembly, mapping, binning, taxonomic annotation, functional annotation, and microbial mining. |
| `metagenomics-workflow` | — | End-to-end shotgun metagenomics: quality control, assembly, mapping, binning, taxonomic annotation, functional annotation, and microbial mining (BGCs, AMR, MGEs/viruses, AMPs, metabolism, defense). |
| `study-design` | — | Study design for shotgun metagenomics across QC, assembly, binning, and annotation. |
| `metagenomics-llm` | — | Route LMs and Foldseek/MMseqs structure–sequence search (also under AI). |

## Other

- `busco`

---

## See also

- [Standard pipeline](standard-pipeline.md)
- [Tool selection](tool-selection.md)
- [Public databases](public-databases.md)
- [References](references.md)
- [Troubleshooting](troubleshooting.md)
- [Getting started](getting-started.md)
