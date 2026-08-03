---
name: bracken
description: >
  Bayesian re-estimation of abundance from Kraken2 reports. Use this skill when working with bracken: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/jenniferlu717/Bracken. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'kraken', 'abundance']
upstream: https://github.com/jenniferlu717/Bracken
stage: taxonomy
---

# Bracken

Upstream: [Bracken](https://github.com/jenniferlu717/Bracken)

## Citation

Lu, J., Breitwieser, F. P., Thielen, P. & Salzberg, S. L. Bracken: estimating species abundance in metagenomics data. *PeerJ Comput. Sci.* **3**, e104 (2017). https://doi.org/10.7717/peerj-cs.104

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Run **after** Kraken2 with a matching Bracken DB built from the same Kraken DB. Do not mix MetaPhlAn and Bracken tables unlabeled.

## How to run

```bash
conda install -c bioconda bracken  # if packaged; else follow upstream

bracken -d $KRAKEN2_DB -i temp/kraken/${id}.report -o temp/kraken/${id}.bracken -r 150 -l S
```

## Key parameters

| `-d` | same as Kraken DB | Required |
| `-r` | read length | Match data |
| `-l` | taxonomic level | S/G/… |

## Decision notes

- Stage: **taxonomy** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

kraken2 · metaphlan · visualization · `tool-selection` · `metagenomics-workflow`
