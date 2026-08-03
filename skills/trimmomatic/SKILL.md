---
name: trimmomatic
description: >
  Flexible Illumina adapter/quality trimmer. Use this skill when working with trimmomatic: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/usadellab/Trimmomatic. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'trimming']
upstream: https://github.com/usadellab/Trimmomatic
stage: qc
---

# Trimmomatic

Upstream: [Trimmomatic](https://github.com/usadellab/Trimmomatic)

## Citation

Bolger, A. M., Lohse, M. & Usadel, B. Trimmomatic: a flexible trimmer for Illumina sequence data. *Bioinformatics* **30**, 2114–2120 (2014). https://doi.org/10.1093/bioinformatics/btu170

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Prefer **fastp** for most shotgun runs (speed + JSON). Use Trimmomatic when a lab SOP already pins ILLUMINACLIP settings.

## How to run

```bash
conda install -c bioconda trimmomatic  # if packaged; else follow upstream

trimmomatic PE -threads 8 \
  seq/${id}_1.fq.gz seq/${id}_2.fq.gz \
  temp/qc/${id}_1P.fq.gz temp/qc/${id}_1U.fq.gz \
  temp/qc/${id}_2P.fq.gz temp/qc/${id}_2U.fq.gz \
  ILLUMINACLIP:adapters.fa:2:30:10 SLIDINGWINDOW:4:20 MINLEN:50
```

## Key parameters

| `ILLUMINACLIP` | adapter fasta | Required |
| `SLIDINGWINDOW` | 4:20 typical | |
| `MINLEN` | ≥50 | |

## Decision notes

- Stage: **qc** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

fastp · fastqc · kneaddata · `tool-selection` · `metagenomics-workflow`
