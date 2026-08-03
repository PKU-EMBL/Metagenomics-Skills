---
name: quast
description: >
  Assembly quality assessment (contiguity, misassemblies; metaQUAST for metagenomes). Use this skill when working with quast: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/ablab/quast. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['assembly', 'qc', 'quast']
upstream: https://github.com/ablab/quast
stage: assessment
---

# QUAST / metaQUAST

Upstream: [QUAST / metaQUAST](https://github.com/ablab/quast)

## Citation

Mikheenko, A., Saveliev, V. & Gurevich, A. MetaQUAST: evaluation of metagenome assemblies. *Bioinformatics* **32**, 1088–1090 (2016). https://doi.org/10.1093/bioinformatics/btv697

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Run after assembly **before** binning to catch fragmented/misassembled contigs. metaQUAST when references exist; otherwise QUAST stats only.

## How to run

```bash
conda install -c bioconda quast  # if packaged; else follow upstream

metaquast.py contigs.fa -o temp/quast -t 16
# or quast.py for generic stats without refs
```

## Key parameters

| metaQUAST | needs refs optional | |
| N50/L50 | report | |

## Decision notes

- Stage: **assessment** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

megahit · metaspades · metaflye · mag-qc · `tool-selection` · `metagenomics-workflow`
