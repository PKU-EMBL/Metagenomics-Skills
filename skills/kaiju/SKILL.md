---
name: kaiju
description: >
  Fast sensitive taxonomic classification via protein-level matches. Use this skill when working with kaiju: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/bioinformatics-centre/kaiju. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'protein', 'classification']
upstream: https://github.com/bioinformatics-centre/kaiju
stage: taxonomy
---

# Kaiju

Upstream: [Kaiju](https://github.com/bioinformatics-centre/kaiju)

## Citation

Menzel, P., Ng, K. L. & Krogh, A. Fast and sensitive taxonomic classification for metagenomics with Kaiju. *Nat. Commun.* **7**, 11257 (2016). https://doi.org/10.1038/ncomms11257

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Protein-aware read taxonomy — useful when nucleotide markers fail. Database choice dominates; not interchangeable with MetaPhlAn labels.

## How to run

```bash
conda install -c bioconda kaiju  # if packaged; else follow upstream

kaiju -t nodes.dmp -f kaiju_db.fmi -i clean_1.fq.gz -j clean_2.fq.gz -z 16 -o temp/kaiju/${id}.out
kaiju2table -t nodes.dmp -n names.dmp -r species -o temp/kaiju/${id}.tsv temp/kaiju/${id}.out
```

## Key parameters

| DB | RefSeq/nr builds | Large |
| `-z` | threads | |

## Decision notes

- Stage: **taxonomy** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

kraken2 · diamond · metaphlan · `tool-selection` · `metagenomics-workflow`
