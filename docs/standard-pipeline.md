# Standard pipeline

Shotgun metagenomics stages — not a MAG-first workflow.

```text
1. QC                 fastp → kneaddata  (± fastqc / cutadapt / trimmomatic)
2. Assembly           megahit | metaspades | metaflye | metamdbg
3. Mapping            bowtie2 | bwa | bwa-mem2 | strobealign | minimap2
                        → samtools → (coverm depths)
4. Binning            single: metabat2 / maxbin2 / concoct / semibin2 / vamb
                        ensemble: basalt ★ | metawrap | dastool
                        → drep → coverm → checkm2 / gunc / mag-qc
5. Taxonomic annot.   reads: metaphlan | kraken2+bracken | motus | sylph | kaiju
                      genomes: gtdbtk (+ gtdb / mgnify)
6. Functional annot.  reads: humann
                      genes/genomes: prodigal|bakta|prokka → cd-hit|mmseqs2
                                    → salmon → eggnog-mapper / diamond (± rgi)
7. Microbial mining   BGCs: antismash
                      AMR: rgi / deeparg
                      MGE/virus: genomad / virsorter2 → checkv
                      AMP: macrel
                      metabolism: dram / gapseq
                      defense: defensefinder
                      (route via microbial-mining)
```

Public indexes (`public-databases`, `sra-ena`, `mgnify`, `gtdb`,
`biobakery-databases`) sit beside stages.

## Stage thinking

### 1–4
QC → assembly → mapping (coverage) → binning as usual. Bins become MAGs only
after completeness/contamination filters.

### 5–6
Taxonomy and function are separate claim layers (reads vs genomes).

### 7. Microbial mining
Discovery of **elements** in contigs/genomes: natural-product BGCs, resistome,
plasmids/viruses, AMPs, metabolic potential, defense systems. Computational hits
are hypotheses — not validated compounds, phenotypes, or complete phages unless
QC says so (`checkv`, experimental follow-up).

## Skill map by stage

| Stage | Skills (examples) |
|-------|-------------------|
| Design/setup | `study-design`, `setup`, `public-databases` |
| 1 QC | `fastp`, `kneaddata`, `fastqc`, `cutadapt`, `trimmomatic` |
| 2 Assembly | `megahit`, `metaspades`, `metaflye`, `metamdbg`, `quast` |
| 3 Mapping | `bowtie2`, `bwa`, `bwa-mem2`, `strobealign`, `minimap2`, `samtools`, `bbmap`, `diamond` |
| 4 Binning | `metabat2`, `maxbin2`, `concoct`, `semibin2`, `vamb`, `basalt`, `metawrap`, `dastool`, `drep`, `coverm`, `checkm2`, `gunc`, `mag-qc` |
| 5 Taxonomy | `metaphlan`, `kraken2`, `bracken`, `motus`, `sylph`, `kaiju`, `gtdbtk`, `gtdb`, `mgnify` |
| 6 Function | `humann`, `prodigal`, `prokka`, `bakta`, `cd-hit`, `mmseqs2`, `salmon`, `eggnog-mapper`, `rgi`, `barrnap` |
| 7 Mining | `microbial-mining`, `antismash`, `genomad`, `virsorter2`, `checkv`, `macrel`, `dram`, `gapseq`, `deeparg`, `defensefinder` |
| Strain | `instrain` |
| Report | `visualization` |
| Routing | `tool-selection`, `metagenomics-workflow` |
