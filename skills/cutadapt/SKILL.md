---
name: cutadapt
description: >
  Adapter/primer trimming for short and long reads. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, adapters"
  metagenomics.upstream: "https://github.com/marcelm/cutadapt"
  metagenomics.stage: "qc"
---

# Cutadapt

Upstream: [Cutadapt](https://github.com/marcelm/cutadapt)

## Citation

Martin, M. Cutadapt removes adapter sequences from high-throughput sequencing reads. *EMBnet J.* **17**, 10–12 (2011). https://doi.org/10.14806/ej.17.1.200

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Use when adapters/primers are known exactly (amplicon-like primers on shotgun libraries, custom oligos). For general Illumina shotgun QC prefer fastp.

## How to run

```bash
conda install -c conda-forge -c bioconda cutadapt

cutadapt -j 8 -a AGATCGGAAGAGC -A AGATCGGAAGAGC \
  -o temp/qc/${id}_1.fq.gz -p temp/qc/${id}_2.fq.gz \
  seq/${id}_1.fq.gz seq/${id}_2.fq.gz
```

## Key parameters

| `-a/-A` | adapters | R1/R2 |
| `-j` | threads | |

## Decision notes

- Stage: **QC** — adapter/primer trimming before host depletion / assembly
- Prefer when custom adapters or amplicon primers matter; else `fastp` often enough
- Keep trimmed PE pairing consistent for KneadData / assembly

## Related skills

fastp · trimmomatic · `tool-selection` · `metagenomics-workflow`
