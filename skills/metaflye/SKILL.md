---
name: metaflye
description: >
  Long-read metagenome assembly with Flye/metaFlye. Use this skill when working with metaflye: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/fenderglass/Flye. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['assembly', 'long-read']
upstream: https://github.com/fenderglass/Flye
stage: assembly
---

# metaFlye

Upstream: [metaFlye](https://github.com/fenderglass/Flye)

## Citation

Kolmogorov, M. *et al.* metaFlye: scalable long-read metagenome assembly using repeat graphs. *Nat. Methods* **17**, 1103–1110 (2020). https://doi.org/10.1038/s41592-020-00971-x

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Primary long-read metagenome assembler for noisy ONT/PacBio CLR. For HiFi prefer metaMDBG/hifiasm-meta. Still map reads back for binning.

## How to run

```bash
conda install -c bioconda flye  # if packaged; else follow upstream

flye --meta --nano-raw reads.fastq.gz --out-dir temp/asm/flye -t 32
# or --pacbio-raw / --nano-hq per chemistry
```

## Key parameters

| `--meta` | metagenome mode | Required |
| read type flag | match chemistry | |

## Decision notes

- Stage: **assembly** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

minimap2 · metamdbg · megahit · metaspades · `tool-selection` · `metagenomics-workflow`
