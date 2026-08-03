---
name: virsorter2
description: >
  Viral sequence identification from metagenomic assemblies. Use this skill when working with virsorter2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/jiarong/VirSorter2. For routing across mining tasks use microbial-mining.
  For stage order use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['virus', 'phage', 'genome-mining']
upstream: https://github.com/jiarong/VirSorter2
stage: mining
---

# VirSorter2

Upstream: [VirSorter2](https://github.com/jiarong/VirSorter2)

## Citation

Guo, J. *et al.* VirSorter2: a multi-classifier, expert-guided approach to detect diverse DNA and RNA viruses. *Microbiome* **9**, 37 (2021). https://doi.org/10.1186/s40168-020-00990-y

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Classic viral contig mining. Pair with **CheckV** for quality and optionally geNomad for cross-method consensus. Viral taxonomy is a separate claim from bacterial MAG taxonomy.

## How to run

```bash
conda install -c bioconda virsorter  # if packaged; else follow upstream docs

virsorter run -w temp/virsorter2 -i contigs.fa --min-length 1500 -j 16 all
```

## Key parameters

| `--min-length` | 1500+ | Reduce noise |
| DB | vs2 setup | Once |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

checkv · genomad · megahit · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
