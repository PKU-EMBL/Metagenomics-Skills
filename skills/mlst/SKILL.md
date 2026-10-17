---
name: mlst
description: >
  mlst — chromosomal multilocus sequence typing of assemblies against PubMLST schemes
  (Torsten Seemann wrapper). Use for isolate / HQ-MAG species ST calling. Route via
  cge-finders / microbial-mining for isolate packages; plasmid ST → pmlst (different
  schemes).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MLST, PubMLST, typing, isolate, ST, epidemiology"
  metagenomics.upstream: "https://github.com/tseemann/mlst"
  metagenomics.stage: "mining"
---

# mlst

Upstream: [tseemann/mlst](https://github.com/tseemann/mlst) · schemes from
[PubMLST](https://pubmlst.org/)

## Citation

Seemann, T. mlst: scan contig files against PubMLST typing schemes.
https://github.com/tseemann/mlst

Jolley, K. A., Bray, J. E. & Maiden, M. C. J. Open-access bacterial population
genomics: BIGSdb software, the PubMLST.org website and their applications.
*Wellcome Open Res.* **3**, 124 (2018).
https://doi.org/10.12688/wellcomeopenres.14826.1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `pmlst`.

## Analytical thinking

Chromosomal **MLST** assigns a species-scheme sequence type from seven (or
scheme-defined) housekeeping loci. Auto-scheme detection can mis-assign on
novel/environmental genomes — verify species/`--scheme`. Novel alleles yield
incomplete STs.

**Not** plasmid typing (`pmlst`) and **not** ANI taxonomy (`gtdbtk` / `skani`).
Use with CGE Finders for One-Health isolate reports: species ST + resistome +
plasmids.

## How to run

```bash
mamba install -c bioconda -c conda-forge mlst
mlst assembly.fasta > mlst.tsv
mlst --scheme ecoli assembly.fasta
# update schemes per upstream / mlst --list
```

Pin `mlst` version and PubMLST scheme download date.

## Decision tree

```text
Sequence type needed?
├─ Chromosomal PubMLST ST → mlst
├─ Plasmid scheme ST → pmlst
├─ Species/taxonomy for MAGs → gtdbtk
└─ AMR / plasmids / virulence → cge-finders / abricate / rgi
```

## Related skills

`pmlst` · `cge-finders` · `abricate` · `staramr` · `plasmidfinder` ·
`gtdbtk` · `microbial-mining` · `tool-selection`
