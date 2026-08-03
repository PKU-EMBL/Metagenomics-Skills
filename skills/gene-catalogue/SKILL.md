---
name: gene-catalogue
description: >
  Metagenome assembly and non-redundant gene catalogue construction.
  Use this skill when: (1) Assembling with MEGAHIT or metaSPAdes,
  (2) Predicting genes with Prodigal,
  (3) Clustering ORFs with cd-hit,
  (4) Quantifying genes with salmon,
  (5) Annotating with eggNOG-mapper or CARD/RGI.

  For classical MAGs, use mag-classical.
  For study design of co-assembly, use study-design.
license: MIT
category: analysis-tools
tags: [assembly, megahit, prodigal, cd-hit, salmon, eggnog]
---

# Assembly and Gene Catalogue

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Host-depleted PE | From `preprocessing` |
| RAM | 64 GB | 256 GB+ for large co-assemblies |
| Threads | 8 | 32+ |

## Recommended sequence

| Step | Default | Output |
|------|---------|--------|
| Assemble | MEGAHIT (metaSPAdes optional) | contigs FASTA |
| Evaluate | QUAST | assembly report |
| Genes | Prodigal `-p meta` | gene.fa + GFF |
| Cluster | `cd-hit-est -c 0.95 -aS 0.9 -G 0 -g 0` | NR nucleotides |
| Translate | `seqkit translate --trim` | NR proteins |
| Quantify | `salmon quant --meta` | TPM / counts |
| Function | eggNOG-mapper (DIAMOND) | COG/KO/CAZy tables |
| AMR | RGI / CARD | resistance annotations |

## Example commands

```bash
megahit -t 32 \
  -1 sample1_1.fastq,sample2_1.fastq \
  -2 sample1_2.fastq,sample2_2.fastq \
  -o temp/megahit

prodigal -i temp/megahit/final.contigs.fa \
  -d temp/prodigal/gene.fa -o temp/prodigal/gene.gff -p meta -f gff

cd-hit-est -i temp/prodigal/gene.fa -o result/NR/nucleotide.fa \
  -aS 0.9 -c 0.95 -G 0 -g 0 -T 0 -M 0
```

## Decision tree

```text
Assembly mode?
│
├─ Stratum defines contrast → assemble within stratum
├─ Related replicates, gene catalogue → co-assembly allowed in pilot
└─ Very large cohort (>30 samples / >300 Gb) → subgroup assembly
```

## Related skills

- `study-design` — whether to co-assemble
- `mag-classical` — bin contigs into MAGs
- `basalt` — refined MAG recovery from assemblies
