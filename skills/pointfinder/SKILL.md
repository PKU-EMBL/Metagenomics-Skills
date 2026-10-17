---
name: pointfinder
description: >
  PointFinder — CGE detection of antimicrobial resistance associated with chromosomal
  point mutations in selected bacterial pathogens. Use when acquired-gene screens miss
  mutation-driven resistance (e.g. gyrA, rpoB). DB: pointfinder_db; often run via
  ResFinder (-c) or staramr.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PointFinder, CGE, AMR, chromosomal, mutation, SNP, resistome"
  metagenomics.upstream: "https://bitbucket.org/genomicepidemiology/pointfinder_db"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "ResFinder 4.7.2 interface"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "PointFinder branch reviewed against ResFinder source; not executed here"
---

# PointFinder

Database: [pointfinder_db](https://bitbucket.org/genomicepidemiology/pointfinder_db) ·
Typically invoked through [ResFinder](https://github.com/genomicepidemiology/resfinder)
(`-c` / `--db_path_point`) or [staramr](https://github.com/phac-nml/staramr).

## Citation

Zankari, E. *et al.* PointFinder: a novel web tool for WGS-based detection of
antimicrobial resistance associated with chromosomal point mutations in bacterial
pathogens. *J. Antimicrob. Chemother.* **72**, 2764–2768 (2017).
https://doi.org/10.1093/jac/dkx217

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md), `resfinder`, and
`cge-finders`.

## Analytical thinking

PointFinder is **species-panel limited** (e.g. *E. coli*, *Salmonella*,
*Campylobacter*, enterococci, … — check current DB). It finds known
resistance-associated chromosomal SNPs/indels, not novel mutations outside the
panel. Always state organism used for the PointFinder scheme.

Prefer running via current ResFinder / staramr so software and DB stay aligned.
Do not treat as a substitute for acquired-gene ResFinder/`rgi` hits.

## How to run

```bash
set -euo pipefail
POINT_DB=${POINTFINDER_DB:?set POINTFINDER_DB}
SPECIES=${POINTFINDER_SPECIES:?set a species supported by the pinned database}
[[ -s assembly.fasta && -d "$POINT_DB" ]] || exit 2
python -m resfinder --inputfasta assembly.fasta -o point_out \
  --species "$SPECIES" --db_path_point "$POINT_DB" --point
test -d point_out
```

Alternatively, run the explicit scheme through `$staramr` (for example, `--pointfinder-organism escherichia_coli`) rather than silently inferring a species.

## Decision tree

```text
Mutation-driven AMR?
├─ Species in PointFinder panel → pointfinder via resfinder/staramr
├─ Acquired genes → resfinder / rgi
├─ Unknown environmental MAG → prefer rgi; PointFinder often N/A
└─ Phenotype confirmation → AST / MIC (out of scope)
```

## Related skills

`cge-finders` · `resfinder` · `staramr` · `plasmidfinder` · `rgi` ·
`microbial-mining` · `tool-selection`
