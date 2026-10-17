---
name: dbcan
description: >
  Annotate carbohydrate-active enzymes (CAZymes) with dbCAN3 / run_dbcan on genomes or
  protein sets, including CGC finding and glycan substrate prediction (dbCAN-sub /
  dbCAN-PUL) relevant to dissolved organic matter (DOM) polymer processing. Use for
  CAZyme mining complementary to DRAM/eggNOG and to dom-biosurfactant routing.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "CAZy, CAZyme, DOM, glycan, substrate, genome-mining, dbCAN3"
  metagenomics.upstream: "https://github.com/linnabrown/run_dbcan"
  metagenomics.stage: "mining"
---

# dbCAN (run_dbcan / dbCAN3)

Upstream: [linnabrown/run_dbcan](https://github.com/linnabrown/run_dbcan) ·
Server: https://bcb.unl.edu/dbCAN2/

## Citation

Zheng, J. *et al.* dbCAN3: automated carbohydrate-active enzyme and substrate
annotation. *Nucleic Acids Res.* **51**, W115–W121 (2023).
https://doi.org/10.1093/nar/gkad328

Earlier: Zhang, H. *et al.* dbCAN2: a meta server for automated carbohydrate-active
enzyme annotation. *Nucleic Acids Res.* **46**, W95–W101 (2018).
https://doi.org/10.1093/nar/gky418

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CAZymes process complex carbohydrates — a major fraction of **DOM / polymer
organic matter** (cellulose, xylan, pectin, mucin, etc.). dbCAN3 adds
**substrate prediction** at subfamily and CGC/PUL levels. Prefer protein FASTA
(+ GFF for CGC) from `bakta`/`prodigal`. Consensus across HMMER/DIAMOND/
dbCAN-sub is stronger than a single hit.

| vs | Prefer dbCAN when |
|----|-------------------|
| `hadeg` / `biosurfdb` | Glycan DOM vs HC/biosurfactant genes |
| `dram` | Dedicated CAZyme/substrate detail vs distillate sheets |
| `element-cycling` | Organic C polymer enzymes vs inorganic C/N/S cycles |

## How to run

```bash
# Preflight a pinned dbCAN bundle containing the enabled HMM/substrate assets.
[[ -d db/dbcan ]] || exit 2
run_dbcan proteins.faa protein --out_dir temp/dbcan/${id} --db_dir db/dbcan -t 16
# CGC + substrate: supply GFF / use substrate_prediction per run_dbcan docs
```

## Decision tree

```text
Glycan / DOM polymer capacity?
├─ CAZymes + substrates / CGC → dbcan
├─ HC / biosurfactant / plastic → hadeg (± biosurfdb)
├─ Broad distillate → dram
└─ Route menu → dom-biosurfactant
```

## Related skills

`dom-biosurfactant` · `hadeg` · `biosurfdb` · `dram` · `eggnog-mapper` ·
`bakta` · `prodigal` · `element-cycling` · `microbial-mining` · `tool-selection`
