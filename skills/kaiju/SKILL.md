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

Kaiju classifies reads by **six-frame translated** matches against a protein DB
(LCA of hits). Strength: remote homology / understudied clades where DNA k-mers
fail. Weakness: weaker close-species separation than good DNA classifiers.

| Tool | Signal | Prefer when |
|------|--------|-------------|
| `kaiju` | AA / protein | Novel / divergent lineages |
| `kraken2` | DNA k-mers | Speed, custom DNA DBs |
| `metabuli` | Joint DNA+AA | Want both sensitivity and specificity |
| `metaphlan` / `singlem` | Markers | Clade/SGB or unknown-species marker profiles |

Database choice dominates results. Do not merge Kaiju tables with MetaPhlAn
unlabeled.

## How to run

```bash
kaiju -t nodes.dmp -f kaiju_db.fmi \
  -i clean_1.fq.gz -j clean_2.fq.gz -z 16 \
  -o temp/kaiju/${id}.out
kaiju2table -t nodes.dmp -n names.dmp -r species \
  -o temp/kaiju/${id}.tsv temp/kaiju/${id}.out
```

## Key parameters

| Item | Notes |
|------|-------|
| DB | RefSeq / nr / proGenomes-derived builds — pin release |
| `-z` | Threads |
| `-a` / greedy modes | See upstream for sensitivity vs speed |
| Rank in `kaiju2table` | Species/genus — state in Methods |

## Decision tree

```text
Protein-aware read taxonomy?
├─ Yes, AA sensitivity primary → kaiju
├─ Joint DNA+AA → metabuli
├─ Marker composition → metaphlan / singlem
└─ Fast DNA k-mer → kraken2 (+ bracken)
```

## Methods caveats

- Hits depend on protein DB completeness; unclassified ≠ empty community
- Pin Kaiju + NCBI taxonomy dump versions used to build the DB

## Related skills

`metabuli` · `kraken2` · `diamond` · `metaphlan` · `singlem` · `tool-selection`
