---
name: lucaphylo
description: >
  LucaPhylo — alignment-free phylogenetic inference / placement via hyperbolic protein
  language models (ESM2 + hyperbolic geometry). Use when: (1) MSA-based trees fail on
  highly divergent proteins, (2) Exploring PLM phylogeny as a complement to
  IQ-TREE/PhyloPhlAn, (3) Following the LucaPhylo training or placement checkpoints.
  Route via phylogenomics; do not replace GTDB-Tk for MAG taxonomy by default.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "LucaPhylo, PLM, phylogeny, hyperbolic, alignment-free, ESM2"
  metagenomics.upstream: "https://github.com/NickShannn/LucaPhylo"
  metagenomics.stage: "taxonomy"
---

# LucaPhylo

Upstream: [NickShannn/LucaPhylo](https://github.com/NickShannn/LucaPhylo) ·
Checkpoints: https://huggingface.co/NickShan/LucaPhylo

## Citation

Shan, Y. *et al.* Alignment-free phylogenetic inference via hyperbolic protein
language models. *bioRxiv* https://doi.org/10.64898/2026.05.26.723419 (2026).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classical phylogenomics needs MSAs. LucaPhylo places **unaligned** proteins
using ESM2 embeddings adapted into hyperbolic space — aimed at highly divergent
sequences (training emphasis includes viral RdRP / polyprotein settings). Treat
as an **AI phylogeny** track next to `iqtree` / `phylophlan`, not as default MAG
taxonomy (`gtdbtk`).

| vs | Prefer LucaPhylo when |
|----|------------------------|
| `iqtree` / `phylophlan` | MSA unreliable or discarded divergent taxa |
| `homology-search` | Goal is a tree/placement, not hit tables |
| `gtdbtk` | Never as sole bacterial MAG taxonomy |

Pin checkpoint stage (1–4), backbone tree, and that results are computational
hypotheses. GPU recommended for training; inference benchmarks include CPU/GPU
profiles in upstream docs.

## How to run

```bash
conda create -n lucaphylo python=3.10.16
conda activate lucaphylo
git clone https://github.com/NickShannn/LucaPhylo.git
cd LucaPhylo
pip install -r requirements.txt
# download checkpoints (HF / Zenodo) — see upstream README
# training stages:
#   bash scripts/run_stage_1.sh … run_stage_4_train.sh
# placement / inference: follow Stage-4 inference scripts in upstream docs
```

Do not invent CLI flags — follow the repository scripts for the installed tag.

## Decision tree

```text
Phylogeny without reliable MSA?
├─ Yes, PLM/hyperbolic placement → lucaphylo
├─ Standard MAG/marker phylogenomics → phylophlan → iqtree
├─ Taxonomy placement only → gtdbtk
└─ Homology search only → homology-search
```

## Related skills

`phylogenomics` · `protein-language-model` · `esm` · `iqtree` · `phylophlan` ·
`metagenomics-llm` · `omg` · `gtdbtk` · `tool-selection`
