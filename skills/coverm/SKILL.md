---
name: coverm
description: >
  Calculate coverage/relative abundance of genomes or contigs. Use this skill when working with coverm: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/wwood/CoverM. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['abundance', 'MAG', 'coverage']
upstream: https://github.com/wwood/CoverM
---

# CoverM

Upstream: [wwood/CoverM](https://github.com/wwood/CoverM)

## Citation

Aroney, S. T. N. *et al.* CoverM: read alignment statistics for metagenomics. *Bioinformatics* **41**, btaf147 (2025). https://doi.org/10.1093/bioinformatics/btaf147

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

CoverM estimates how reads recruit to dereplicated genomes. Use the same
dehosted reads that define biological samples. Relative abundance ≠ absolute
load. Merge per-sample outputs carefully (headers differ by CoverM version).

## How to run

```bash
coverm genome --coupled ${id}_1.fastq ${id}_2.fastq \
  --genome-fasta-directory drep95/dereplicated_genomes/ -x fa \
  -t 8 -o temp/coverm/${id}.txt
```

## Related skills

`drep` · `gtdbtk` · `visualization`

