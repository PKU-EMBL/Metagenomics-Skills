---
name: disinfinder
description: >
  DisinFinder — CGE disinfectant / biocide resistance gene screen via the DisinFinder
  database, typically run through ResFinder. Use for isolate biocide-resistance markers
  alongside acquired AMR.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "DisinFinder, CGE, biocide, disinfectant, resistance, ResFinder"
  metagenomics.upstream: "https://bitbucket.org/genomicepidemiology/disinfinder_db"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "ResFinder 4.7.2 interface"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "DisinFinder branch reviewed against ResFinder source; not executed here"
---

# DisinFinder

Database: [disinfinder_db](https://bitbucket.org/genomicepidemiology/disinfinder_db) ·
Invoked through [ResFinder](https://github.com/genomicepidemiology/resfinder)
(`--db_path_disinf` / disinfectant mode).

## Citation

Cite ResFinder 4 / resource papers (DisinFinder ships as a CGE DB used by
ResFinder):

Bortolaia, V. *et al.* ResFinder 4.0 for predictions of phenotypes from
genotypes. *J. Antimicrob. Chemother.* **75**, 3491–3500 (2020).
https://doi.org/10.1093/jac/dkaa345

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md), `resfinder`, and
`cge-finders`.

## Analytical thinking

DisinFinder targets **disinfectant / biocide-associated** determinants
(separate from ResFinder antibiotic genes and PointFinder chromosomal SNPs).
Hit ≠ measured biocide MIC or clinical antiseptic failure. Keep tables separate
from CARD/`rgi` antibiotic claims.

Prefer ResFinder CLI with the DisinFinder DB installed and pinned. Batch isolate
AMR+plasmid workflows may still use `staramr` for antibiotics/plasmids, then
add DisinFinder via ResFinder when biocide genes are in scope.

## How to run

```bash
set -euo pipefail
DISINF_DB=${DISINFINDER_DB:?set DISINFINDER_DB}
[[ -s assembly.fasta && -d "$DISINF_DB" ]] || exit 2
python -m resfinder --help >/dev/null
python -m resfinder --inputfasta assembly.fasta -o disinf_out \
  --db_path_disinf "$DISINF_DB" --disinfectant
test -d disinf_out
```

This command targets the ResFinder interface exposing `-db_disinf`; do not run it with a release whose help omits that option. Pin ResFinder, `resfinder_db`, and `disinfinder_db` commits.

## Decision tree

```text
Biocide / disinfectant genes?
├─ CGE DisinFinder DB → disinfinder via resfinder
├─ Antibiotic acquired genes → resfinder
├─ Chromosomal AMR SNPs → pointfinder
├─ CARD antibiotics → rgi
└─ Multi-DB mass screen → abricate (if DB includes relevant sets)
```

## Related skills

`cge-finders` · `resfinder` · `pointfinder` · `staramr` · `abricate` · `rgi` ·
`plasmidfinder` · `microbial-mining` · `tool-selection`
