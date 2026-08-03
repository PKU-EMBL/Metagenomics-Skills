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

Bracken redistributes Kraken-classified reads to a target taxonomic level using
a Bayesian model conditioned on genome lengths / k-mer uniqueness in the **same**
database build. It answers: “given Kraken’s read assignments, what are smoothed
abundances at rank L?” — not “is species X truly present?”

Caveats:

- Must use a Bracken index built from the **same** Kraken2 DB.
- `-r` read length should match sequencing.
- Rare taxa remain false-positive-prone; MetaPhlAn papers have criticized high
  FP rates for some Bracken setups — report confidence/thresholds carefully.
- Never paste Bracken and MetaPhlAn columns into one “species abundance” matrix
  without a method factor.

## How to run

```bash
bracken -d $KRAKEN2_DB -i temp/kraken/${id}.report \
  -o temp/kraken/${id}.bracken -r 150 -l S
```

## Key parameters

| Flag | Notes |
|------|-------|
| `-d` | Same DB root as Kraken2 |
| `-r` | Read length used to build Bracken files |
| `-l` | Rank (S/G/…) |
| `-t` | Min reads threshold (if used) — affects rare taxa |

## Related skills

`kraken2` · `metaphlan` · `metabuli` · `visualization` · `tool-selection`
