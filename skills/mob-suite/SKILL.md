---
name: mob-suite
description: >
  MOB-suite — plasmid reconstruction and typing from draft assemblies (replicon,
  relaxase/MOB type, mate-pair, transferability, mash clusters). Use for plasmid
  compatibility / MOB typing and plasmid contig binning beyond geNomad scores. Route via
  microbial-mining; pair with genomad, plasmaag, mobileog, rgi.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MOB-suite, plasmid, MOB, replicon, incompatibility, MGE, typing"
  metagenomics.upstream: "https://github.com/phac-nml/mob-suite"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "3.1.9"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "MOB-recon/MOB-typer CLIs reviewed; not executed here"
---

# MOB-suite

Upstream: [phac-nml/mob-suite](https://github.com/phac-nml/mob-suite)

## Citation

Robertson, J. & Nash, J. H. E. MOB-suite: software tools for clustering,
reconstruction and typing of plasmids from draft assemblies. *Microb. Genom.*
**4**, e000206 (2018). https://doi.org/10.1099/mgen.0.000206

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MOB-suite types plasmids by **replicon** and **MOB/relaxase** markers and can
reconstruct plasmid clusters from draft assemblies — useful for
**compatibility / transfer** context (Inc/MOB-style interpretation as provided
by the tool’s databases). Complements `genomad` (detection) and `plasmaag`
(multi-sample plasmid MAGs).

Typing ≠ phenotypic incompatibility assay. Pin MOB-suite DB release.

## How to run

```bash
set -euo pipefail
DB=${MOB_SUITE_DB:?set MOB_SUITE_DB to an initialized pinned database}
[[ -s assembly.fasta && -d "$DB" ]] || exit 2
mob_recon --infile assembly.fasta --outdir mob_out \
  --database_directory "$DB"
test -s mob_out/contig_report.txt
test -s mob_out/mobtyper_results.txt
# For an independently recovered plasmid sequence:
[[ -s plasmid.fasta ]] || exit 2
mob_typer --infile plasmid.fasta --out_file mob_typer.tsv \
  --database_directory "$DB"
test -s mob_typer.tsv
```

Initialize a dedicated database once with `mob_init --database_directory "$MOB_SUITE_DB"`, then freeze its manifest/checksums. Use a new output directory after changing assembly or database.

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
