---
name: gapseq
description: >
  Predict bacterial metabolic pathways and reconstruct genome-scale metabolic models.
  Use for installation, parameter choice, execution, output interpretation, or
  troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "metabolism, GEMs, genome-mining"
  metagenomics.upstream: "https://github.com/jotech/gapseq"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "find/draft/fill workflow checked against current upstream usage; not executed here"
---

# gapseq

Upstream: [gapseq](https://github.com/jotech/gapseq)

## Citation

Zimmermann, J., Kaleta, C. & Waschina, S. gapseq: informed prediction of bacterial metabolic pathways and reconstruction of accurate metabolic models. *Genome Biol.* **22**, 81 (2021). https://doi.org/10.1186/s13059-021-02295-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Downstream of genome annotation for **pathway/model mining**. Needs reasonably complete MAGs; low-completeness bins produce hollow models. Interpret human/gut context with `vmh` when relevant.

## How to run

Current granular workflow is `find` + `find-transport` → `draft` → `fill`.
Use a biologically justified medium rather than accepting growth after arbitrary
gap filling.

```bash
set -Eeuo pipefail
proteins="${1:?usage: build-gapseq.sh PROTEINS_FAA MEDIUM_CSV OUTPUT_DIR}"
medium="${2:?usage: build-gapseq.sh PROTEINS_FAA MEDIUM_CSV OUTPUT_DIR}"
out="${3:?usage: build-gapseq.sh PROTEINS_FAA MEDIUM_CSV OUTPUT_DIR}"
for input in "$proteins" "$medium"; do test -s "$input" || exit 2; done
proteins="$(realpath "$proteins")"
medium="$(realpath "$medium")"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
ln -s "$proteins" "$out/genome.faa"
(
  cd "$out"
  gapseq find -p all genome.faa >find.stdout.log 2>find.stderr.log
  gapseq find-transport genome.faa \
    >find-transport.stdout.log 2>find-transport.stderr.log
  gapseq draft -r genome-all-Reactions.tbl -t genome-Transporter.tbl \
    -p genome-all-Pathways.tbl >draft.stdout.log 2>draft.stderr.log
  gapseq fill -m genome-draft.RDS -n "$medium" \
    >fill.stdout.log 2>fill.stderr.log
)
```

## Key parameters

| completeness | prefer high-quality MAGs | |
| pathways | `-p all` costly | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Validation, recovery, and provenance

Require pathway/reaction/transporter tables, draft and gap-filled RDS/SBML
models, completed logs, and explicit medium/objective. Check mass/charge balance,
blocked reactions, exchange bounds, growth/no-growth controls, gap-filled
reaction count, gene-reaction support, and phenotype predictions against known
biology. Growth after gap filling alone is not validation.

Use a fresh directory after changing proteins, databases, medium, objective, or
release. Record gapseq/R/solver versions, database commit, genome quality and
protein checksum, medium checksum, commands, logs, draft/final model checksums,
added reactions, and validation tests. Fluxes remain model-conditioned
hypotheses.

## Related skills

`dram` · `bakta` · `checkm2` · `eggnog-mapper` · `microbial-mining` ·
`community-metabolic-modeling` · `tool-selection` · `metagenomics-workflow` ·
`vmh`
