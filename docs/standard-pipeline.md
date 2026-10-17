# Standard pipeline

Shotgun metagenomics stages — not a MAG-first workflow. Coding agents should
follow the [inspect → plan → preflight → pilot → validate contract](agent-playbook.md)
and stop before expensive execution when required inputs are unresolved.

```text
0. Design/preflight   study-design → setup → public-databases
                      lock statistical unit, controls, batches, manifests, compute
1. QC                 short reads: fastp → kneaddata  (± fastqc / cutadapt / trimmomatic)
                      long reads: technology-appropriate QC (do not use fastp blindly)
2. Assembly           megahit | metaspades | metaflye | metamdbg  (± racon | pilon)
                      coassembly planning: binchicken (± singlem markers)
3. Mapping            strobealign | bowtie2 | bwa-mem2 | bwa | minimap2
                        → samtools → coverm depths
                      gene/plasmid vs huge genome DBs: lexicmap
4. Binning            single: metabat2 / maxbin2 / concoct / semibin2 / vamb
                             / aamb / taxvamb / comebin / metabinner / lorbin
                      ensemble: basalt ★ | metawrap | dastool
                      refine/clean: anvio / deepurify
                        → drep / skani|fastani → coverm → checkm2 / gunc / mag-qc
5. Taxonomic annot.   reads: metaphlan | singlem | kraken2+bracken | motus
                             | sylph | metabuli | kaiju
                      genomes: gtdbtk (+ gtdb / mgnify / progenomes context)
6. Functional annot.  reads: humann
                      genes/genomes: prodigal|bakta|prokka → cd-hit|mmseqs2
                                    → salmon → eggnog-mapper / diamond (± rgi)
7. Microbial mining   BGCs: antismash → bigscape
                      AMR: rgi / deeparg; isolates: resfinder / staramr / abricate
                      MGE/virus: genomad / virsorter2 → checkv → vcontact
                      plasmids: plasmaag (± genomad); CGE: plasmidfinder → pmlst
                      CGE Finders: cge-finders (VF / DisinFinder / MEF / mlst / …)
                      AMP: macrel
                      metabolism: dram / dbcan / gapseq (± vmh)
                      defense: defensefinder / padloc
                      (route via microbial-mining)
8. Research delivery  multiqc → research-analysis
                      ID/abundance validation → diversity/DA/networks → Methods/provenance
                      workflow: nextflow | snakemake
```

Public data layers (`public-databases`): raw archives (`sra-ena`), catalogues
(`mgnify`, `gtdb`, `progenomes`), tool indexes (`biobakery-databases`, …),
benchmarks (`cami`, `insilicoseq`), knowledge bases (`kegg`, `vmh`).

## Stage thinking

### 0. Design and preflight

Declare the independent biological unit, primary contrast, controls, batches,
exclusions, read technology, assembly partition, coverage matrix, compute, and
DB releases. Keep raw data immutable and capture checksums. Pilot before scaling.

### 1–4
QC → assembly → mapping (coverage) → binning. Prefer **multi-coverage** when
related samples exist. Bins become MAGs only after completeness/contamination
filters (`mag-qc`). Optional: interactive refinement (`anvio`) or decontamination
(`deepurify`).

### 5–6
Taxonomy and function are separate claim layers (reads vs genomes). Do not merge
MetaPhlAn, SingleM, Kraken, and GTDB labels unlabeled. Sequence abundance ≠
taxonomic abundance in profiler benchmarks.

### 7. Microbial mining
Discovery of **elements** in contigs/genomes. Computational hits are hypotheses —
not validated compounds, phenotypes, or complete phages unless QC says so
(`checkv`, then `vcontact` for taxonomy).

### 8. Research delivery
Join sample metadata explicitly, preserve abundance semantics, diagnose
batch/confounding, report effect sizes and uncertainty with multiplicity control,
and archive commands, versions, database releases, logs, and validation evidence.

## Skill map by stage

| Stage | Skills (examples) |
|-------|-------------------|
| 0 Design/setup | `study-design`, `setup`, `public-databases` |
| 1 QC | `fastp`, `kneaddata`, `fastqc`, `cutadapt`, `trimmomatic` |
| 2 Assembly | `megahit`, `metaspades`, `metaflye`, `metamdbg`, `racon`, `pilon`, `quast`, `binchicken`, `plass` |
| 3 Mapping | `strobealign`, `bowtie2`, `bwa`, `bwa-mem2`, `minimap2`, `samtools`, `bbmap`, `diamond`, `lexicmap`, `phylign` |
| 4 Binning | `metabat2`, `maxbin2`, `concoct`, `semibin2`, `vamb`, `aamb`, `taxvamb`, `comebin`, `metabinner`, `lorbin`, `basalt`, `metawrap`, `dastool`, `anvio`, `deepurify`, `drep`, `skani`, `fastani`, `coverm`, `checkm2`, `gunc`, `mag-qc` |
| 5 Taxonomy | `metaphlan`, `singlem`, `kraken2`, `bracken`, `motus`, `sylph`, `metabuli`, `kaiju`, `gtdbtk`, `gtdb`, `mgnify`, `phylogenomics`, `phylophlan`, `unicore`, `iqtree`, `fasttree`, `lucaphylo` |
| 6 Function | `humann`, `prodigal`, `prokka`, `bakta`, `cd-hit`, `mmseqs2`, `hh-suite`, `metaeuk`, `salmon`, `eggnog-mapper`, `rgi`, `barrnap`, `foldcomp`, `foldseek`, `foldmason`, `petasearch`, `homology-search`, `erast` |
| 7 Mining | `microbial-mining`, `antismash`, `bigscape`, `genomad`, `virsorter2`, `checkv`, `vcontact`, `mobileog`, `isescan`, `integronfinder`, `mob-suite`, `plasmaag`, `cge-finders`, `plasmidfinder`, `pmlst`, `mlst`, `resfinder`, `pointfinder`, `disinfinder`, `virulencefinder`, `mobileelementfinder`, `staramr`, `abricate`, `macrel`, `element-cycling`, `metabolic`, `mebs`, `fegenie`, `dom-biosurfactant`, `hadeg`, `biosurfdb`, `dram`, `dbcan`, `gapseq`, `vmh`, `deeparg`, `defensefinder`, `padloc`, `qsap`, `folddisco`, `spacedust` |
| Strain | `instrain` |
| Public data | `sra-ena`, `cami`, `progenomes`, `kegg`, `insilicoseq`, … |
| Report / research analysis | `research-analysis`, `visualization`, `microeco`, `phyloseq`, `maaslin2`, `ancombc`, `lefse`, `stamp`, `sparcc`, `spieceasi`, `multiqc`, `nextflow`, `snakemake` |
| Genome language models | `genome-language-model`, `omg`, `nucleotide-transformer`, `dnabert2`, `caduceus`, `evo2` |
| Protein language models | `protein-language-model`, `esm`, `esmc`, `saprot`, `prostt5`, `plmsearch`, `deepblast` |
| AI / LMs & structure search | `metagenomics-llm`, `omg`, `mmseqs2`, `foldseek`, `folddisco`, `plmsearch`, `deepblast`, `spacedust`, `alphagem` |
| Routing | `tool-selection`, `metagenomics-workflow`, `metagenomics-llm`, `genome-language-model`, `protein-language-model`, `homology-search`, `phylogenomics` |
