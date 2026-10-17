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

**Local pipeline** reviewed from `pipeline/readme.md`:

```bash
# Pfam + ESM2 embeddings + homology prediction (protein mode).
PFAMDB=${PFAMDB:?set PFAMDB to the pinned Pfam assets}
MODEL_PATH=${MODEL_PATH:?set MODEL_PATH to the pinned ESM2/ERAST checkpoint}
[[ -e "$PFAMDB" && -e "$MODEL_PATH" ]] || exit 2
cd pipeline
python pfam_scan.py -out example/pfam_q.json -outfmt json example/q.fa "$PFAMDB"
python pfam_scan.py -out example/pfam_t.json -outfmt json example/t.fa "$PFAMDB"
python encode.py --res_path example/q_emb.npy --model_path "$MODEL_PATH" --fa_path example/q.fa
python encode.py --res_path example/t_emb.npy --model_path "$MODEL_PATH" --fa_path example/t.fa
python predict.py --fa_q example/q.fa --fa_t example/t.fa \
  --emb_q example/q_emb.npy --emb_t example/t_emb.npy \
  --pfam_q example/pfam_q.json --pfam_t example/pfam_t.json \
  --out example/out.jsonl --mode p
# Nucleotide runs use the separately prepared nucleotide artifacts and --mode n.
```

EHSM checkpoint: Zenodo record noted in upstream README.

## Decision tree

```text
Need homology at extreme scale / vector retrieval?
├─ Public billion-seq search → erast web DB
├─ Custom local sets → erast pipeline (encode → predict)
├─ Structure available → foldseek
├─ Routine catalogues → mmseqs2 / diamond
└─ Unsure → homology-search
```

## Related skills

`homology-search` · `plmsearch` · `deepblast` · `mmseqs2` · `foldseek` ·
`metagenomics-llm` · `tool-selection`
