---
name: fastqc
description: >
  QC reports for Illumina FASTQ before/after trimming. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, fastq"
  metagenomics.upstream: "https://github.com/s-andrews/FastQC"
  metagenomics.stage: "qc"
---

# FastQC

Upstream: [FastQC](https://github.com/s-andrews/FastQC)

## Citation

Andrews, S. FastQC: a quality control tool for high throughput sequence data (2010). https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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
