---
name: pmlst
description: >
  pMLST — plasmid multilocus sequence typing from assemblies or reads using CGE /
  PubMLST plasmid schemes (IncI1, IncF, IncHI2, …). Use after PlasmidFinder replicon
  hits when a scheme ST is needed. Route via cge-finders / plasmidfinder /
  microbial-mining; chromosomal ST → mlst.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "pMLST, plasmid, MLST, CGE, typing, Inc, PubMLST"
  metagenomics.upstream: "https://github.com/ssi-dk/pmlst"
  metagenomics.stage: "mining"
---

# pMLST

Upstream: [ssi-dk/pmlst](https://github.com/ssi-dk/pmlst) ·
PyPI/bioconda: `pmlst_ssi` · CGE service historically at genomicepidemiology.org

## Citation

Carattoli, A. *et al.* In Silico Detection and Typing of Plasmids using
PlasmidFinder and Plasmid Multilocus Sequence Typing. *Antimicrob. Agents
Chemother.* **58**, 3895–3903 (2014). https://doi.org/10.1128/AAC.02412-14

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md), `plasmidfinder`, and
`cge-finders`.

## Analytical thinking

pMLST assigns a **plasmid sequence type** for a chosen scheme after alleles
are called. Requires selecting the correct scheme (e.g. IncI1, IncF RST, …) —
wrong scheme → nonsense ST. Incomplete draft plasmids may yield partial
allelic profiles.

Typical order: `plasmidfinder` (replicon) → `pmlst` (scheme ST) → optional
`mob-suite` (MOB/reconstruction). Chromosomal isolate ST is `mlst`, not pMLST.

## How to run

```bash
# bioconda preferred
mamba install -c bioconda -c conda-forge pmlst_ssi
# select scheme per upstream docs / --help
pmlst -i assembly.fasta -o pmlst_out -s IncI1
# exact entrypoint/flags vary by packaging — follow installed help
```

Pin software + scheme/database versions; report the scheme name with every ST.

## Decision tree

```text
Plasmid typing depth?
├─ Replicon only → plasmidfinder / staramr
├─ Plasmid ST (scheme) → pmlst
├─ Chromosomal ST → mlst
├─ MOB / reconstruction → mob-suite
└─ Meta plasmid contigs → genomad / plasmaag
```

## Related skills

`cge-finders` · `plasmidfinder` · `mlst` · `mob-suite` · `staramr` ·
`genomad` · `plasmaag` · `abricate` · `microbial-mining` · `tool-selection`
