---
name: racon
description: >
  Ultrafast consensus polishing of assemblies using mapped long (or short)
  reads. Use after long-read or hybrid assembly before binning/annotation.
  Upstream: https://github.com/lbcb-sci/racon.
license: MIT
category: analysis-tools
tags: [polish, assembly, long-read]
upstream: https://github.com/lbcb-sci/racon
stage: assembly
---

# Racon

Upstream: [lbcb-sci/racon](https://github.com/lbcb-sci/racon)

## Citation

Vaser, R., Sović, I., Nagarajan, N. & Šikić, M. Fast and accurate de novo
genome assembly from long uncorrected reads. *Genome Res.* **27**, 737–746
(2017). https://doi.org/10.1101/gr.214270.116

## Analytical thinking

Racon polishes contigs given **overlaps from mapping** (usually Minimap2 PAF).
Typical long-read loop: assemble → map reads → racon → (optional repeat). Do
not expect Racon alone to fix massive mis-assemblies; it refines consensus.

For Illumina polishing of long-read drafts, consider `pilon` / Polypolish
ecosystems as alternatives.

## How to run

```bash
conda install -c bioconda racon minimap2

minimap2 -x map-ont -t 16 assembly.fa reads.fastq.gz > temp/polish/map.paf
racon -t 16 reads.fastq.gz temp/polish/map.paf assembly.fa \
  > temp/polish/assembly.racon.fa
```

## Related skills

`minimap2` · `metaflye` · `metamdbg` · `pilon` · `quast`
