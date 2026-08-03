---
name: sra-ena
description: >
  Fetch and cite public shotgun metagenomic reads from NCBI SRA and EBI ENA.
  Use this skill when: (1) Downloading public metagenomes by SRR/ERR/DRR,
  (2) Resolving BioProject/Study accessions, (3) Choosing fasterq-dump vs
  ena-ftp / Aspera, (4) Building manifests for reanalysis. Upstream:
  https://github.com/ncbi/sra-tools and https://www.ebi.ac.uk/ena.
  For analysed microbiome studies and MAG catalogues, use mgnify.
  For database routing, use public-databases.
license: MIT
category: utilities
tags: [database, SRA, ENA, download, reanalysis]
upstream: https://github.com/ncbi/sra-tools
---

# NCBI SRA / EBI ENA

Upstream: [ncbi/sra-tools](https://github.com/ncbi/sra-tools) ·
ENA: https://www.ebi.ac.uk/ena ·
NCBI SRA: https://www.ncbi.nlm.nih.gov/sra

## Analytical thinking

SRA/ENA hold **raw (or submitted) sequencing data**, not polished community
tables. Reanalysis still requires your own QC (`fastp`, `kneaddata`) — public
“clean” claims are not transferable without provenance.

Prefer ENA FTP/Aspera for large European-hosted studies when NCBI is slow;
prefer `fasterq-dump` when you already live in the SRA Toolkit ecosystem.
Always map **Study / BioProject → Sample → Run** before bulk download so PE
pairs and metadata stay aligned.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Accession | SRR/ERR/DRR or BioProject | Manifest TSV with sample IDs |
| Tooling | `prefetch` + `fasterq-dump` **or** `wget`/`curl` ENA FTP | `ascp` for large cohorts |
| Disk | ~2–3× compressed run size | Separate `seq/public/` tree |

## How to run (SRA Toolkit)

```bash
conda install -c bioconda sra-tools

# Resolve & stage
prefetch SRR000001

# Convert to FASTQ (PE-aware)
fasterq-dump --split-files --threads 8 -O seq/public SRR000001
gzip seq/public/SRR000001_*.fastq
```

## How to run (ENA FTP pattern)

```bash
# Look up download links via ENA browser/API for the ERR/DRR accession, then:
wget -c -P seq/public \
  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/.../ERR000001_1.fastq.gz \
  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/.../ERR000001_2.fastq.gz
```

Use the ENA browser or API to resolve the exact FTP path; do not invent paths.

## Key metadata to archive

| Field | Why |
|-------|-----|
| Run accession | Primary download key |
| BioSample / Sample | Biological unit |
| BioProject / Study | Cohort identity |
| Instrument / layout | PE vs SE; chemistry |
| Spot/bases | Depth sanity check |
| Download date + MD5 | Provenance |

## Decision tree

```text
Public data needed?
├─ Raw reads for reanalysis → sra-ena
├─ Pre-analysed MGnify study / biome MAG catalogue → mgnify
└─ Reference taxonomy genomes → gtdb
```

## Verify

```bash
seqkit stats seq/public/*_{1,2}.fastq.gz
# Confirm R1/R2 read counts match before KneadData
```

## Related skills

`public-databases` · `mgnify` · `study-design` · `fastp` · `kneaddata` · `setup`
