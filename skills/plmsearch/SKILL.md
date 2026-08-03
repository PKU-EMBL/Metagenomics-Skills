---
name: plmsearch
description: >
  PLMSearch — protein language model embeddings for fast, sensitive remote
  homology search from sequences alone. Use when: (1) Homology is too remote
  for BLAST/MMseqs, (2) Structure search is unavailable but structural
  similarity is expected, (3) Screening large query–target protein pairs.
  Upstream: https://github.com/maovshao/PLMSearch.
  Web: https://dmiip.sjtu.edu.cn/PLMSearch. Route via metagenomics-llm.
license: MIT
category: analysis-tools
tags: [PLM, remote-homology, search, protein]
upstream: https://github.com/maovshao/PLMSearch
stage: function
---

# PLMSearch

Upstream: [maovshao/PLMSearch](https://github.com/maovshao/PLMSearch) ·
https://dmiip.sjtu.edu.cn/PLMSearch

## Citation

Liu, W. *et al.* PLMSearch: Protein language model powers accurate and fast
sequence search for remote homology. *Nat. Commun.* **15**, 2775 (2024).
https://doi.org/10.1038/s41467-024-46808-5

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Classical sequence search misses many remote homologs (low identity, similar
structure). PLMSearch uses **pretrained PLM representations** plus a similarity
model trained with structural similarity signals — sequence-only input, structure-
aware sensitivity, MMseqs2-like speed on large pair screens in the paper’s
benchmarks.

| Tool | When |
|------|------|
| `mmseqs2` / `diamond` | Default catalogue search |
| `foldseek` | Structures / ProstT5 available |
| `plmsearch` | Remote homology / dark proteins (sequence-only PLM) |
| `deepblast` | Structure-aware alignment + TM-score prediction (TM-Vec) |

Hits remain computational — transfer annotation cautiously.

## How to run

```bash
# follow upstream README for env + PLM weights (e.g. ESM / ProtT5 family)
# typical: embed query/target → similarity search → ranked homologs
```

## Decision tree

```text
Protein search sensitivity need?
├─ Standard → mmseqs2 / diamond
├─ Have structures → foldseek (± folddisco motifs)
├─ Remote homology, sequence-only → plmsearch
├─ Need explicit structural alignment from sequence → deepblast
└─ Gene neighborhood modules → spacedust
```

## Related skills

`metagenomics-llm` · `foldseek` · `folddisco` · `deepblast` · `mmseqs2` ·
`diamond` · `eggnog-mapper` · `spacedust` · `tool-selection`
