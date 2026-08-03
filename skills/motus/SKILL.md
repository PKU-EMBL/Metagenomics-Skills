---
name: motus
description: >
  Marker-gene taxonomic profiling across environments (mOTUs3). Use this skill when working with motus: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/motu-tool/mOTUs. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'marker', 'profile']
upstream: https://github.com/motu-tool/mOTUs
stage: taxonomy
---

# mOTUs

Upstream: [mOTUs](https://github.com/motu-tool/mOTUs)

## Citation

Ruscheweyh, H.-J. *et al.* Cultivation-independent genomes greatly expand taxonomic-profiling capabilities of mOTUs across various environments. *Microbiome* **10**, 212 (2022). https://doi.org/10.1186/s40168-022-01410-z

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Marker-based alternative/complement to MetaPhlAn. Pin mOTUs DB version; do not merge with Kraken without labels.

## How to run

```bash
conda install -c bioconda motus  # if packaged; else follow upstream

motus profile -f clean_1.fq.gz -r clean_2.fq.gz -t 16 -o temp/motus/${id}.motus
```

## Key parameters

| DB | motus download-db | Pin version |
| `-t` | threads | |

## Decision notes

- Stage: **taxonomy** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

metaphlan · kraken2 · sylph · `tool-selection` · `metagenomics-workflow`
