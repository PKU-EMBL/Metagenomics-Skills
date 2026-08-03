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
stage: function
---

# Bakta

Upstream: [Bakta](https://github.com/oschwengers/bakta)

## Citation

Schwengers, O. *et al.* Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. *Microb. Genom.* **7**, 000685 (2021). https://doi.org/10.1099/mgen.0.000685

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Bakta provides **rapid, standardized** bacterial genome annotation with
alignment-free sequence identification — preferred substrate for many new
studies over Prokka when the Bakta DB is available.

Use on QC-filtered MAGs/genomes before `antismash`, `dram`, `rgi`,
`defensefinder`. Not a substitute for catalogue-scale `prodigal`+clustering.

## How to run

```bash
bakta --db $BAKTA_DB --threads 8 --output temp/bakta/${id} genome.fa
```

## Key parameters

| Item | Notes |
|------|-------|
| `$BAKTA_DB` | Required — pin release with software |
| Input | Prefer near-complete, low-contamination genomes |
| Threads | Scale with CPU |

## Decision tree

```text
Genome annotation substrate?
├─ Bacterial MAG/isolate, modern default → bakta
├─ Minimal classic pipeline → prokka
└─ Mining next → bakta/prokka → microbial-mining tools
```

## Related skills

`prokka` · `prodigal` · `antismash` · `dram` · `rgi` · `defensefinder` ·
`mag-qc` · `microbial-mining` · `tool-selection`
