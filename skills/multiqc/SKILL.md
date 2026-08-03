---
name: multiqc
description: >
  MultiQC — aggregate bioinformatics QC logs into a single interactive HTML
  report (FastQC, fastp, Bowtie2/BWA, Samtools, QUAST, …). Use after QC/mapping
  steps to audit libraries before biological statistics. Upstream:
  https://github.com/MultiQC/MultiQC. Route via research-analysis / setup.
license: MIT
category: utilities
tags: [MultiQC, QC, report, FastQC, research-analysis]
upstream: https://github.com/MultiQC/MultiQC
stage: qc
---

# MultiQC

Upstream: [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) ·
https://multiqc.info/

## Citation

Ewels, P., Magnusson, M., Lundin, S. & Käller, M. MultiQC: summarize analysis
results for multiple tools and samples in a single report. *Bioinformatics*
**32**, 3047–3048 (2016). https://doi.org/10.1093/bioinformatics/btw354

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

MultiQC is for **technical QC dashboards**, not alpha diversity or DA tests.
Point it at directories of tool logs after `fastqc` / `fastp` / mapping / QUAST.
Pin MultiQC version; module support varies by log format.

## How to run

```bash
pip install multiqc   # or conda install -c bioconda multiqc
multiqc qc_logs/ -o multiqc_report
# optional: multiqc -c multiqc_config.yaml …
```

## Decision tree

```text
Need aggregated QC HTML?
├─ Yes → multiqc
├─ Biological diversity / DA → research-analysis → microeco / maaslin2
└─ Per-tool QC only → fastqc / fastp / quast skills
```

## Related skills

`research-analysis` · `fastqc` · `fastp` · `quast` · `samtools` · `setup` ·
`visualization` · `tool-selection`
