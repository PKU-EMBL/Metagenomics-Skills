---
name: prodigal
description: >
  Protein-coding gene prediction; use -p meta for metagenomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "genes, orf"
  metagenomics.upstream: "https://github.com/hyattpd/Prodigal"
  metagenomics.stage: "gene"
---

# Prodigal

Upstream: [hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)

## Citation

Hyatt, D. *et al.* Prodigal: prokaryotic gene recognition and translation initiation site identification. *BMC Bioinformatics* **11**, 119 (2010). https://doi.org/10.1186/1471-2105-11-119

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

For metagenomes always use **`-p meta`**. Gene catalogues inherit assembly
errors—garbage contigs produce garbage ORFs. Optionally keep only complete genes
(`partial=00`) when catalogs are huge.

## How to run

```bash
prodigal -i contigs.fa \
  -d genes.fna -a genes.faa \
  -o genes.gff -p meta -f gff
```

## Decision tree

```text
Have contigs?
├─ Build gene catalogue → prodigal → cd-hit → salmon → eggnog-mapper
└─ Only MAGs → predict genes per MAG later for annotation
```

## Related skills

`megahit` · `cd-hit` · `salmon` · `eggnog-mapper`

