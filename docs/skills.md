# Skills

Skills grouped by scientific stage (QC → assembly → mapping → binning → taxonomy → function → microbial mining → research analysis), plus homology, phylogenomics, and language-model hubs.

Release: **v1.25.0** · Total: **226** skills.

For ARG, mobile-element, host, HGT, source, strain-sharing, and transmission evidence,
see the [typed evidence guide](arg-mge-host-strain.md).

---

## 1. Quality control

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `fastp` | [fastp](https://github.com/OpenGene/fastp) | Ultra-fast FASTQ QC/adapter trimming for Illumina/MGI short reads. |
| `kneaddata` | [kneaddata](https://github.com/biobakery/kneaddata) | QC wrapper focused on host (and contaminant) read removal via Bowtie2. |
| `fastqc` | [fastqc](https://github.com/s-andrews/FastQC) | QC reports for Illumina FASTQ before/after trimming. |
| `cutadapt` | [cutadapt](https://github.com/marcelm/cutadapt) | Adapter/primer trimming for short and long reads. |
| `trimmomatic` | [trimmomatic](https://github.com/usadellab/Trimmomatic) | Flexible Illumina adapter/quality trimmer. |
| `contamination-control` | — | Design controls, distinguish reagent/background/host contamination, and gate corrective actions. |
| `decontam` | [decontam](https://github.com/benjjneb/decontam) | Flag likely contaminants from negative-control prevalence or DNA-concentration frequency. |
| `hostile` | [Hostile](https://github.com/bede/hostile) | Fast host-read depletion with bundled or custom indexes and explicit depletion summaries. |
| `long-read-qc` | — | Route ONT and PacBio HiFi diagnostics, filtering, adapter control, and post-filter validation. |
| `nanoplot` | [NanoPlot](https://github.com/wdecoster/NanoPlot) | Long-read quality, length, yield, and channel/run diagnostics. |
| `chopper` | [Chopper](https://github.com/wdecoster/chopper) | Stream ONT FASTQ quality/length/headcrop/tailcrop filtering. |
| `filtlong` | [Filtlong](https://github.com/rrwick/Filtlong) | Quality-weighted long-read filtering with optional short-read evidence. |
| `hifiadapterfilt` | [HiFiAdapterFilt](https://github.com/sheinasim-USDA/HiFiAdapterFilt) | Remove PacBio HiFi adapter-contaminated reads. |
| `sortmerna` | [SortMeRNA](https://github.com/sortmerna/sortmerna) | Separate rRNA and non-rRNA reads for metatranscriptomics. |

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
| `nf-core-mag` | [nf-core/mag](https://github.com/nf-core/mag) | Versioned Nextflow workflow for assembly, binning, QC, taxonomy, and annotation. |

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
| `bbmap` | [bbmap](https://sourceforge.net/projects/bbmap/) | Fast splice-aware aligner and BBTools suite utilities (BBMerge, etc.). |
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
| `metacoag` | [MetaCoAG](https://github.com/metagentools/MetaCoAG) | Assembly-graph, coverage, composition, and marker-aware contig binning. |
| `metator` | [MetaTOR](https://github.com/koszullab/metaTOR) | Build normalized meta-Hi-C contact networks and proximity-derived MAGs. |
| `hicbin` | [HiCBin](https://github.com/dyxstat/HiCBin) | Normalize/filter Hi-C contacts and recover MAGs with Leiden clustering. |

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
| `sourmash` | [sourmash](https://github.com/sourmash-bio/sourmash) | FracMinHash signatures, containment/search, gather, and taxonomic summarization. |
| `tiara` | [Tiara](https://github.com/ibe-uw/tiara) | Neural-domain classification of prokaryotic, eukaryotic, organellar, and unknown contigs. |
| `whokaryote` | [Whokaryote](https://github.com/LottePronk/whokaryote) | Separate eukaryotic and prokaryotic metagenomic contigs. |
| `eukcc` | [EukCC](https://github.com/EBI-Metagenomics/EukCC) | Estimate completeness and contamination of microbial-eukaryote bins. |
| `eukaryotic-metagenomics` | — | Route eukaryotic contig separation, gene prediction, binning, QC, taxonomy, and abundance. |
| `nf-core-taxprofiler` | [nf-core/taxprofiler](https://github.com/nf-core/taxprofiler) | Versioned multi-profiler Nextflow workflow for taxonomic classification. |

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
| `amrfinderplus` | [AMRFinderPlus](https://github.com/ncbi/amr) | Curated acquired ARG, mutation, stress, and selected virulence calls with NCBI databases. |
| `args-oap` | [ARGs-OAP](https://github.com/xinehc/args_oap) | Environmental read-based SARG profiling and normalized ARG quantification. |
| `pathofact` | [PathoFact 2.0](https://gitlab.com/uniluxembourg/lcsb/systems-ecology/pathofact2) | Integrated ARG, virulence, toxin, BGC, and geNomad context workflow. |
| `barrnap` | [barrnap](https://github.com/tseemann/barrnap) | Basic rapid ribosomal RNA predictor for genomes. |
| `biobakery-databases` | [biobakery-databases](https://github.com/biobakery/biobakery) | Install and pin bioBakery reference databases for MetaPhlAn and HUMAnN (ChocoPhlAn markers, UniRef gene families, MetaCyc pathways, utility mapping). |
| `metatranscriptomics` | — | Route microbial RNA QC, rRNA/host depletion, quantification, function, and DNA-aware interpretation. |
| `pangenome-analysis` | — | Route annotation-harmonized bacterial pangenome construction, QC, association, and phylogeny. |
| `panaroo` | [Panaroo](https://github.com/gtonkinhill/panaroo) | Graph-based bacterial pangenome inference with annotation-error correction. |
| `ppanggolin` | [PPanGGOLiN](https://github.com/labgem/PPanGGOLiN) | Partitioned pangenomes and persistent/shell/cloud gene-family analysis. |
| `community-metabolic-modeling` | — | Route genome-scale reconstruction, media definition, community simulation, and validation. |
| `carveme` | [CarveMe](https://github.com/cdanielmachado/carveme) | Reconstruct and gap-fill genome-scale metabolic models. |
| `micom` | [MICOM](https://github.com/micom-dev/micom) | Build abundance-weighted microbial community models and infer exchanges. |

## 7. Microbial mining

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `microbial-mining` | — | Route mining: BGCs, AMR, MGEs, element cycling, defense, QS, metabolism. |
| `resistome-analysis` | — | Separate ARG detection, quantification, physical context, host, and phenotype evidence. |
| `mobilome-analysis` | — | Route plasmid/virus/ICE/integron discovery, boundaries, typing, cargo, and hosts. |
| `arg-mge-host-linkage` | — | Grade ARG–MGE–host evidence from co-occurrence through molecule/experimental support. |
| `horizontal-gene-transfer` | — | Choose HGT methods by evolutionary scale and audit donor/direction uncertainty. |
| `antismash` | [antismash](https://github.com/antismash/antismash) | Detect and annotate biosynthetic gene clusters (BGCs) on genomes and MAGs. |
| `bigscape` | [bigscape](https://github.com/medema-group/BiG-SCAPE) | Cluster and compare biosynthetic gene clusters across genomes with BiG-SCAPE. |
| `genomad` | [genomad](https://github.com/apcamargo/genomad) | Identify plasmids, viruses, and other mobile genetic elements. |
| `virsorter2` | [virsorter2](https://github.com/jiarong/VirSorter2) | Viral sequence identification from metagenomic assemblies. |
| `checkv` | [checkv](https://bitbucket.org/berkeleylab/checkv) | Quality assessment of metagenome-assembled viral genomes. |
| `vcontact` | [vcontact](https://bitbucket.org/MAVERICLab/vcontact3) | vConTACT2/3 gene-sharing / ML hierarchical virus taxonomy. |
| `mobileog` | [mobileOG-db](https://github.com/clb21565/mobileOG-db) | Annotate MGE life-cycle protein families (mobileOG-db). |
| `isescan` | [ISEScan](https://github.com/xiezhq/ISEScan) | Insertion sequence (IS) element annotation. |
| `integronfinder` | [Integron_Finder](https://github.com/gem-pasteur/Integron_Finder) | Detect integrons and gene cassettes. |
| `mob-suite` | [mob-suite](https://github.com/phac-nml/mob-suite) | Plasmid reconstruction and MOB/replicon typing. |
| `plasmaag` | [plasmaag](https://github.com/RasmussenLab/PlasMAAG) | Plasmid and organism reconstruction via assembly–alignment graphs. |
| `plasx` | [PlasX](https://github.com/michaelkyu/PlasX) | Classify plasmid-like contigs from compatible gene-family architecture. |
| `mobmess` | [MobMess](https://github.com/michaelkyu/MobMess) | Cluster plasmids and infer sequence containment/backbone/compound systems. |
| `cge-finders` | — | Route CGE Finder screens (plasmid / AMR / virulence / MGE). |
| `plasmidfinder` | [PlasmidFinder](https://github.com/genomicepidemiology/plasmidfinder) | CGE replicon / plasmid typing. |
| `pmlst` | [pmlst](https://github.com/ssi-dk/pmlst) | Plasmid multilocus sequence typing (pMLST schemes). |
| `mlst` | [mlst](https://github.com/tseemann/mlst) | Chromosomal PubMLST sequence typing. |
| `resfinder` | [ResFinder](https://github.com/genomicepidemiology/resfinder) | CGE acquired AMR genes (± PointFinder / DisinFinder). |
| `pointfinder` | [pointfinder_db](https://bitbucket.org/genomicepidemiology/pointfinder_db) | Chromosomal AMR point mutations (via ResFinder/staramr). |
| `disinfinder` | [disinfinder_db](https://bitbucket.org/genomicepidemiology/disinfinder_db) | Disinfectant / biocide resistance genes (via ResFinder). |
| `virulencefinder` | [VirulenceFinder](https://bitbucket.org/genomicepidemiology/virulencefinder) | CGE virulence gene markers (supported species). |
| `mobileelementfinder` | [MobileElementFinder](https://pypi.org/project/MobileElementFinder/) | Named MGEs (IS/Tn/ICE/IME/…). |
| `staramr` | [staramr](https://github.com/phac-nml/staramr) | Combined ResFinder + PointFinder + PlasmidFinder scan. |
| `abricate` | [ABRicate](https://github.com/tseemann/abricate) | Multi-DB mass screen (ResFinder/CARD/VFDB/PlasmidFinder/…). |
| `macrel` | [macrel](https://github.com/BigDataBiology/macrel) | Screen genomes and metagenomes for antimicrobial peptides (AMPs). |
| `element-cycling` | — | Route C/N/S/Fe/P/H₂/CH₄ elemental cycling annotation. |
| `metabolic` | [METABOLIC](https://github.com/AnantharamanLab/METABOLIC) | Multi-element biogeochemical trait profiling (C/N/S/…). |
| `mebs` | [MEBS](https://github.com/valdeanda/mebs) | Entropy scores for S (and N/O/CH₄/Fe) cycle machinery. |
| `fegenie` | [FeGenie](https://github.com/Arkadiy-Garber/FeGenie) | Iron genes, siderophores, Fe redox, magnetosome neighborhoods. |
| `dom-biosurfactant` | — | Route DOM / glycan, biosurfactant, and HC/plastic biodegradation. |
| `hadeg` | [HADEG](https://github.com/jarojasva/HADEG) | Curated HC/plastic degradation and biosurfactant genes. |
| `biosurfdb` | [BioSurfDB](https://www.biosurfdb.org/) | Biosurfactant and biodegradation portal / pathways. |
| `dram` | [dram](https://github.com/WrightonLabCSU/DRAM) | Distill microbial metabolism annotations for MAGs/genomes. |
| `dbcan` | [dbcan](https://github.com/linnabrown/run_dbcan) | CAZymes + glycan substrate / CGC prediction (DOM polymers). |
| `gapseq` | [gapseq](https://github.com/jotech/gapseq) | Predict pathways and reconstruct genome-scale metabolic models. |
| `deeparg` | [deeparg](https://github.com/gaarangoa/DeepARG) | Deep-learning prediction of antibiotic resistance genes. |
| `defensefinder` | [defensefinder](https://github.com/mdmparis/defense-finder) | Detect anti-phage defense systems in prokaryotic genomes. |
| `padloc` | [PADLOC](https://github.com/padlocbio/padloc) | Prokaryotic antiviral defence locator (HMM + synteny). |
| `qsap` | [QSAP](https://github.com/chunxiao-dcx/QSAP) | Quorum-sensing related gene annotation (QSP database). |
| `virome-analysis` | — | Route viral discovery, quality control, vOTU construction, abundance, taxonomy, and host evidence. |
| `votu-workflow` | [CheckV utilities](https://bitbucket.org/berkeleylab/checkv/) | Build quality-gated viral operational taxonomic units using 95% ANI and 85% aligned fraction. |
| `vibrant` | [VIBRANT](https://github.com/AnantharamanLab/VIBRANT) | Legacy viral recovery, quality/category summaries, and auxiliary-metabolic-gene candidates. |
| `iphop` | [iPHoP](https://github.com/simroux/iphop) | Integrate multiple signals to predict prokaryotic hosts of phages. |
| `viralcc` | [ViralCC](https://github.com/dyxstat/ViralCC) | Bin viral contigs and inspect exploratory virus–host meta-Hi-C links. |
| `spacepharer` | [SpacePHARER](https://github.com/soedinglab/spacepharer) | Predict phage hosts from aggregated CRISPR spacer evidence with FDR controls. |
| `metachip` | [MetaCHIP2](https://github.com/songweizhi/MetaCHIP2) | Detect candidate HGTs with best-match and phylogenetic reconciliation. |
| `waafle` | [WAAFLE](https://github.com/biobakery/waafle) | Detect taxonomic LGT mosaics on metagenomic contigs with junction QC. |
| `hgtector` | [HGTector2](https://github.com/qiyunlab/HGTector) | Find taxonomically partitioned homology outliers as putative acquired genes. |

## Strain / microdiversity

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `instrain` | [instrain](https://github.com/MrOlm/inStrain) | Strain-level microdiversity and shared-strain detection from metagenomes. |
| `strain-resolved-analysis` | — | Route marker phylogenies, cohort SNVs, within-population diversity, and strain sharing. |
| `strainphlan` | [StrainPhlAn](https://github.com/biobakery/MetaPhlAn) | Reconstruct marker-based within-species strain phylogenies. |
| `metasnv` | [metaSNV](https://github.com/metasnv-tool/metaSNV) | Call and summarize population SNVs across metagenomic cohorts. |
| `midas2` | [MIDAS2](https://github.com/pollardlab/MIDAS) | Database-conditioned species, SNV, and pangenome gene-content profiling. |
| `strainge` | [StrainGE](https://github.com/broadinstitute/StrainGE) | Low-abundance strain reference search and StrainGR variant/gap comparison. |
| `strainfacts` | [StrainFacts](https://github.com/bsmith89/StrainFacts) | Jointly deconvolve latent strain genotypes and abundances from metagenotypes. |
| `strain-transmission` | — | Grade strain sharing and transmission with callability, mixture, background, and epidemiology. |
| `poppunk` | [PopPUNK](https://github.com/bacpop/PopPUNK) | Core/accessory k-mer population structure and validated query assignment. |
| `gubbins` | [Gubbins](https://github.com/nickjcroucher/gubbins) | Recombination-aware bacterial phylogeny from whole-genome alignments. |
| `transphylo` | [TransPhylo](https://github.com/xavierdidelot/TransPhylo) | Infer posterior transmission trees and unsampled intermediates from dated phylogenies. |

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

## Research analysis (stats · figures · reports · workflows)

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `research-analysis` | — | Route QC reports, diversity/figures, DA, networks, and workflow managers. |
| `visualization` | — | Stage-wise figure checklist. |
| `microeco` | [microeco](https://github.com/ChiLiubio/microeco) | R package for microbiome diversity, plots, DA, and networks. |
| `phyloseq` | [phyloseq](https://github.com/joey711/phyloseq) | Bioconductor microbiome data class and ggplot2 analysis. |
| `maaslin2` | [Maaslin2](https://github.com/biobakery/Maaslin2) | Multivariable meta-omic associations (MaAsLin2/3). |
| `ancombc` | [ANCOMBC](https://github.com/FrederickHuangLin/ANCOMBC) | Compositional DA with sampling-fraction bias correction. |
| `lefse` | [LEfSe](https://github.com/SegataLab/lefse) | LDA effect-size biomarker discovery. |
| `stamp` | [STAMP](https://github.com/dparks1134/STAMP) | GUI statistical analysis of taxonomic/functional profiles. |
| `sparcc` | [SparCC](https://bitbucket.org/yonatanf/sparcc) | Compositional correlation networks. |
| `spieceasi` | [SpiecEasi](https://github.com/zdk123/SpiecEasi) | Sparse compositionally robust association networks. |
| `absolute-abundance` | — | Convert relative profiles to calibrated load-aware quantities with spike-ins, qPCR, flow cytometry, or mass. |
| `permanova` | [vegan](https://github.com/vegandevs/vegan) | PERMANOVA with dispersion checks and design-restricted permutations. |
| `aldex2` | [ALDEx2](https://bioconductor.org/packages/ALDEx2/) | Monte Carlo CLR-based compositional differential abundance and effect sizes. |
| `corncob` | [corncob](https://github.com/statdivlab/corncob) | Beta-binomial differential abundance and dispersion modeling. |
| `netcomi` | [NetCoMi](https://github.com/stefpeschel/NetCoMi) | Construct, compare, and assess microbiome association networks. |
| `source-tracking` | — | Design source–sink analyses with FEAST and contamination-aware controls. |
| `feast` | [FEAST](https://github.com/cozygene/FEAST) | Estimate microbial source contributions to sink communities. |
| `sourcetracker2` | [SourceTracker2](https://github.com/biota/sourcetracker2) | Bayesian source–sink mixture estimation with an unknown-source component. |
| `transfer-network-analysis` | — | Validate and analyze evidence-typed ARG/MGE/host/HGT/source/strain/transmission graphs. |
| `multiqc` | [MultiQC](https://github.com/MultiQC/MultiQC) | Aggregate FastQC/mapping/QUAST logs into one HTML report. |
| `nextflow` | [Nextflow](https://github.com/nextflow-io/nextflow) | Portable containerized workflows (± nf-core). |
| `snakemake` | [Snakemake](https://github.com/snakemake/snakemake) | Rule-based reproducible workflow DAGs. |

## Report & utilities

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `research-analysis` | — | Research stats/figures routing — also under Research analysis. |
| `visualization` | — | Statistical visualization checklist — also under Research analysis. |
| `setup` | — | First-time environment and database setup for shotgun metagenomics tool skills. |


## Homology search

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `homology-search` | — | Route sequence, structure, PLM, vector-DB, and genome-warehouse search. |
| `mmseqs2` | [MMseqs2](https://github.com/soedinglab/MMseqs2) | Sequence search / clustering / contig taxonomy — also under Function. |
| `hh-suite` | [HH-suite](https://github.com/soedinglab/hh-suite) | HHblits/HHsearch HMM–HMM remote homology. |
| `plass` | [PLASS](https://github.com/soedinglab/plass) | Protein-level (and PenguiN) assembly from metagenomic reads. |
| `metaeuk` | [MetaEuk](https://github.com/soedinglab/metaeuk) | Eukaryotic gene discovery/annotation via MMseqs2. |
| `foldcomp` | [Foldcomp](https://github.com/steineggerlab/foldcomp) | Compress/index large protein structure sets. |
| `foldseek` | [Foldseek](https://github.com/steineggerlab/foldseek) | 3Di structure search, Multimer, ProstT5 — also under AI. |
| `folddisco` | [Folddisco](https://github.com/steineggerlab/folddisco) | Structural motif search — also under AI. |
| `foldmason` | [FoldMason](https://github.com/steineggerlab/foldmason) | Multiple protein structure alignment at scale. |
| `petasearch` | [Petasearch](https://github.com/steineggerlab/petasearch) | Parallelized peta-scale protein database search. |
| `erast` | [ERAST](https://github.com/TencentAILabHealthcare/ERAST) | Billion-scale vector-DB homology search (protein + nucleotide). |
| `phylign` | [Phylign](https://github.com/karel-brinda/phylign) | BLAST-like search on phylogeny-compressed microbial genome collections. |
| `lexicmap` | [LexicMap](https://github.com/shenwei356/LexicMap) | Gene/plasmid alignment vs millions of genomes — also under Mapping. |
| `plmsearch` | [PLMSearch](https://github.com/maovshao/PLMSearch) | PLM remote homology — also under AI. |
| `deepblast` | [DeepBLAST](https://github.com/flatironinstitute/deepblast) | TM-Vec + DeepBLAST — also under AI. |

## Phylogenomics / trees

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `phylogenomics` | — | Route MAG trees, GTDB placement, classical vs AI phylogeny. |
| `phylophlan` | [PhyloPhlAn](https://github.com/biobakery/phylophlan) | Marker-based phylogeny of isolates and MAGs. |
| `unicore` | [Unicore](https://github.com/steineggerlab/unicore) | Structural core-gene phylogeny with Foldseek/ProstT5. |
| `iqtree` | [IQ-TREE2](https://github.com/iqtree/iqtree2) | Maximum-likelihood trees with model selection / UFBoot. |
| `fasttree` | [FastTree](https://github.com/morgannprice/fasttree) | Fast approximate ML trees for large MSAs. |
| `lucaphylo` | [LucaPhylo](https://github.com/NickShannn/LucaPhylo) | Alignment-free hyperbolic PLM phylogenetic inference. |
| `gtdbtk` | [GTDB-Tk](https://github.com/Ecogenomics/GTDBTk) | GTDB taxonomy placement — also under Taxonomy. |

## Genome language models

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `genome-language-model` | — | Route genome language models: representation, generative, metagenomic gLM2. |
| `omg` | [OMG](https://github.com/TattaBio/OMG) | Open MetaGenomic corpus + gLM2 mixed-modality genome LM. |
| `nucleotide-transformer` | [nucleotide-transformer](https://github.com/instadeepai/nucleotide-transformer) | InstaDeep NT family including NTv3 multi-species foundation model. |
| `dnabert2` | [DNABERT_2](https://github.com/MAGICS-LAB/DNABERT_2) | Efficient multi-species genome LM + GUE benchmark. |
| `caduceus` | [Caduceus](https://github.com/kuleshov-group/caduceus) | Bi-directional equivariant long-range DNA language model. |
| `evo2` | [Evo 2](https://github.com/ArcInstitute/evo2) | Long-context DNA LM for modeling/design across all domains of life. |

## Protein language models

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `protein-language-model` | — | Route protein language models: ESM, ESMC, SaProt, ProstT5, PLM search. |
| `esm` | [ESM](https://github.com/facebookresearch/esm) | ESM-2 family embeddings; ESMFold / ESM Atlas context. |
| `esmc` | [evolutionaryscale/esm](https://github.com/evolutionaryscale/esm) | ESM C / Cambrian next-gen protein representation models. |
| `saprot` | [SaProt](https://github.com/westlake-repl/SaProt) | Westlake structure-aware AA+3Di protein LM (ICLR 2024). |
| `prostt5` | [ProstT5](https://github.com/mheinzinger/ProstT5) | AA ↔ Foldseek 3Di bilingual PLM (from ProtT5). |
| `plmsearch` | [PLMSearch](https://github.com/maovshao/PLMSearch) | PLM embeddings for fast remote homology protein search. |
| `deepblast` | [DeepBLAST](https://github.com/flatironinstitute/deepblast) | TM-Vec + DeepBLAST remote homology and structural alignment from sequence. |

## AI / language models & structure search

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `metagenomics-llm` | — | Route genome/protein LMs and Steinegger structure/sequence search. |
| `genome-language-model` | — | Genome language model routing — also under Genome language models. |
| `protein-language-model` | — | Protein language model routing — also under Protein language models. |
| `omg` | [OMG](https://github.com/TattaBio/OMG) | Open MetaGenomic corpus + gLM2 — also under Genome language models. |
| `mmseqs2` | [MMseqs2](https://github.com/soedinglab/MMseqs2) | Sequence search, Linclust NR, contig taxonomy — also under Function. |
| `foldseek` | [Foldseek](https://github.com/steineggerlab/foldseek) | Ultrafast 3Di structure search, clustering, Foldseek-Multimer, ProstT5. |
| `folddisco` | [Folddisco](https://github.com/steineggerlab/folddisco) | Fast discontinuous structural motif search (AFDB/PDB/ESM30). |
| `plmsearch` | [PLMSearch](https://github.com/maovshao/PLMSearch) | PLM remote homology — also under Protein language models. |
| `deepblast` | [DeepBLAST](https://github.com/flatironinstitute/deepblast) | TM-Vec + DeepBLAST — also under Protein language models. |
| `spacedust` | [Spacedust](https://github.com/soedinglab/Spacedust) | De novo conserved gene clusters via Foldseek-aware neighborhood discovery. |
| `alphagem` | [AlphaGEM](https://github.com/hongzhonglu/AlphaGEM) | GEMs with structure alignment and DL dark-metabolism mining. |

## Orchestration

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `tool-selection` | — | Choose shotgun tools by stage through research analysis (stats/figures). |
| `metagenomics-workflow` | — | End-to-end shotgun path including mining and research-analysis delivery. |
| `study-design` | — | Study design for shotgun metagenomics across QC, assembly, binning, annotation, and reporting. |
| `homology-search` | — | Route all homology/search paradigms (also under Homology search). |
| `phylogenomics` | — | Route phylogeny / evolutionary analyses (also under Phylogenomics). |
| `element-cycling` | — | Route elemental / biogeochemical cycling (also under Microbial mining). |
| `dom-biosurfactant` | — | Route DOM / biosurfactant / HC biodegradation (also under Microbial mining). |
| `cge-finders` | — | Route CGE Finder suite (also under Microbial mining). |
| `research-analysis` | — | Route stats / figures / networks / workflow managers (also under Research analysis). |
| `genome-language-model` | — | Route genome language models (also under Genome language models). |
| `protein-language-model` | — | Route protein language models (also under Protein language models). |
| `metagenomics-llm` | — | Route LMs and Foldseek/MMseqs structure–sequence search (also under AI). |

## Other

| Skill | Upstream | Purpose |
|-------|----------|---------|
| `busco` | [BUSCO](https://gitlab.com/ezlab/busco) | Ortholog-based assembly/genome completeness (eukaryote-oriented; use CheckM2 for prokaryotic MAGs). |

---

## See also

- [Standard pipeline](standard-pipeline.md)
- [Tool selection](tool-selection.md)
- [Public databases](public-databases.md)
- [References](references.md)
- [Troubleshooting](troubleshooting.md)
- [Getting started](getting-started.md)
