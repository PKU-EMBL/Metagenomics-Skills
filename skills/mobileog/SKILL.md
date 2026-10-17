---
name: mobileog
description: >
  mobileOG-db — manually curated protein families for bacterial MGE life-cycle functions
  (integration/excision, replication/recombination/repair, stability/defense, transfer,
  phage-related) with diamond + mobileOG-pl parsing. Use to annotate MGE machinery on
  MAG/contig proteins beyond geNomad contig scores.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mobileOG, MGE, plasmid, phage, ICE, genome-mining"
  metagenomics.upstream: "https://github.com/clb21565/mobileOG-db"
  metagenomics.stage: "mining"
---

# mobileOG-db

Upstream: [clb21565/mobileOG-db](https://github.com/clb21565/mobileOG-db) ·
Portal: https://mobileogdb.flsi.cloud.vt.edu/

## Citation

Brown, C. L. *et al.* mobileOG-db: a Manually Curated Database of Protein
Families Mediating the Life Cycle of Bacterial Mobile Genetic Elements.
*Appl. Environ. Microbiol.* **88**, e00991-22 (2022).
https://doi.org/10.1128/aem.00991-22

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

mobileOG-db labels proteins into MGE machinery categories (IE, RRR, STD, T, P).
Use after gene call to interpret **what MGE functions** are present; pair with
`genomad` (contig-level plasmid/virus calls), `isescan` (IS), `integronfinder`
(integrons), and `mob-suite` (plasmid typing).

Hit ≠ complete conjugative element. Pin database release (e.g. beatrix) and
DIAMOND thresholds from upstream/mobileOG-pl docs.

## How to run

```bash
# build/download diamond DB from mobileOG release; then e.g.
diamond blastp -q proteins.faa --db mobileOG-db.dmnd -o hits.tsv \
  --outfmt 6 …   # thresholds: follow mobileOG-pl README
# parse with mobileOGs-pl-*.py — see upstream mobileOG-pl/
```

## Decision tree

```text
MGE functional proteins?
├─ Contig plasmid/virus scores → genomad
├─ MGE protein machinery categories → mobileog
├─ Insertion sequences → isescan
├─ Integrons / cassettes → integronfinder
├─ Plasmid MOB/replicon typing → mob-suite
└─ ARG on MGEs → rgi ∩ genomad/mobileog context
```

## Related skills

`genomad` · `isescan` · `integronfinder` · `mob-suite` · `rgi` · `plasmaag` ·
`microbial-mining` · `tool-selection`
