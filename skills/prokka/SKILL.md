---
name: prokka
description: >
  Rapid prokaryotic genome annotation (CDS/rRNA/tRNA). Use this skill when working with prokka: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/tseemann/prokka. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['annotation', 'orf', 'prokaryote']
upstream: https://github.com/tseemann/prokka
stage: function
---

# Prokka

Upstream: [Prokka](https://github.com/tseemann/prokka)

## Citation

Seemann, T. Prokka: rapid prokaryotic genome annotation. *Bioinformatics* **30**, 2068–2069 (2014). https://doi.org/10.1093/bioinformatics/btu153

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Convenient MAG/isolate annotator wrapping Prodigal + databases. For large gene catalogues prefer Prodigal→CD-HIT→eggNOG; use Prokka for per-genome GenBank/GFF.

## How to run

```bash
conda install -c bioconda prokka  # if packaged; else follow upstream

prokka bins/bin.fa --outdir temp/prokka/${id} --prefix ${id} --cpus 8 --force
```

## Key parameters

| `--cpus` | threads | |
| kingdom | Bacteria default | |

## Decision notes

- Stage: **function** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

prodigal · eggnog-mapper · barrnap · `tool-selection` · `metagenomics-workflow`
