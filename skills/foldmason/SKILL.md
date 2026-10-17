---
name: foldmason
description: >
  FoldMason — multiple protein structure alignment at scale (Steinegger lab). Use when:
  (1) Building structural MSAs from AFDB / predicted models, (2) Comparing folds across
  MAG protein families after Foldseek clustering, (3) Preparing structure-aware
  alignments for phylogeny or motif work.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "FoldMason, structure-MSA, Foldseek, alignment"
  metagenomics.upstream: "https://github.com/steineggerlab/foldmason"
  metagenomics.stage: "function"
---

# FoldMason

Upstream: [steineggerlab/foldmason](https://github.com/steineggerlab/foldmason) ·
Web: https://search.foldseek.com/foldmason

## Citation

Gilchrist, C. L. M., Mirdita, M. & Steinegger, M. Multiple protein structure
alignment at scale with FoldMason. *Science* **391**, 485–488 (2026).
https://doi.org/10.1126/science.ads6733

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Foldseek finds pairwise structural neighbors; **FoldMason** builds scalable
**multiple** structure alignments (FASTA + HTML reports). Useful after
clustering dark proteins or AFDB hits into families.

| vs | Prefer FoldMason when |
|----|------------------------|
| `foldseek` | Need MSA of many structures, not just hit table |
| Sequence MSA (MAFFT/…) | Structures available / twilight zone |
| `folddisco` | Global structural MSA vs local motif |

## How to run

```bash
conda install -c bioconda foldmason
foldmason easy-msa structures/*.pdb result.fasta tmp --report-mode 1
# HTML report when --report-mode 1; webserver also available
```

## Decision tree

```text
Have a set of related structures?
├─ Pairwise search only → foldseek
├─ Multiple structure alignment → foldmason
├─ Short motif → folddisco
└─ Sequence MSA → hh-suite / classical aligners
```

## Related skills

`foldseek` · `folddisco` · `foldcomp` · `unicore` · `homology-search` ·
`phylogenomics` · `tool-selection`
