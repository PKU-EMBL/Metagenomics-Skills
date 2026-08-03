---
name: genomad
description: >
  Identify plasmids, viruses, and other mobile genetic elements in assemblies. Use this skill when working with genomad: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/apcamargo/genomad. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['MGE', 'plasmid', 'virus', 'genome-mining']
upstream: https://github.com/apcamargo/genomad
stage: mining
---

# geNomad

Upstream: [geNomad](https://github.com/apcamargo/genomad)

## Citation

Camargo, A. P. *et al.* Identification of mobile genetic elements with geNomad. *Nat. Biotechnol.* **42**, 1303–1312 (2024). https://doi.org/10.1038/s41587-023-01953-y

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

geNomad mines **MGEs** (plasmids/viruses) from contigs or genomes. Essential for plasmidome/virome claims and for flagging MGE-borne AMR. Does not replace CheckV for viral quality.

## How to run

```bash
conda install -c bioconda genomad  # if packaged; else follow upstream docs

genomad download-database db/genomad
genomad end-to-end contigs.fa temp/genomad --cleanup --threads 16
```

## Key parameters

| DB | `genomad download-database` | Pin version |
| input | contigs or genomes | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

checkv · virsorter2 · rgi · antismash · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
