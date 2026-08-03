---
name: vamb
description: >
  Deep variational autoencoder binning of metagenome contigs. Use this skill when working with vamb: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/RasmussenLab/vamb. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['binning', 'vae', 'deep-learning']
upstream: https://github.com/RasmussenLab/vamb
stage: binning
---

# VAMB

Upstream: [VAMB](https://github.com/RasmussenLab/vamb)

## Citation

Nissen, J. N. *et al.* Improved metagenome binning and assembly using deep variational autoencoders. *Nat. Biotechnol.* **39**, 555–560 (2021). https://doi.org/10.1038/s41587-020-00777-4

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

DL composition+coverage binning. GPU optional. Good ensemble diversity vs MetaBAT/MaxBin; still run CheckM2 and prefer BASALT/MetaWRAP/DAS Tool for multi-binner consensus when claiming catalogues.

## How to run

```bash
conda install -c bioconda vamb  # if packaged; else follow upstream

vamb --outdir temp/bins/vamb --fasta contigs.fa --bamfiles temp/map/*.bam -p 16
```

## Key parameters

| `--bamfiles` | BAMs | Sorted |
| GPU | optional | Faster |

## Decision notes

- Stage: **binning** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

semibin2 · metabat2 · dastool · basalt · `tool-selection` · `metagenomics-workflow`
