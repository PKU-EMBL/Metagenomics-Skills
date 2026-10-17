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
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "amethyst/vDino snapshot c9d765b"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "wrapper CLI reviewed against upstream; not executed here"
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

Hit ≠ complete conjugative element. Pin the database release and use its matching metadata/parser; do not combine legacy beatrix/kyanite with current amethyst/vDino assets.

## Inputs and run

The reviewed amethyst wrapper accepts nucleotide contigs/long reads, calls Prodigal, searches the matching DIAMOND DB, and merges release metadata.

```bash
set -euo pipefail
root=${MOBILEOG_PL:?set MOBILEOG_PL to the pinned mobileOG-pl directory}
input=contigs.fa
db=db/mobileOG-db-amethyst.dmnd
meta=db/mobileOG-db-amethyst.All.csv
[[ -s "$input" && -s "$db" && -s "$meta" ]] || exit 2
(
  cd "$root"
  bash mobileOGs-pl-amethyst.sh -i "$OLDPWD/$input" -d "$OLDPWD/$db" \
    -m "$OLDPWD/$meta" -k 15 -e 1e-20 -p 60 -q 80
) >mobileog.stdout.log 2>mobileog.stderr.log
test -s "${input}.mobileOG.Alignment.Out.csv"
test -s "${input}_temp_summary.csv"
```

Thresholds above are the stringent amethyst quick-start example, not universal biological cutoffs; predeclare and sensitivity-test changes.

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

## Validation, recovery, and provenance

Reconcile output proteins to contig coordinates and DIAMOND rows; inspect identity, query coverage, e-value, element-class/category, database source and neighboring hits. Require coherent multi-gene/context evidence before labeling a complete MGE and retain no-hit contigs. Check controls and compare with geNomad, ISEScan, IntegronFinder or MOB-suite for claim-specific evidence.

The wrapper writes files beside the input; run on a staged copy or archive outputs before rerunning. Record mobileOG-pl commit/parser, database and metadata release/checksums, Prodigal/DIAMOND versions, command/thresholds, input checksum and result checksums. Protein-family labels do not prove element boundaries, mobility, host or activity.

## Related skills

`genomad` · `isescan` · `integronfinder` · `mob-suite` · `rgi` · `plasmaag` ·
`microbial-mining` · `tool-selection`
