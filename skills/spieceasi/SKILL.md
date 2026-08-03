---
name: spieceasi
description: >
  SPIEC-EASI — Sparse Inverse Covariance Estimation for Ecological Association
  Inference; compositionally robust microbial network inference (MB / glasso)
  with optional SparCC. Use for conditional association networks from count /
  relative abundance tables. Upstream: https://github.com/zdk123/SpiecEasi.
  Route via research-analysis; pure SparCC correlations → sparcc.
license: MIT
category: evaluation
tags: [SPIEC-EASI, SpiecEasi, network, glasso, microbiome, compositionality]
upstream: https://github.com/zdk123/SpiecEasi
stage: report
---

# SPIEC-EASI (SpiecEasi)

Upstream: [zdk123/SpiecEasi](https://github.com/zdk123/SpiecEasi)

## Citation

Kurtz, Z. D. *et al.* Sparse and compositionally robust inference of microbial
ecological networks. *PLoS Comput. Biol.* **11**, e1004226 (2015).
https://doi.org/10.1371/journal.pcbi.1004226

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

SPIEC-EASI infers **sparse graphical models** (neighborhood selection or
glasso) after compositional transforms — edges closer to conditional dependence
than raw correlations. Includes a `sparcc()` implementation for comparison.
Needs enough samples relative to taxa; filter rare features; pin method
(`mb`/`glasso`), λ path, and StARS/pulsar settings.

Networks are hypotheses — not proven interactions.

## How to run

```r
# remotes::install_github("zdk123/SpiecEasi")
library(SpiecEasi)
# se <- spiec.easi(counts, method='mb', lambda.min.ratio=1e-2, nlambda=20,
#                  pulsar.params=list(rep.num=50))
# extract adjacency / plot with igraph — follow README
```

## Decision tree

```text
Network inference need?
├─ Conditional sparse network → spieceasi
├─ SparCC correlations only → sparcc
├─ Group DA → ancombc / maaslin2
└─ Exploratory plots → microeco / phyloseq
```

## Related skills

`sparcc` · `research-analysis` · `microeco` · `phyloseq` · `maaslin2` ·
`tool-selection`
