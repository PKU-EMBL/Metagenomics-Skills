---
name: fastqc
description: >
  QC reports for Illumina FASTQ before/after trimming. Use this skill when working with fastqc: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/s-andrews/FastQC. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'fastq']
upstream: https://github.com/s-andrews/FastQC
stage: qc
---

# FastQC

Upstream: [FastQC](https://github.com/s-andrews/FastQC)

## Citation

Andrews, S. FastQC: a quality control tool for high throughput sequence data (2010). https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

FastQC is a **report**, not a cleaner. Use it to audit raw and cleaned reads; do trimming with fastp/cutadapt.

## How to run

```bash
conda install -c bioconda fastqc  # if packaged; else follow upstream

fastqc seq/${id}_1.fq.gz seq/${id}_2.fq.gz -o temp/qc -t 8
```

## Key parameters

| `-o` | output dir | HTML+zip reports |
| `-t` | threads | |

## Decision notes

- Stage: **QC** (report-only)
- Prefer before/after trimming for QC reports; does not modify reads
- Pair with `fastp` JSON/HTML for actionable filters

## Related skills

fastp · kneaddata · `tool-selection` · `metagenomics-workflow`
