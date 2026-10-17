---
name: deepblast
description: >
  TM-Vec and DeepBLAST — deep learning for protein remote homology and structural
  alignment from sequences (predict TM-scores; align homologous regions without solved
  structures). Use when: (1) Searching structure-like similarity in large sequence DBs,
  (2) Aligning remote homologs for annotation, (3) Complementing PLMSearch / Foldseek
  workflows.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "DeepBLAST, TM-Vec, remote-homology, structure, PLM"
  metagenomics.upstream: "https://github.com/flatironinstitute/deepblast"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-research-code"
  metagenomics.upstream-version: "DeepBLAST snapshot ec661fa; TM-Vec wiki workflow"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "TM-Vec/DeepBLAST CLI reviewed against upstream wiki; not executed here"
---

# TM-Vec / DeepBLAST

Upstream: [tm-vec](https://github.com/tymor22/tm-vec) ·
[deepblast](https://github.com/flatironinstitute/deepblast)

## Citation

Hamamsy, T. *et al.* Protein remote homology detection and structural alignment
using deep learning. *Nat. Biotechnol.* **42**, 975–985 (2024).
https://doi.org/10.1038/s41587-023-01917-2

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

| Component | Role |
|-----------|------|
| **TM-Vec** | Predict structural similarity (TM-score-like) from sequence pairs; search large DBs |
| **DeepBLAST** | Structurally align proteins from sequence by identifying homologous regions |

Designed for the metagenomic reality that many proteins lack close sequence
neighbors but retain structural homology. Complementary to `plmsearch` and to
structure search (Foldseek) when structures/pLDDT models exist.

## Inputs and run

Install the `tm-vec` package in a frozen Linux environment and download checksummed TM-Vec model/config, DeepBLAST checkpoint, database embeddings, metadata and matching FASTA. Search first; request alignments only for a limited top-K because DeepBLAST alignment is much slower.

```bash
set -euo pipefail
mkdir -p result
for f in query.faa tm_vec_cath_model.ckpt tm_vec_cath_model_params.json \
  database/db.npy database/meta.npy database/sequences.faa; do [[ -s "$f" ]] || exit 2; done
tmvec-search \
  --query query.faa \
  --tm-vec-model tm_vec_cath_model.ckpt \
  --tm-vec-config tm_vec_cath_model_params.json \
  --database database/db.npy --metadata database/meta.npy \
  --database-fasta database/sequences.faa --device gpu \
  --output-format tabular --output result/tmvec.tsv \
  --output-embeddings result/query_embeddings.npy \
  >result/tmvec.stdout.log 2>result/tmvec.stderr.log
```

For structural alignments, index the database FASTA, add `--database-faidx`, `--deepblast-model`, `--k-nearest-neighbors`, and use `--output-format alignment`. Use CPU only when resource estimates accept the >10× slowdown reported upstream.

## Decision tree

```text
Remote homology workflow?
├─ Fast PLM embedding search → plmsearch
├─ TM-score search + structural alignment → deepblast (TM-Vec)
├─ Have structures / AFDB → foldseek (± folddisco / spacedust)
└─ Close homologs → mmseqs2 / diamond
```

## Validation, recovery, and provenance

Require complete query accounting, finite embeddings, parseable `query_id/rank/database_id/tm-score` rows, coordinate-valid alignments when requested, and known positive/negative controls. Inspect score calibration and disagreement between TM-Vec and DeepBLAST; confirm important hits using sequence/profile or actual structure evidence. The upstream docs note edge cases for very high identity and low predicted TM-score.

Write outputs to new paths after changing checkpoint/database and never mix embedding arrays with different metadata order. Record package/source versions, model/config/database URLs and hashes, device/CUDA, command, FASTA/checksums, top-K and output checksums. Predicted TM scores and alignments are computational evidence, not solved structures or function.

## Related skills

`protein-language-model` · `esm` · `plmsearch` · `metagenomics-llm` ·
`foldseek` · `folddisco` · `spacedust` · `mmseqs2` · `eggnog-mapper` ·
`tool-selection`
