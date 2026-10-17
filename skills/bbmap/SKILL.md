---
name: bbmap
description: >
  Fast splice-aware aligner and BBTools suite utilities (BBMerge, etc.). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, bbtools"
  metagenomics.upstream: "https://sourceforge.net/projects/bbmap/"
  metagenomics.stage: "mapping"
---

# BBMap

Upstream: [BBMap](https://sourceforge.net/projects/bbmap/)

## Citation

Bushnell, B. BBMap: a fast, accurate, splice-aware aligner. *LBNL Report* (2014). https://escholarship.org/uc/item/1h3515gn

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Useful Swiss-army mapper/utilities; for standard metagenome coverage prefer Bowtie2/strobealign unless BBMap is already standardized in the lab.

## How to run

```bash
conda install -c conda-forge -c bioconda bbmap

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
