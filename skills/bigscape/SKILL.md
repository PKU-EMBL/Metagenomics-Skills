---
name: bigscape
description: >
  Cluster and compare biosynthetic gene clusters across genomes with BiG-SCAPE
  (similarity networks of antiSMASH regions). Use after batch antiSMASH for BGC family
  discovery.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "BGC, network, genome-mining, antiSMASH"
  metagenomics.upstream: "https://github.com/medema-group/BiG-SCAPE"
  metagenomics.stage: "mining"
---

# BiG-SCAPE

Upstream: [medema-group/BiG-SCAPE](https://github.com/medema-group/BiG-SCAPE)

## Citation

Navarro-Muñoz, J. C. *et al.* A computational framework to explore large-scale
biosynthetic diversity. *Nat. Chem. Biol.* **16**, 60–68 (2020).
https://doi.org/10.1038/s41589-019-0400-9

## Analytical thinking

BiG-SCAPE groups antiSMASH regions into **BGC families** via similarity
networks. Requires consistent antiSMASH outputs. Family membership ≠ identical
chemistry — use for prioritization and diversity plots.

## How to run

```bash
# After antiSMASH on many MAGs into a common input layout (see BiG-SCAPE docs):
bigscape -i temp/antismash_collection -o temp/bigscape -c 16 \
  --mibig --include_gbk_dir
```

CLI flags evolve — verify with your BiG-SCAPE version help.

## Related skills

`antismash` · `microbial-mining` · `bakta` · `visualization`
