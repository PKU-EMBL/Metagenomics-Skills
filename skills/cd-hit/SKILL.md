---
name: cd-hit
description: >
  Cluster genes/proteins to build non-redundant catalogues. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "clustering, dereplication"
  metagenomics.upstream: "https://github.com/weizhongli/cdhit"
  metagenomics.stage: "function"
---

# CD-HIT

Upstream: [weizhongli/cdhit](https://github.com/weizhongli/cdhit)

## Citation

Fu, L., Niu, B., Zhu, Z., Wu, S. & Li, W. CD-HIT: accelerated for clustering the next-generation sequencing data. *Bioinformatics* **28**, 3150–3152 (2012). https://doi.org/10.1093/bioinformatics/bts565

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

`cd-hit-est` collapses redundant nucleotide ORFs into a non-redundant catalogue.
Defaults used widely in shotgun catalogues: identity **0.95**, alignment coverage
**0.9** (`-c 0.95 -aS 0.9`). Changing thresholds changes biological interpretation
of “a gene”—report them.

## How to run

```bash
cd-hit-est -i genes.fna -o NR/nucleotide.fa \
  -aS 0.9 -c 0.95 -G 0 -g 0 -T 0 -M 0
seqkit translate --trim NR/nucleotide.fa > NR/protein.fa
```

## Related skills

`prodigal` · `salmon` · `eggnog-mapper`

