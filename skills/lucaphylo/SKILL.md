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
  metagenomics.maturity: "reviewed-research-code"
  metagenomics.upstream-version: "v1.0 snapshot 30f52e8"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Stage-4 wrapper reviewed against upstream; not executed here"
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

Use the v1.0 Stage-4 wrapper with a matching Stage-2/3 base checkpoint, Stage-4 LoRA adapter, backbone tree and backbone/query FASTAs:

```bash
set -euo pipefail
root=${LUCAPHYLO_ROOT:?set LUCAPHYLO_ROOT to pinned snapshot 30f52e8}
: "${MODEL_NAME_OR_PATH:?set the matching Stage-2/3 checkpoint}"
: "${STAGE4_ADAPTER_PATH:?set the matching Stage-4 adapter}"
: "${BACKBONE_TREE:?set the backbone Newick}"
: "${BACKBONE_SEQS:?set the backbone protein FASTA}"
: "${QUERY_SEQS:?set the query protein FASTA}"
OUTPUT_DIR=${OUTPUT_DIR:-result/lucaphylo}
export MODEL_NAME_OR_PATH STAGE4_ADAPTER_PATH BACKBONE_TREE BACKBONE_SEQS QUERY_SEQS OUTPUT_DIR
export DEVICE=${DEVICE:-cuda:0}
[[ -f "$root/scripts/run_stage_4_infer.sh" ]] || exit 2
for f in "$BACKBONE_TREE" "$BACKBONE_SEQS" "$QUERY_SEQS"; do [[ -s "$f" ]] || exit 2; done
bash "$root/scripts/run_stage_4_infer.sh" --save_nj_tree
test -s "$OUTPUT_DIR/stage4_full_distance_matrix.csv"
test -s "$OUTPUT_DIR/stage4_infer_summary.json"
```

Require unique IDs, exact backbone-tree/FASTA leaf agreement, disjoint query IDs, symmetric finite distances with zero diagonal, and a tree containing all expected leaves. Record source/checkpoint revisions and hashes, parameters, device/dependencies, input/output checksums and the summary JSON. Do not resume into a directory from different checkpoints/backbones; model-derived distances/NJ trees are hypotheses, not taxonomy.

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
