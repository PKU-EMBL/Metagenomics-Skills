# Standard pipeline

Shotgun metagenomics stages — not a MAG-first workflow.

```text
1. QC                 fastp → kneaddata  (± fastqc / cutadapt / trimmomatic)
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
                      AMR: rgi / deeparg
                      MGE/virus: genomad / virsorter2 → checkv → vcontact
                      plasmids: plasmaag (± genomad)
                      AMP: macrel
                      metabolism: dram / dbcan / gapseq (± vmh)
                      defense: defensefinder
                      (route via microbial-mining)
```

Public data layers (`public-databases`): raw archives (`sra-ena`), catalogues
(`mgnify`, `gtdb`, `progenomes`), tool indexes (`biobakery-databases`, …),
benchmarks (`cami`, `insilicoseq`), knowledge bases (`kegg`, `vmh`).

## Stage thinking

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

## Skill map by stage

| Stage | Skills (examples) |
|-------|-------------------|
| Design/setup | `study-design`, `setup`, `public-databases` |
| 1 QC | `fastp`, `kneaddata`, `fastqc`, `cutadapt`, `trimmomatic` |
| 2 Assembly | `megahit`, `metaspades`, `metaflye`, `metamdbg`, `racon`, `pilon`, `quast`, `binchicken` |
| 3 Mapping | `strobealign`, `bowtie2`, `bwa`, `bwa-mem2`, `minimap2`, `samtools`, `bbmap`, `diamond`, `lexicmap` |
| 4 Binning | `metabat2`, `maxbin2`, `concoct`, `semibin2`, `vamb`, `aamb`, `taxvamb`, `comebin`, `metabinner`, `lorbin`, `basalt`, `metawrap`, `dastool`, `anvio`, `deepurify`, `drep`, `skani`, `fastani`, `coverm`, `checkm2`, `gunc`, `mag-qc` |
| 5 Taxonomy | `metaphlan`, `singlem`, `kraken2`, `bracken`, `motus`, `sylph`, `metabuli`, `kaiju`, `gtdbtk`, `gtdb`, `mgnify` |
| 6 Function | `humann`, `prodigal`, `prokka`, `bakta`, `cd-hit`, `mmseqs2`, `salmon`, `eggnog-mapper`, `rgi`, `barrnap` |
| 7 Mining | `microbial-mining`, `antismash`, `bigscape`, `genomad`, `virsorter2`, `checkv`, `vcontact`, `plasmaag`, `macrel`, `dram`, `dbcan`, `gapseq`, `vmh`, `deeparg`, `defensefinder` |
| Strain | `instrain` |
| Public data | `sra-ena`, `cami`, `progenomes`, `kegg`, `insilicoseq`, … |
| Report | `visualization` |
| AI / LMs | `metagenomics-llm`, `omg`, `plmsearch`, `deepblast`, `spacedust`, `alphagem` |
| Routing | `tool-selection`, `metagenomics-workflow`, `metagenomics-llm` |
