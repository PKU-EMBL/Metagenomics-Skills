---
name: abricate
description: >
  ABRicate — mass screening of contigs for AMR/virulence/plasmid markers
  against bundled databases (ResFinder, CARD, NCBI, VFDB, PlasmidFinder,
  EcoLI_VF, ARG-ANNOT, MEGARES, …). Use for fast multi-DB isolate or MAG
  screens and database concordance checks. Upstream:
  https://github.com/tseemann/abricate. Route via cge-finders /
  microbial-mining; official CGE CLI still via resfinder/plasmidfinder when
  phenotype mapping or PointFinder is required.
license: MIT
category: analysis-tools
tags: [ABRicate, AMR, virulence, PlasmidFinder, ResFinder, CARD, VFDB, screening]
upstream: https://github.com/tseemann/abricate
stage: mining
---

# ABRicate

Upstream: [tseemann/abricate](https://github.com/tseemann/abricate)

## Citation

Seemann, T. ABRicate: mass screening of contigs for antimicrobial and virulence
genes. https://github.com/tseemann/abricate

Also cite the **database** papers for each `--db` used (ResFinder, CARD,
PlasmidFinder, VFDB, … — see `resfinder`, `rgi`, `plasmidfinder`,
`virulencefinder`).

See also [docs/references.md](../../docs/references.md) and `cge-finders`.

## Analytical thinking

ABRicate is a **BLASTN mass-screen wrapper** over multiple curated gene DBs.
Ideal for: (1) quick multi-DB presence/absence, (2) cross-checking ResFinder vs
CARD vs NCBI AMRFinder-style sets, (3) plasmid replicon + virulence gene panels
on many assemblies.

Does **not** replace PointFinder chromosomal SNPs, ResFinder phenotype
summaries, or CARD protein models (`rgi`). Thresholds (%ID / coverage) drive
sensitivity — pin them in Methods. Metagenome contigs: expect fragmented hits.

## How to run

```bash
mamba install -c bioconda -c conda-forge abricate
abricate --list                    # available DBs
abricate --db resfinder assembly.fasta > resfinder.tsv
abricate --db plasmidfinder assembly.fasta > plasmidfinder.tsv
abricate --db vfdb assembly.fasta > vfdb.tsv
abricate --summary *.tsv > summary.tsv
# update DBs periodically: abricate --setupdb / upstream instructions
```

## Decision tree

```text
Multi-DB gene screen on assemblies?
├─ Fast concordance / batch TSV → abricate
├─ CGE ResFinder + phenotype / PointFinder → resfinder (± pointfinder)
├─ CGE DisinFinder → disinfinder via resfinder
├─ CARD protein models → rgi
├─ Official PlasmidFinder CLI → plasmidfinder
└─ Plasmid ST schemes → pmlst
```

## Related skills

`cge-finders` · `resfinder` · `plasmidfinder` · `disinfinder` ·
`virulencefinder` · `staramr` · `rgi` · `pmlst` · `mlst` ·
`microbial-mining` · `tool-selection`
