---
name: metabat2
description: >
  Adaptive contig binning from composition + coverage. Use this skill when working with metabat2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://bitbucket.org/berkeleylab/metabat. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'metabat']
upstream: https://bitbucket.org/berkeleylab/metabat
stage: binning
---

# MetaBAT 2

Upstream: [MetaBAT 2](https://bitbucket.org/berkeleylab/metabat)

## Citation

Kang, D. D. *et al.* MetaBAT 2: an adaptive binning algorithm for robust and efficient genome reconstruction from metagenome assemblies. *PeerJ* **7**, e7359 (2019). https://doi.org/10.7717/peerj.7359

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Core single-binner. Feed depth from `jgi_summarize_bam_contig_depths` on sorted BAMs. Ensemble with MaxBin2/CONCOCT then DAS Tool / MetaWRAP / BASALT.

## How to run

```bash
conda install -c bioconda metabat2  # if packaged; else follow upstream

jgi_summarize_bam_contig_depths --outputDepth depth.txt temp/map/*.bam
metabat2 -i contigs.fa -a depth.txt -o temp/bins/metabat/bin -t 16
```

## Key parameters

| `-a` | depth table | From BAMs |
| `-m` | min contig len | Often 1500–2500 |

## Decision notes

- Stage: **binning** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

maxbin2 · concoct · dastool · metawrap · basalt · bowtie2 · `tool-selection` · `metagenomics-workflow`
