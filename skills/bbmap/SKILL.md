---
name: bbmap
description: >
  Fast splice-aware aligner and BBTools suite utilities (BBMerge, etc.). Use this skill when working with bbmap: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://sourceforge.net/projects/bbmap/. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'alignment', 'bbtools']
upstream: https://sourceforge.net/projects/bbmap/
stage: mapping
---

# BBMap

Upstream: [BBMap](https://sourceforge.net/projects/bbmap/)

## Citation

Bushnell, B. BBMap: a fast, accurate, splice-aware aligner. *LBNL Report* (2014). https://escholarship.org/uc/item/1h3515gn

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Useful Swiss-army mapper/utilities; for standard metagenome coverage prefer Bowtie2/strobealign unless BBMap is already standardized in the lab.

## How to run

```bash
conda install -c bioconda bbmap  # if packaged; else follow upstream

bbmap.sh ref=contigs.fa in1=clean_1.fq.gz in2=clean_2.fq.gz \
  out=temp/map/${id}.bam threads=16
```

## Key parameters

| `ref=` | contigs | |
| `out=` | BAM/SAM | |

## Decision notes

- Stage: **mapping** / utilities (BBTools suite)
- Prefer for specialized BBMerge/BBDuk tasks; for Illumina→contigs coverage prefer `strobealign` / `bowtie2`

## Related skills

bowtie2 · samtools · coverm · `tool-selection` · `metagenomics-workflow`
