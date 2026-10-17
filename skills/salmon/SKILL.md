---
name: salmon
description: >
  Fast quantification of gene/transcript abundance; use --meta for metagenomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "quantification, abundance"
  metagenomics.upstream: "https://github.com/COMBINE-lab/salmon"
  metagenomics.stage: "function"
---

# Salmon

Upstream: [COMBINE-lab/salmon](https://github.com/COMBINE-lab/salmon)

## Citation

Patro, R., Duggal, G., Love, M. I., Irizarry, R. A. & Kingsford, C. Salmon provides fast and bias-aware quantification of transcript expression. *Nat. Methods* **14**, 417–419 (2017). https://doi.org/10.1038/nmeth.4197

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Quantify a **non-redundant gene catalogue** (nucleotides) with dehosted PE reads.
Typical catalogue path:

```text
prodigal (contigs) → cd-hit | mmseqs2 (NR) → salmon quant --meta
                   → eggnog-mapper on NR proteins
```

For metagenomes pass **`--meta`**. Prefer TPM vs counts consciously — downstream
stats must match the unit. CoverM genome abundance ≠ gene catalogue TPM.

Note: salmon 2.x (Rust) changed index format — rebuild indexes when upgrading;
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

## Key parameters

| Flag | Notes |
|------|-------|
| `--meta` | Metagenome mode — required for community catalogues |
| `-l A` | Auto library type; verify if stranded protocols used |
| Index | Rebuild after salmon major version change |

## Decision tree

```text
Abundance need?
├─ NR gene catalogue → salmon --meta
├─ Genome/MAG relative abundance → coverm
├─ Pathway/gene families from reads → humann
└─ Contig coverage for binning → coverm contig / mapper depths
```

## Related skills

`prodigal` · `cd-hit` · `mmseqs2` · `eggnog-mapper` · `coverm` · `kneaddata` ·
`humann` · `tool-selection`
