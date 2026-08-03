---
name: diamond
description: >
  Ultra-fast protein alignment (BLASTP/X alternative) for functional/taxonomic searches. Use this skill when working with diamond: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/bbuchfink/diamond. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['mapping', 'protein', 'blast']
upstream: https://github.com/bbuchfink/diamond
stage: mapping
---

# DIAMOND

Upstream: [DIAMOND](https://github.com/bbuchfink/diamond)

## Citation

Buchfink, B., Reuter, K. & Drost, H.-G. Sensitive protein alignments at tree-of-life scale using DIAMOND. *Nat. Methods* **18**, 366–368 (2021). https://doi.org/10.1038/s41592-021-01101-x

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Use for gene→UniRef/NR/eggNOG-scale protein search and contig taxonomy helpers. Not a substitute for Bowtie2 coverage mapping.

## How to run

```bash
conda install -c bioconda diamond  # if packaged; else follow upstream

diamond makedb --in proteins.faa -d ref
diamond blastp -q query.faa -d ref -o hits.tsv -p 16 -f 6
```

## Key parameters

| `blastp/blastx` | mode | |
| `-f 6` | tabular | BLAST-like |

## Decision notes

- Stage: **mapping** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

eggnog-mapper · mmseqs2 · blast · `tool-selection` · `metagenomics-workflow`
