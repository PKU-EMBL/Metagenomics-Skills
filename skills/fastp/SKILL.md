---
name: fastp
description: >
  Ultra-fast FASTQ QC/adapter trimming for Illumina/MGI short reads. Use this skill when working with fastp: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/OpenGene/fastp. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'fastq', 'trimming']
upstream: https://github.com/OpenGene/fastp
---

# fastp

Upstream: [OpenGene/fastp](https://github.com/OpenGene/fastp)

## Citation

Chen, S., Zhou, Y., Chen, Y. & Gu, J. fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics* **34**, i884–i890 (2018). https://doi.org/10.1093/bioinformatics/bty560

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Use fastp **before** host depletion or assembly so adapter/low-quality bases do
not create false k-mers or broken PE pairs. Prefer fastp for short reads; for
ONT/PacBio use long-read QC tools (e.g. fastplong), not fastp.

Always archive HTML/JSON reports — they are the audit trail for “reads were clean”.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Illumina/MGI PE or SE FASTQ(.gz) | Phred33 |
| CPU | 4 threads | 8–16 |
| Disk | ~1–2× input for outputs | Separate `temp/qc` |

## How to run

```bash
# Bioconda
conda install -c bioconda fastp

fastp \
  -i seq/${id}_1.fq.gz -I seq/${id}_2.fq.gz \
  -o temp/qc/${id}_1.fastq -O temp/qc/${id}_2.fastq \
  -j temp/qc/${id}_fastp.json -h temp/qc/${id}_fastp.html \
  -w 8
```

## Key parameters

| Parameter | Typical | Notes |
|-----------|---------|-------|
| `-i/-I` | R1/R2 | Required for PE |
| `-o/-O` | cleaned FASTQ | Keep uncompressed only if KneadData expects it |
| `-j/-h` | JSON/HTML | Always keep |
| `-w` | 8 | Threads |
| `--detect_adapter_for_pe` | on when unsure | Auto adapter detection |

## Output

```text
temp/qc/${id}_1.fastq
temp/qc/${id}_2.fastq
temp/qc/${id}_fastp.json
temp/qc/${id}_fastp.html
```

## Decision tree

```text
Short-read shotgun?
├─ Yes → fastp
└─ Long-read only → not fastp (use long-read QC)
```

## Verify

```bash
seqkit stat temp/qc/${id}_*.fastq
grep -E 'total reads|adapter' temp/qc/${id}_fastp.json | head
```

## Related skills

`kneaddata` → next for host removal · `setup` for env install

