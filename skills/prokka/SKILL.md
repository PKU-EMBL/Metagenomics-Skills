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

Prokka wraps Prodigal + feature predictors into GenBank/GFF — convenient for
**per-genome** annotation of isolates/MAGs. For large non-redundant gene
catalogues prefer `prodigal` → `cd-hit`/`mmseqs2` → `eggnog-mapper`.

| Need | Prefer |
|------|--------|
| Standardized bacterial annotation + modern DBs | `bakta` |
| Classic rapid GFF/GBK, minimal deps | `prokka` |
| Catalogue-scale ORFs only | `prodigal` |

Fragmented MAGs yield incomplete/wrong gene calls — filter with `mag-qc` first.

## How to run

```bash
prokka bins/bin.fa --outdir temp/prokka/${id} --prefix ${id} --cpus 8 --force
```

## Key parameters

| Flag | Notes |
|------|-------|
| `--cpus` | Threads |
| `--kingdom` | Bacteria default; set Archaea when appropriate |
| `--compliant` | NCBI-oriented outputs when submitting |

## Decision tree

```text
Annotate a bacterial/archaeal genome/MAG?
├─ Modern standardized → bakta
├─ Classic rapid GBK/GFF → prokka
└─ Only proteins for catalogue → prodigal
```

## Related skills

`bakta` · `prodigal` · `eggnog-mapper` · `barrnap` · `antismash` · `dram` ·
`tool-selection`
