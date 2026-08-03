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

Sketch-based profiling — very fast for large cohorts / genome containment. Complementary to MetaPhlAn/Kraken; cite DB/sketch set.

## How to run

```bash
conda install -c bioconda sylph  # if packaged; else follow upstream

sylph sketch -c 200 reads_1.fq.gz reads_2.fq.gz -o temp/sylph/${id}
sylph profile temp/sylph/${id}.syldb database.syldb -o temp/sylph/${id}.tsv
```

## Key parameters

| sketch DB | prebuilt / custom | Pin |
| containment | genome presence | |

## Decision notes

- Stage: **taxonomy** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

metaphlan · kraken2 · motus · gtdb · `tool-selection` · `metagenomics-workflow`
