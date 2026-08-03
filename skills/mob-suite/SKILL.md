---
name: mob-suite
description: >
  MOB-suite — plasmid reconstruction and typing from draft assemblies
  (replicon, relaxase/MOB type, mate-pair, transferability, mash clusters).
  Use for plasmid compatibility / MOB typing and plasmid contig binning beyond
  geNomad scores. Upstream: https://github.com/phac-nml/mob-suite. Route via
  microbial-mining; pair with genomad, plasmaag, mobileog, rgi.
license: MIT
category: analysis-tools
tags: [MOB-suite, plasmid, MOB, replicon, incompatibility, MGE, typing]
upstream: https://github.com/phac-nml/mob-suite
stage: mining
---

# MOB-suite

Upstream: [phac-nml/mob-suite](https://github.com/phac-nml/mob-suite)

## Citation

Robertson, J. & Nash, J. H. E. MOB-suite: software tools for clustering,
reconstruction and typing of plasmids from draft assemblies. *Microb. Genom.*
**4**, e000206 (2018). https://doi.org/10.1099/mgen.0.000206

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

MOB-suite types plasmids by **replicon** and **MOB/relaxase** markers and can
reconstruct plasmid clusters from draft assemblies — useful for
**compatibility / transfer** context (Inc/MOB-style interpretation as provided
by the tool’s databases). Complements `genomad` (detection) and `plasmaag`
(multi-sample plasmid MAGs).

Typing ≠ phenotypic incompatibility assay. Pin MOB-suite DB release.

## How to run

```bash
# install mob_suite; download databases per upstream
mob_recon --infile assembly.fasta --outdir mob_out
mob_typer --infile plasmid.fasta --out mob_typer.tsv
# exact subcommands: follow installed version help
```

## Decision tree

```text
Plasmid typing / reconstruction?
├─ Contig plasmid/virus flags → genomad
├─ CGE replicon typing → plasmidfinder / staramr
├─ Replicon / MOB typing → mob-suite
├─ Multi-sample plasmid MAGs → plasmaag
├─ MGE protein functions → mobileog
└─ ARG on plasmids → resfinder / rgi ∩ mob-suite/genomad
```

## Related skills

`cge-finders` · `plasmidfinder` · `staramr` · `genomad` · `plasmaag` ·
`mobileog` · `integronfinder` · `rgi` · `resfinder` · `microbial-mining` ·
`tool-selection`
