---
name: sra-ena
description: >
  Fetch and cite public shotgun metagenomic reads from NCBI SRA and EBI ENA. Use this
  skill when: (1) Downloading public metagenomes by SRR/ERR/DRR, (2) Resolving
  BioProject/Study accessions, (3) Choosing fasterq-dump vs ena-ftp / Aspera, (4)
  Building manifests for reanalysis. For analysed microbiome studies and MAG catalogues,
  use mgnify. For database routing, use public-databases.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, SRA, ENA, download, reanalysis"
  metagenomics.upstream: "https://github.com/ncbi/sra-tools"
  metagenomics.stage: "utilities"
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

## How to run (ENA-resolved links)

```bash
set -euo pipefail
run=${1:?usage: ena-download.sh ERR_OR_DRR_ACCESSION}
mkdir -p seq/public metadata
curl -fsSLG 'https://www.ebi.ac.uk/ena/portal/api/filereport' \
  --data-urlencode "accession=$run" --data-urlencode 'result=read_run' \
  --data-urlencode 'fields=run_accession,fastq_ftp,fastq_md5' \
  --data-urlencode 'format=tsv' --data-urlencode 'download=true' \
  -o "metadata/${run}.ena.tsv"
[[ $(wc -l < "metadata/${run}.ena.tsv") -eq 2 ]] || exit 3
awk -F '\t' 'NR==2 {gsub(/;/,"\n",$2); print $2}' "metadata/${run}.ena.tsv" |
  while IFS= read -r remote; do
    [[ -n "$remote" ]] && wget -c -P seq/public "https://${remote}"
  done
find seq/public -name "${run}*.fastq.gz" -size +0c | grep -q .
```

Archive the returned MD5 field and verify each file against its position-matched checksum before analysis; an HTTP success alone is not data integrity.

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
