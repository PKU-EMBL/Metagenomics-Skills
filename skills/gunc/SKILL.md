---
name: gunc
description: >
  Detect chimerism/contamination in prokaryotic genomes/MAGs. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, contamination, chimerism"
  metagenomics.upstream: "https://github.com/grp-bork/gunc"
  metagenomics.stage: "assessment"
---

# GUNC

Upstream: [GUNC](https://github.com/grp-bork/gunc)

## Citation

Orakov, A. *et al.* GUNC: detection of chimerism and contamination in prokaryotic genomes. *Genome Biol.* **22**, 178 (2021). https://doi.org/10.1186/s13059-021-02393-0

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CheckM-style metrics estimate surplus marker copies but under-detect some
**clade-level chimeras** (contigs from distinct lineages merged into one bin).
GUNC was built for those underdetected contamination types; the paper
conservatively estimated substantial residual contamination in public genomes
even after conventional QC.

Use GUNC **with** CheckM2 before strong claims on novel lineages, GEMs, or
BGCs tied to a single MAG. Contamination types to keep distinct in text:

| Type | Rough meaning |
|------|----------------|
| Redundant | Extra copies from related genome content |
| Non-redundant / chimeric | Foreign-lineage fragments in one “genome” |

Single-coverage binning can hide co-abundant contaminants within one sample —
multi-coverage binning + GUNC is a strong pair (Mattock & Watson 2023).

## How to run

```bash
conda install -c bioconda gunc  # if packaged; else follow upstream

gunc run -i bins/ --db_file $GUNC_DB -r temp/gunc -t 16
```

## Key parameters

| Item | Notes |
|------|-------|
| DB | Download/pin GUNC DB |
| With CheckM2 | Combine filters; discordant calls → manual review |
| Novel lineages | Higher scrutiny; GUNC DB taxonomy limits apply |

## Related skills

`checkm2` · `mag-qc` · `drep` · `basalt` · `study-design` · `tool-selection`
