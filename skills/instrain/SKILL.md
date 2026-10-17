---
name: instrain
description: >
  Strain-level microdiversity and shared-strain detection from metagenomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "strain, microdiversity, snp"
  metagenomics.upstream: "https://github.com/MrOlm/inStrain"
  metagenomics.stage: "strain"
---

# inStrain

Upstream: [inStrain](https://github.com/MrOlm/inStrain)

## Citation

Olm, M. R. *et al.* inStrain profiles population microdiversity from metagenomic data and sensitively detects shared microbial strains. *Nat. Biotechnol.* **39**, 727–736 (2021). https://doi.org/10.1038/s41587-020-00797-0

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Species-level profilers (MetaPhlAn, Kraken, sylph) and MAG catalogues do not
resolve **within-species** SNP microdiversity or prove strain sharing across
samples. inStrain profiles diversity from reads mapped to genomes/MAGs and
detects shared strains with sensitive comparisons.

Requirements for trustworthy results:

- High-quality mapping to **dereplicated**, preferably high-completeness genomes
- Adequate breadth/depth of coverage (tool filters — report them)
- Not a replacement for species profiling or for ANI catalogue building (`drep` /
  `skani`)

Typical order: bin → CheckM2/GUNC → dRep → map reads → `inStrain profile` →
optional compare for shared strains.

## How to run

```bash
set -euo pipefail
[[ -s "temp/map/${id}.bam" && -s genomes.fa ]] || exit 2
inStrain profile "temp/map/${id}.bam" genomes.fa \
  -o "temp/instrain/${id}" -p 16
# After profiling at least two samples against the same reference:
inStrain compare -i temp/instrain/sample1 temp/instrain/sample2 \
  -o temp/instrain/cohort_compare -p 16
```

## Key parameters

| Input | Notes |
|-------|-------|
| BAM | To dereplicated references; consistent mapper |
| Coverage / breadth filters | Record the installed defaults and predeclare every override |
| `compare` | Shared-strain detection across profiles |

## Related skills

`bowtie2` · `strobealign` · `drep` · `skani` · `coverm` · `metaphlan` ·
`tool-selection` · `metagenomics-workflow`
