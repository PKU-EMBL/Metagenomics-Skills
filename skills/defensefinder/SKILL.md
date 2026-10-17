---
name: defensefinder
description: >
  Detect anti-phage defense systems in prokaryotic genomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "defense, CRISPR, genome-mining"
  metagenomics.upstream: "https://github.com/mdmparis/defense-finder"
  metagenomics.stage: "mining"
---

# DefenseFinder

Upstream: [DefenseFinder](https://github.com/mdmparis/defense-finder)

## Citation

Tesson, F. *et al.* Systematic and quantitative view of the antiviral arsenal of prokaryotes. *Nat. Commun.* **13**, 2561 (2022). https://doi.org/10.1038/s41467-022-30269-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Mines **defense systems** (CRISPR and beyond). Complements `padloc` (different
system models — often run both for surveys) and viral MGE mining
(`genomad` / `virsorter2`) for host–virus interaction stories.

## How to run

```bash
conda install -c bioconda defense-finder  # if packaged; else follow upstream docs

defense-finder run genome.faa --out temp/defense/${id}
```

## Key parameters

| input | proteins preferred | From Bakta/Prokka |
| models | installed DB | Pin |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

`padloc` · `genomad` · `virsorter2` · `spacedust` · `bakta` · `antismash` ·
`microbial-mining` · `tool-selection` · `metagenomics-workflow`
