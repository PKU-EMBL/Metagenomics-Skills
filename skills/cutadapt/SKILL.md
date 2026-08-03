---
name: cutadapt
description: >
  Adapter/primer trimming for short and long reads. Use this skill when working with cutadapt: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/marcelm/cutadapt. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'adapters']
upstream: https://github.com/marcelm/cutadapt
stage: qc
---

# Cutadapt

Upstream: [Cutadapt](https://github.com/marcelm/cutadapt)

## Citation

Martin, M. Cutadapt removes adapter sequences from high-throughput sequencing reads. *EMBnet J.* **17**, 10–12 (2011). https://doi.org/10.14806/ej.17.1.200

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Use when adapters/primers are known exactly (amplicon-like primers on shotgun libraries, custom oligos). For general Illumina shotgun QC prefer fastp.

## How to run

```bash
conda install -c bioconda cutadapt  # if packaged; else follow upstream

cutadapt -j 8 -a AGATCGGAAGAGC -A AGATCGGAAGAGC \
  -o temp/qc/${id}_1.fq.gz -p temp/qc/${id}_2.fq.gz \
  seq/${id}_1.fq.gz seq/${id}_2.fq.gz
```

## Key parameters

| `-a/-A` | adapters | R1/R2 |
| `-j` | threads | |

## Decision notes

- Stage: **qc** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

fastp · trimmomatic · `tool-selection` · `metagenomics-workflow`
