---
name: plasmidfinder
description: >
  PlasmidFinder — CGE in silico replicon / plasmid typing from assemblies or
  reads (BLAST/KMA vs PlasmidFinder DB). Use for Inc/replicon markers on
  isolates and HQ genomes. Upstream:
  https://github.com/genomicepidemiology/plasmidfinder. Route via cge-finders /
  microbial-mining; complement with genomad, plasmaag, mob-suite.
license: MIT
category: analysis-tools
tags: [PlasmidFinder, CGE, plasmid, replicon, Inc, typing, MGE]
upstream: https://github.com/genomicepidemiology/plasmidfinder
stage: mining
---

# PlasmidFinder

Upstream: [genomicepidemiology/plasmidfinder](https://github.com/genomicepidemiology/plasmidfinder) ·
DB: [plasmidfinder_db](https://bitbucket.org/genomicepidemiology/plasmidfinder_db)

## Citation

Carattoli, A. *et al.* In Silico Detection and Typing of Plasmids using
PlasmidFinder and Plasmid Multilocus Sequence Typing. *Antimicrob. Agents
Chemother.* **58**, 3895–3903 (2014). https://doi.org/10.1128/AAC.02412-14

See also [docs/references.md](../../docs/references.md) and `cge-finders`.

## Analytical thinking

PlasmidFinder matches **replicon** sequences (Inc/rep families as represented
in the CGE DB). A hit supports plasmid **type presence**, not a complete
circular plasmid or host linkage. Database historically strong for
Enterobacterales / selected Gram+ sets — weak for open environmental plasmidomes.

Prefer `genomad` / `plasmaag` for metagenomic plasmid contig discovery;
`mob-suite` for MOB/relaxase + reconstruction; PlasmidFinder for CGE-compatible
replicon typing on isolates.

## How to run

```bash
# clone DB: plasmidfinder_db; install per upstream (pip/docker/bioconda when available)
python plasmidfinder.py -i assembly.fasta -o plasmidfinder_out \
  -p /path/to/plasmidfinder_db
# or use staramr for combined Res/Point/Plasmid DB scans
```

Exact flags vary by release — follow installed `--help` and pin DB commit/tag.

## Decision tree

```text
Plasmid claim?
├─ CGE replicon typing → plasmidfinder
├─ Combined isolate AMR+plasmid report → staramr
├─ Contig plasmid/virus scores (meta) → genomad
├─ Plasmid MAG recovery → plasmaag
├─ MOB / relaxase typing → mob-suite
└─ ARG on plasmids → resfinder / rgi ∩ plasmidfinder/genomad
```

## Related skills

`cge-finders` · `staramr` · `resfinder` · `mob-suite` · `genomad` · `plasmaag` ·
`mobileelementfinder` · `rgi` · `microbial-mining` · `tool-selection`
