---
name: salmon
description: >
  Fast quantification of gene/transcript abundance; use --meta for metagenomes. Use this skill when working with salmon: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/COMBINE-lab/salmon. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['quantification', 'abundance']
upstream: https://github.com/COMBINE-lab/salmon
---

# Salmon

Upstream: [COMBINE-lab/salmon](https://github.com/COMBINE-lab/salmon)

## Citation

Patro, R., Duggal, G., Love, M. I., Irizarry, R. A. & Kingsford, C. Salmon provides fast and bias-aware quantification of transcript expression. *Nat. Methods* **14**, 417–419 (2017). https://doi.org/10.1038/nmeth.4197

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Quantify the **NR gene catalogue** with salmon using dehosted PE reads.
For metagenomes pass **`--meta`**. Prefer TPM vs counts consciously—downstream
stats must match the unit.

Note: salmon 2.x (Rust) changed index format—rebuild indexes when upgrading;
bioconda may still ship 1.x (`salmon-cpp`). Pin and document the version.

## How to run

```bash
salmon index -t NR/nucleotide.fa -i temp/salmon/index -p 8

salmon quant -i temp/salmon/index -l A -p 8 --meta \
  -1 temp/hr/${id}_1.fastq -2 temp/hr/${id}_2.fastq \
  -o temp/salmon/${id}.quant

salmon quantmerge --quants temp/salmon/*.quant -o result/salmon/gene.TPM
salmon quantmerge --quants temp/salmon/*.quant --column NumReads \
  -o result/salmon/gene.count
```

## Related skills

`cd-hit` · `eggnog-mapper` · `kneaddata`

