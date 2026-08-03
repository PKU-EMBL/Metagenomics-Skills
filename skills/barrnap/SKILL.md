---
name: barrnap
description: >
  Basic rapid ribosomal RNA predictor for genomes. Use this skill when working with barrnap: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/tseemann/barrnap. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['rrna', 'annotation']
upstream: https://github.com/tseemann/barrnap
stage: gene
---

# Barrnap

Upstream: [Barrnap](https://github.com/tseemann/barrnap)

## Citation

Seemann, T. Barrnap: BAsic Rapid Ribosomal RNA Predictor. https://github.com/tseemann/barrnap

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Quick rRNA loci on MAGs/isolates for QC (16S presence) and annotation. Pair with GTDB-Tk / Prokka workflows.

## How to run

```bash
conda install -c bioconda barrnap  # if packaged; else follow upstream

barrnap bins/bin.fa > temp/barrnap/${id}.gff
```

## Key parameters

| kingdom | bac/arc/euk | |

## Decision notes

- Stage: **function** (rRNA prediction)
- Prefer as a quick rRNA check on genomes/MAGs; not a substitute for full annotation (`bakta`/`prokka`)

## Related skills

prokka · gtdbtk · checkm2 · `tool-selection` · `metagenomics-workflow`
