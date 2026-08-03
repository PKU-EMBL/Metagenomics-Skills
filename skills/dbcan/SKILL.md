---
name: dbcan
description: >
  Annotate carbohydrate-active enzymes (CAZymes) with dbCAN/run_dbcan on
  genomes or protein sets. Use for CAZyme mining complementary to DRAM/eggNOG.
  Upstream: https://github.com/linnabrown/run_dbcan.
license: MIT
category: analysis-tools
tags: [CAZy, CAZyme, genome-mining, annotation]
upstream: https://github.com/linnabrown/run_dbcan
stage: mining
---

# dbCAN (run_dbcan)

Upstream: [linnabrown/run_dbcan](https://github.com/linnabrown/run_dbcan)

## Citation

Huang, L. *et al.* dbCAN-seq: a database of carbohydrate-active enzyme
(CAZyme) sequence and annotation. *Nucleic Acids Res.* **46**, D516–D521
(2018). https://doi.org/10.1093/nar/gkx1036  
*(use the dbCAN/run_dbcan paper matching your installed major version)*

## Analytical thinking

CAZyme annotation supports **carbohydrate metabolism mining** (plant polymers,
mucin, etc.). Prefer protein FASTA from `bakta`/`prodigal`. Consensus across
HMM/DIAMOND tools inside dbCAN is stronger than a single hit — report the
version’s recommended evidence rules.

Complements `dram` distillates; do not double-count the same genes in figures
without noting both tools.

## How to run

```bash
# Follow upstream for DB download (dbCAN-HMM, CAZy, …)
run_dbcan proteins.faa protein --out_dir temp/dbcan/${id} --db_dir db/dbcan -t 16
```

## Related skills

`dram` · `eggnog-mapper` · `bakta` · `prodigal` · `microbial-mining`
