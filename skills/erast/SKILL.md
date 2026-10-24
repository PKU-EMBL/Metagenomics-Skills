---
name: erast
description: >
  ERAST — efficient retrieval-augmented homology search combining sequence
  language-model embeddings with a billion-scale vector database (protein and
  nucleotide). Use when: (1) Classical BLAST/MMseqs/Foldseek scale poorly, (2) You need
  vector-DB nearest-neighbor search plus reranking, (3) Accessing the public ERAST web
  DB or running the local encode→predict pipeline.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ERAST, vector-DB, embedding, homology, PLM, search"
  metagenomics.upstream: "https://github.com/TencentAILabHealthcare/ERAST"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-experimental"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "local protein pipeline arguments checked against upstream pipeline README; not executed here"
---

# ERAST

Upstream: [TencentAILabHealthcare/ERAST](https://github.com/TencentAILabHealthcare/ERAST) ·
Web vector DB: https://ai4s.tencent.com/erast

## Citation

Jiang, Y. *et al.* Scalable homology detection with ERAST. *Nat. Biotechnol.*
(2026). https://doi.org/10.1038/s41587-026-03051-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

ERAST is the **vector-database** route: embed sequences (ESM2-class PLMs),
retrieve neighbors from a ~billion-sequence index, then preretrieval / retrieval /
postretrieval (rerank) stages. Supports **protein and nucleotide**. Complements
— does not replace — `mmseqs2` / `foldseek` for routine catalogues.

| vs | Prefer ERAST when |
|----|-------------------|
| `mmseqs2` / `diamond` | Extreme DB scale / embedding retrieval desired |
| `foldseek` | No structures; or nt+protein vector search |
| `plmsearch` / `deepblast` | Using the public billion-scale ERAST index / web DB |

Caveats: pin model + Pfam DB + EHSM checkpoint; web DB ≠ your private catalogue
unless you rebuild locally; embedding hits need careful annotation transfer.

## How to run

**Web:** https://ai4s.tencent.com/erast

**Local protein pipeline**, using absolute paths because the scripts run from a
pinned checkout:

```bash
set -Eeuo pipefail
pipeline="${ERAST_PIPELINE:?set ERAST_PIPELINE to the checkout pipeline directory}"
pfam="${PFAMDB:?set PFAMDB to a pinned Pfam directory}"
model="${ERAST_MODEL_PATH:?set ERAST_MODEL_PATH to the pinned embedding model}"
query="${1:?usage: run-erast.sh ABS_QUERY_FASTA ABS_TARGET_FASTA ABS_OUTPUT_DIR}"
target="${2:?usage: run-erast.sh ABS_QUERY_FASTA ABS_TARGET_FASTA ABS_OUTPUT_DIR}"
out="${3:?usage: run-erast.sh ABS_QUERY_FASTA ABS_TARGET_FASTA ABS_OUTPUT_DIR}"
[[ "$pipeline" = /* && "$pfam" = /* && "$model" = /* && \
   "$query" = /* && "$target" = /* && "$out" = /* ]] || exit 2
for file in "$query" "$target" "$pfam/Pfam-A.hmm" \
  "$pfam/Pfam-A.hmm.dat" "$pfam/Pfam-A.hmm.h3f" "$pfam/Pfam-A.hmm.h3i" \
  "$pfam/Pfam-A.hmm.h3m" "$pfam/Pfam-A.hmm.h3p"; do
  test -s "$file" || exit 2
done
test -f "$pipeline/predict.py" && test -e "$model" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
reranker_args=()
if [[ -n "${ERAST_RERANKER:-}" ]]; then
  test -e "$ERAST_RERANKER" || exit 2
  reranker_args=(--reranker "$ERAST_RERANKER")
fi
(
  cd "$pipeline"
  python ./pfam_scan.py -out "$out/query.pfam.json" -outfmt json "$query" "$pfam"
  python ./pfam_scan.py -out "$out/target.pfam.json" -outfmt json "$target" "$pfam"
  python ./encode.py --res_path "$out/query.emb.npy" --model_path "$model" \
    --fa_path "$query" --mode p
  python ./encode.py --res_path "$out/target.emb.npy" --model_path "$model" \
    --fa_path "$target" --mode p
  python ./predict.py --fa_q "$query" --fa_t "$target" \
    --emb_q "$out/query.emb.npy" --emb_t "$out/target.emb.npy" \
    --pfam_q "$out/query.pfam.json" --pfam_t "$out/target.pfam.json" \
    --out "$out/predictions.jsonl" "${reranker_args[@]}" --mode p
) >"$out/erast.stdout.log" 2>"$out/erast.stderr.log"
for file in query.pfam.json target.pfam.json query.emb.npy target.emb.npy; do
  test -s "$out/$file"
done
test -f "$out/predictions.jsonl"
```

Nucleotide mode has a distinct embedding/prediction contract and no Pfam stage;
do not reuse the protein command by merely changing the FASTA alphabet. The EHSM
reranker checkpoint is separate from the embedding model.

## Decision tree

```text
Need homology at extreme scale / vector retrieval?
├─ Public billion-seq search → erast web DB
├─ Custom local sets → erast pipeline (encode → predict)
├─ Structure available → foldseek
├─ Routine catalogues → mmseqs2 / diamond
└─ Unsure → homology-search
```

## Validation, recovery, and provenance

Reconcile every query to hits or an explicit no-hit state. Inspect duplicate IDs,
sequence type/length limits, Pfam coverage, embedding shape, nearest-neighbor and
reranker score distributions, ties, controls, and agreement with classical
search. Validate annotation-transfer thresholds on a held-out set.

Use fresh outputs after changing sequences, Pfam, models, reranker, code, or
mode. Record ERAST commit, Python/package/device versions, Pfam release/checksum,
model and EHSM identifiers/revisions/checksums, query/target checksums, commands,
logs, intermediate arrays, and result checksums. Web searches must record access
date/index release and are not equivalent to the local target set.

## Related skills

`homology-search` · `plmsearch` · `deepblast` · `mmseqs2` · `foldseek` ·
`metagenomics-llm` · `tool-selection`
