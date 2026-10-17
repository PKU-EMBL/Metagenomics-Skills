---
name: bwa
description: >
  Burrows–Wheeler short-read alignment (BWA-MEM) to contigs/genomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, short-read"
  metagenomics.upstream: "https://github.com/lh3/bwa"
  metagenomics.stage: "mapping"
---

# BWA / BWA-MEM

Upstream: [BWA / BWA-MEM](https://github.com/lh3/bwa)

## Citation

Li, H. & Durbin, R. Fast and accurate short read alignment with Burrows–Wheeler transform. *Bioinformatics* **25**, 1754–1760 (2009). https://doi.org/10.1093/bioinformatics/btp324

Li, H. Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM. *arXiv* (2013). https://doi.org/10.48550/arXiv.1303.3997

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classic alternative to Bowtie2 for coverage mapping. Prefer **bwa-mem2** on large cohorts when available; keep identical PE cleaned reads as used for assembly.

## How to run

```bash
conda install -c conda-forge -c bioconda bwa

bwa index contigs.fa
bwa mem -t 16 contigs.fa clean_1.fq.gz clean_2.fq.gz \
  | samtools sort -@ 8 -o temp/map/${id}.bam
samtools index temp/map/${id}.bam
```

## Key parameters

| `bwa mem -t` | threads | |
| index | `bwa index` | Once per reference |

## Decision notes

- Stage: **mapping** (short reads)
- Prefer `bwa-mem2` for speed when compatible; keep BWA when Methods require BWA-MEM
- Indexes ≠ Bowtie2 / strobealign

## Related skills

bwa-mem2 · bowtie2 · samtools · coverm · `tool-selection` · `metagenomics-workflow`
