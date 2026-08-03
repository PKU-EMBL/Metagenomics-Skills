---
name: sylph
description: >
  Rapid species-level metagenome profiling and containment estimation. Use this skill when working with sylph: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/bluenote-1577/sylph. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'sketch', 'profile']
upstream: https://github.com/bluenote-1577/sylph
stage: taxonomy
---

# sylph

Upstream: [sylph](https://github.com/bluenote-1577/sylph)

## Citation

Shaw, J. & Yu, Y. W. Rapid species-level metagenome profiling and containment estimation with sylph. *Nat. Biotechnol.* **43**, 1348–1359 (2025). https://doi.org/10.1038/s41587-024-02412-y

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Containment ANI between a reference genome and a metagenome is **biased at low
coverage** (missing k-mers look like divergence). Sylph models k-mer coverage
with a **zero-inflated Poisson**, estimates effective coverage λ, and reports
**coverage-adjusted ANI** plus abundances — two orthogonal outputs.

Why it matters:

- Very fast sketch-based profiling for large cohorts / large genome databases.
- Better presence/ANI calls for low-coverage genomes than naive containment.
- Complementary to MetaPhlAn (markers) and Kraken (LCA k-mers); cite sketch DB.
- User coverage thresholds still matter; assembly incompleteness ≠ low coverage.

## How to run

```bash
conda install -c bioconda sylph  # if packaged; else follow upstream

sylph sketch -c 200 reads_1.fq.gz reads_2.fq.gz -o temp/sylph/${id}
sylph profile temp/sylph/${id}.syldb database.syldb -o temp/sylph/${id}.tsv
# sylph query for ANI-style containment against genomes
```

## Key parameters

| Parameter | Notes |
|-----------|-------|
| `-c` | Subsampling rate (default 200 in paper examples) |
| sketch DB | Prebuilt (e.g. GTDB-based) or custom — pin version |
| coverage threshold | Presence gate; report in Methods |
| `profile` vs `query` | Abundance profiling vs genome containment ANI |

## Decision notes

- Stage: **taxonomy** / genome presence
- Prefer for large-scale genome-resolved containment + profiling speed
- Do not merge with MetaPhlAn/Kraken unlabeled

## Related skills

`metaphlan` · `kraken2` · `motus` · `metabuli` · `skani` · `coverm` ·
`tool-selection` · `metagenomics-workflow`
