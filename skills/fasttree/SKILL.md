---
name: fasttree
description: >
  FastTree — approximately-maximum-likelihood trees for large alignments. Use when: (1)
  Draft phylogenies from big MSAs, (2) Quick topology screens before IQ-TREE, (3)
  Resource-limited exploratory MAG trees. For final ML trees prefer iqtree.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "FastTree, phylogeny, approximate-ML, tree"
  metagenomics.upstream: "https://github.com/morgannprice/fasttree"
  metagenomics.stage: "taxonomy"
---

# FastTree

Upstream: [morgannprice/fasttree](https://github.com/morgannprice/fasttree) ·
often packaged as `fasttree` / `FastTreeMP` (bioconda)

## Citation

Price, M. N., Dehal, P. S. & Arkin, A. P. FastTree: computing large minimum
evolution trees with profiles instead of a distance matrix. *Mol. Biol. Evol.*
**26**, 1641–1650 (2009). https://doi.org/10.1093/molbev/msp077

Price, M. N., Dehal, P. S. & Arkin, A. P. FastTree 2 — approximately
maximum-likelihood trees for large alignments. *PLoS ONE* **5**, e9490 (2010).
https://doi.org/10.1371/journal.pone.0009490

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FastTree trades some accuracy for **speed on large MSAs** — ideal for
exploratory MAG/marker trees and PhyloPhlAn-scale drafts. For manuscript
figures and formal support values, re-infer with `iqtree`.

| vs | Prefer FastTree when |
|----|----------------------|
| `iqtree` | Huge MSA / quick topology / limited CPU |
| Distance-only trees | You still want approximate ML |

Always state FastTree vs IQ-TREE in Methods if both appear.

## How to run

```bash
# protein MSA example
FastTreeMP -lg < markers.fa > temp/fasttree/tree.nwk
# nucleotide
FastTreeMP -gtr -nt < markers.fna > temp/fasttree/tree.nwk
```

## Decision tree

```text
Tree speed vs rigor?
├─ Screen / huge alignment → fasttree
├─ Final ML + UFBoot → iqtree
└─ Full MAG phylogenomics workflow → phylophlan
```

## Related skills

`phylogenomics` · `iqtree` · `phylophlan` · `gtdbtk` · `mag-qc` ·
`tool-selection`
