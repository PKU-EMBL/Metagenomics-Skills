---
name: maxbin2
description: >
  Automated multi-metagenome contig binning. Use for installation, parameter choice,
  execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, maxbin"
  metagenomics.upstream: "https://sourceforge.net/projects/maxbin2/"
  metagenomics.stage: "binning"
---

# MaxBin 2

Upstream: [MaxBin 2](https://sourceforge.net/projects/maxbin2/)

## Citation

Wu, Y.-W., Simmons, B. A. & Singer, S. W. MaxBin 2.0: an automated binning algorithm to recover genomes from multiple metagenomic datasets. *Bioinformatics* **32**, 605–607 (2016). https://doi.org/10.1093/bioinformatics/btv638

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MaxBin 2 uses **nucleotide composition + differential abundance** across samples
(expectation-maximization). It is a classical workhorse and a valuable
**ensemble member** because it often recovers different genomes than MetaBAT2.

| vs MetaBAT2 | Notes |
|-------------|-------|
| Strength | Multi-sample abundance model; widely packaged in MetaWRAP |
| Weakness | Slower / heavier on huge contig sets; fewer adaptive TNF tricks |

Prefer multi-coverage abundance tables. Always QC with CheckM2; for catalogues
feed into `basalt` ★ / `metawrap` / `dastool`.

## How to run

```bash
run_MaxBin.pl -contig contigs.fa -abund depth.txt \
  -out temp/bins/maxbin -thread 16
# multiple -abund for multi-sample; see MaxBin docs for format
```

## Key parameters

| Flag | Notes |
|------|-------|
| `-abund` | Coverage table(s); IDs must match contig headers |
| `-thread` | Threads |
| min contig length | Record the installed default and justify any override |

## Decision tree

```text
Single classical binner?
├─ Adaptive TNF+coverage → metabat2
├─ EM abundance+composition → maxbin2
├─ GMM composition+coverage → concoct
└─ Catalogue / multi-assembly → basalt ★
```

## Related skills

`metabat2` · `concoct` · `dastool` · `metawrap` · `basalt` · `checkm2` ·
`tool-selection`
