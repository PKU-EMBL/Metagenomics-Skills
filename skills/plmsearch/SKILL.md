---
name: plmsearch
description: >
  PLMSearch — protein language model embeddings for fast, sensitive remote homology
  search from sequences alone. Use when: (1) Homology is too remote for BLAST/MMseqs,
  (2) Structure search is unavailable but structural similarity is expected, (3)
  Screening large query–target protein pairs.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PLM, remote-homology, search, protein"
  metagenomics.upstream: "https://github.com/maovshao/PLMSearch"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed-research-code"
  metagenomics.upstream-version: "snapshot d6df1dc"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "research scripts reviewed against upstream notebook; not executed here"
---

# PLMSearch

Upstream: [maovshao/PLMSearch](https://github.com/maovshao/PLMSearch) ·
https://dmiip.sjtu.edu.cn/PLMSearch

## Citation

Liu, W. *et al.* PLMSearch: Protein language model powers accurate and fast
sequence search for remote homology. *Nat. Commun.* **15**, 2775 (2024).
https://doi.org/10.1038/s41467-024-46808-5

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

## Inputs and run

The upstream release is research code rather than a stable installed CLI. Pin the repository and released `plmsearch_data` bundle (ESM-1b weights, target embeddings/Pfam data, and `plmsearch.sav`). This explicit form mirrors `pipeline.ipynb` while naming outputs.

```bash
set -euo pipefail
[[ -s query.faa && -s plmsearch_data/model/plmsearch.sav ]] || exit 2
mkdir -p result/plmsearch
python plmsearch/embedding_generate.py -f query.faa \
  -e result/plmsearch/query.embedding.pkl
python plmsearch/pfam_generate.py -f query.faa \
  -o result/plmsearch/query.pfam.json
python plmsearch/main_pfam.py \
  -qpr result/plmsearch/query.pfam.json \
  -tpr plmsearch_data/swissprot/pfam_result.json -c \
  -opr result/plmsearch/pfamclan.prefilter.json
python plmsearch/main_similarity.py \
  -iqe result/plmsearch/query.embedding.pkl \
  -ite plmsearch_data/swissprot/embedding.pkl \
  -smp plmsearch_data/model/plmsearch.sav \
  -isr result/plmsearch/pfamclan.prefilter.json \
  -osr result/plmsearch/hits.json
```

Use `--nogpu` for embedding generation on CPU. Verify option names against the pinned commit because these scripts do not promise a stable API.

## Decision tree

```text
Protein search sensitivity need?
├─ Standard → mmseqs2 / diamond
├─ Have structures → foldseek (± folddisco motifs)
├─ Remote homology, sequence-only → plmsearch
├─ Need explicit structural alignment from sequence → deepblast
└─ Gene neighborhood modules → spacedust
```

## Validation, recovery, and provenance

Require one finite embedding per query, parseable Pfam/prefilter/hit objects and complete query-ID accounting. Verify released target IDs and ranked scores, inspect known positive/negative proteins, and confirm priority hits with MMseqs2/DIAMOND, Foldseek/structure or profile HMM evidence. Do not infer function solely from nearest embedding.

Never overwrite released target artifacts; write query outputs atomically and restart failed stages from a clean file. Record repository commit, requirements, ESM/model/data bundle URLs and checksums, device/CUDA, commands, query checksum, output schema/checksum and orthogonal validation. PLM similarity is computational homology evidence, not experimental function.

## Related skills

`protein-language-model` · `esm` · `prostt5` · `metagenomics-llm` ·
`foldseek` · `folddisco` · `deepblast` · `mmseqs2` · `diamond` ·
`eggnog-mapper` · `spacedust` · `tool-selection`
