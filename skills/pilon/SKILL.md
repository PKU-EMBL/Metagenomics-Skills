---
name: pilon
description: >
  Polish genome assemblies and fix small errors using short-read BAM evidence. Use after
  mapping Illumina reads to a draft assembly (including long-read drafts).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "polish, assembly, short-read"
  metagenomics.upstream: "https://github.com/broadinstitute/pilon"
  metagenomics.stage: "assembly"
---

# Pilon

Upstream: [broadinstitute/pilon](https://github.com/broadinstitute/pilon)

## Citation

Walker, B. J. *et al.* Pilon: an integrated tool for comprehensive microbial
variant detection and genome assembly improvement. *PLoS ONE* **9**, e112963
(2014). https://doi.org/10.1371/journal.pone.0112963

## Analytical thinking

Pilon uses **short-read alignments** to correct SNPs/indels and optionally fill
gaps. Requires high-quality BAM (Bowtie2/BWA) to the draft. Over-polishing
heterogeneous metagenome contigs can erase true strain variation — prefer on
**isolate-like MAGs** or low-complexity drafts, not blindly on all community
contigs.

## How to run

```bash
conda install -c bioconda pilon bowtie2 samtools

bowtie2-build draft.fa temp/polish/draft
bowtie2 -x temp/polish/draft -1 R1.fq.gz -2 R2.fq.gz -p 16 \
  | samtools sort -@ 8 -o temp/polish/illumina.bam
samtools index temp/polish/illumina.bam

pilon --genome draft.fa --frags temp/polish/illumina.bam \
  --output draft.pilon --outdir temp/polish --threads 16
```

## Related skills

`bowtie2` · `samtools` · `racon` · `quast` · `megahit` · `metaflye`
