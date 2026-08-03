---
name: metabinner
description: >
  MetaBinner — stand-alone ensemble contig binning using multi-feature k-means
  components and two-stage single-copy-gene ensemble integration. Use when:
  (1) Running MetaBinner as an ensemble-style single tool, (2) Comparing to
  MetaWRAP/DAS Tool/COMEBin, (3) Diversifying bin sets before further
  refinement. Upstream: https://github.com/ziyewang/MetaBinner. For recommended
  multi-assembly refinement still prefer basalt ★.
license: MIT
category: analysis-tools
tags: [binning, MetaBinner, ensemble, SCG]
upstream: https://github.com/ziyewang/MetaBinner
stage: binning
---

# MetaBinner

Upstream: [ziyewang/MetaBinner](https://github.com/ziyewang/MetaBinner)

## Citation

Wang, Z. *et al.* MetaBinner: a high-performance and stand-alone ensemble
binning method to recover individual genomes from complex microbial
communities. *Genome Biol.* **24**, 1 (2023).
https://doi.org/10.1186/s13059-022-02832-6

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

MetaBinner is an **internal ensemble**: multiple k-means component binning
results (multi-feature) integrated with SCG-aware two-stage selection — a
stand-alone alternative to piping MetaBAT/MaxBin into MetaWRAP/DAS Tool.

Still feed outputs through CheckM2; for related multi-assembly catalogues prefer
`basalt` ★. Complements `comebin` from the same group.

## How to run

```bash
# follow upstream scripts — typically contigs + coverage tables
MetaBinner ...  # verify flags in README
```

## Related skills

`comebin` · `metawrap` · `dastool` · `basalt` · `checkm2` · `tool-selection`
