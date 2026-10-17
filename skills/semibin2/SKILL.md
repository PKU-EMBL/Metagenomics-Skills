---
name: semibin2
description: >
  Self-supervised contrastive learning binning for short- and long-read assemblies. Use
  for installation, parameter choice, execution, output interpretation, or
  troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, semibin, self-supervised"
  metagenomics.upstream: "https://github.com/BigDataBiology/SemiBin"
  metagenomics.stage: "binning"
---

# SemiBin2

Upstream: [SemiBin2](https://github.com/BigDataBiology/SemiBin)

## Citation

Pan, S., Zhao, X.-M. & Coelho, L. P. SemiBin2: self-supervised contrastive learning leads to better MAGs for short- and long-read sequencing. *Bioinformatics* **39**, i21–i29 (2023). https://doi.org/10.1093/bioinformatics/btad209

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

SemiBin1 used **semi-supervised** contrastive learning with contig annotation —
costly and reference-biased. SemiBin2 switches to **self-supervised** embeddings
from contigs alone, improving HQ MAG counts while cutting runtime (~25%) and
peak memory (~11%) vs SemiBin1 on real short-read samples in the paper.

For long reads, SemiBin2 adds an **ensemble-based DBSCAN** clustering path
(reported 13–26% more HQ genomes than the next-best long-read binner in that
study). Compare with dedicated `lorbin` on long-read assemblies.

Still a **single binner**: for catalogues, feed into `basalt` ★ / `metawrap` /
`dastool`. Prefer multi-sample coverage when related samples exist.

## How to run

```bash
conda install -c conda-forge -c bioconda semibin2

# short-read / general easy mode
SemiBin2 single_easy_bin \
  -i contigs.fa \
  -b temp/map/*.bam \
  -o temp/bins/semibin2 \
  -t 16

# multi-sample / long-read modes: see SemiBin2 docs (environment + DBSCAN options)
```

## Key parameters

| Mode | When |
|------|------|
| `single_easy_bin` | One assembly + BAMs |
| multi-sample modes | Related samples with shared genomes |
| long-read / DBSCAN path | Long-read contigs; pin and record the installed mode/options |

## Literature notes

- Prefer SemiBin2 over SemiBin1 unless reproducing an old Methods block.
- Self-supervision removes annotation bottleneck but does not remove need for
  CheckM2/GUNC.
- Ensemble with classical binners increases recovery diversity (DAS Tool /
  MetaWRAP / BASALT logic).

## Decision notes

- Stage: **binning**
- Long-read alternative/complement: `lorbin`
- Ensemble: `basalt` ★ · `metawrap` · `dastool`

## Related skills

`metabat2` · `vamb` · `comebin` · `lorbin` · `dastool` · `basalt` · `bowtie2` ·
`tool-selection` · `metagenomics-workflow`
