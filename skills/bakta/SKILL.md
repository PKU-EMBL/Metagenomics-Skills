---
name: bakta
description: >
  Rapid standardized annotation of bacterial genomes (alignment-free ID). Use this skill when working with bakta: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/oschwengers/bakta. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['annotation', 'genome-mining', 'prokaryote']
upstream: https://github.com/oschwengers/bakta
stage: mining
---

# Bakta

Upstream: [Bakta](https://github.com/oschwengers/bakta)

## Citation

Schwengers, O. *et al.* Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. *Microb. Genom.* **7**, 000685 (2021). https://doi.org/10.1099/mgen.0.000685

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Modern per-genome annotator preferred over Prokka for many new studies. Good substrate for antiSMASH/DRAM/RGI on polished MAGs.

## How to run

```bash
conda install -c bioconda bakta  # if packaged; else follow upstream docs

bakta --db $BAKTA_DB --threads 8 --output temp/bakta/${id} genome.fa
```

## Key parameters

| `$BAKTA_DB` | required | Pin |
| input | complete/near-complete preferred | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

prokka · prodigal · antismash · dram · rgi · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
