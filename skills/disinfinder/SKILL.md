---
name: disinfinder
description: >
  DisinFinder — CGE disinfectant / biocide resistance gene screen via the
  DisinFinder database, typically run through ResFinder. Use for isolate
  biocide-resistance markers alongside acquired AMR. DB:
  https://bitbucket.org/genomicepidemiology/disinfinder_db. Route via
  cge-finders / resfinder / microbial-mining.
license: MIT
category: analysis-tools
tags: [DisinFinder, CGE, biocide, disinfectant, resistance, ResFinder]
upstream: https://bitbucket.org/genomicepidemiology/disinfinder_db
stage: mining
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

See also [docs/references.md](../../docs/references.md), `resfinder`, and
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
git clone https://bitbucket.org/genomicepidemiology/disinfinder_db.git
# ResFinder disinfectant search (flag names follow installed --help)
python -m resfinder -ifa assembly.fasta -o disinf_out \
  -db_res /path/to/resfinder_db \
  -db_disinf /path/to/disinfinder_db
# some builds use an explicit disinfectant / --disinf switch — check --help
```

Pin ResFinder software + `disinfinder_db` commit/tag.

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
