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
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.1.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream source; not executed here"
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
set -euo pipefail
DB=${PMLST_DB:?set PMLST_DB to a pinned pMLST database checkout}
SCHEME=${PMLST_SCHEME:?set a supported scheme such as incf or inci1}
[[ -s assembly.fasta && -d "$DB" ]] || exit 2
mkdir -p pmlst_out pmlst_tmp
pmlst --version
pmlst -i assembly.fasta -s "$SCHEME" -p "$DB" \
  -o pmlst_out -t pmlst_tmp -x
find pmlst_out -type f -size +0c | grep -q .
```

This targets pMLST 2.1.1. Validate `PMLST_SCHEME` against `pmlst --help`, pin the database commit/version file, preserve partial/unknown allele profiles, and report scheme with every ST.

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
