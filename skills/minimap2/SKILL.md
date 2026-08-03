---
name: minimap2
description: >
  Fast pairwise alignment for long reads and genome-to-genome maps. Use this skill when working with minimap2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/lh3/minimap2. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'alignment', 'long-read']
upstream: https://github.com/lh3/minimap2
stage: mapping
---

# Minimap2

Upstream: [Minimap2](https://github.com/lh3/minimap2)

## Citation

Li, H. Minimap2: pairwise alignment for nucleotide sequences. *Bioinformatics* **34**, 3094–3100 (2018). https://doi.org/10.1093/bioinformatics/bty191

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Use for ONT/PacBio→assembly (`map-ont`/`map-hifi`) and assembly polishing/scaffolding maps. Not the first choice for Illumina→contig coverage (prefer Bowtie2/BWA/strobealign).

## How to run

```bash
conda install -c bioconda minimap2  # if packaged; else follow upstream

minimap2 -ax map-ont -t 16 contigs.fa reads.fastq.gz \
  | samtools sort -@ 8 -o temp/map/lr.bam
# HiFi: -ax map-hifi
# short vs short assembly splice-unaware: -ax sr
```

## Key parameters

| `-ax map-ont` | ONT | |
| `-ax map-hifi` | PacBio HiFi | |
| `-ax sr` | short reads | OK but Bowtie2/BWA often preferred |

## Decision notes

- Stage: **mapping** (long reads / genome-to-genome)
- Prefer for ONT/PacBio→contigs and assembly polish maps; not default Illumina coverage mapper

## Related skills

bowtie2 · bwa · metaflye · metamdbg · samtools · `tool-selection` · `metagenomics-workflow`
