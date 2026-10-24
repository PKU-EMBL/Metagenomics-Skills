---
name: prostt5
description: >
  ProstT5 — bilingual protein language model translating amino-acid sequences and
  Foldseek 3Di structure tokens (fine-tuned from ProtT5). Use when: (1) Building
  Foldseek DBs from FASTA via --prostt5-model, (2) Sequence-only structure-aware search
  without AlphaFold, (3) AA↔3Di representation tasks. HF: Rostlab/ProstT5. Parent
  ProtT5: Rostlab/prot_t5_xl_uniref50. Route via protein-language-model; production
  search usually via foldseek.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ProstT5, ProtT5, PLM, protein-language-model, 3Di, Foldseek, Rostlab"
  metagenomics.upstream: "https://github.com/mheinzinger/ProstT5"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Foldseek ProstT5 database workflow checked against current upstream documentation; not executed here"
---

# ProstT5 (ProtT5 → AA ↔ 3Di)

Upstream: [mheinzinger/ProstT5](https://github.com/mheinzinger/ProstT5) ·
HF: https://huggingface.co/Rostlab/ProstT5 ·
Parent ProtT5: https://huggingface.co/Rostlab/prot_t5_xl_uniref50

## Citation

Heinzinger, M. *et al.* Bilingual language model for protein sequence and
structure. *NAR Genom. Bioinform.* **6**, lqae150 (2024).
https://doi.org/10.1093/nargab/lqae150

ProtT5 / ProtTrans: Elnaggar, A. *et al.* ProtTrans: Toward Understanding the
Language of Life Through Self-Supervised Learning. *IEEE Trans. Pattern Anal.
Mach. Intell.* **44**, 7112–7127 (2022).
https://doi.org/10.1109/TPAMI.2021.3095381

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

ProstT5 fine-tunes **ProtT5** to translate between amino acids and Foldseek
**3Di** tokens. In metagenomics the main production path is **Foldseek
createdb/easy-search with `--prostt5-model`**: ~400–4000× faster than predicting
full structures before search, but ProstT5-only DBs lack Cα — no TM-score /
LDDT features that need coordinates.

| vs | Prefer ProstT5 when |
|----|---------------------|
| `esm` | Need 3Di / Foldseek path, not general ESM embeddings |
| `foldseek` (AFDB coords) | Only FASTA available; accept 3Di-only DB limits |
| `plmsearch` | Structure-token search vs PLM embedding homology |
| ColabFold (deferred) | Prefer AFDB / ProstT5+Foldseek over re-folding catalogues |

## How to run

Download and checksum the model once in setup. This production template converts
protein FASTA into a Foldseek database with predicted 3Di tokens.

```bash
set -Eeuo pipefail
proteins="${1:?usage: build-prostt5-db.sh PROTEINS_FASTA MODEL OUTPUT_DIR}"
model="${2:?usage: build-prostt5-db.sh PROTEINS_FASTA MODEL OUTPUT_DIR}"
out="${3:?usage: build-prostt5-db.sh PROTEINS_FASTA MODEL OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$proteins" && test -e "$model" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
gpu_args=()
[[ "${PROSTT5_GPU:-0}" = 1 ]] && gpu_args=(--gpu 1)
foldseek createdb "$proteins" "$out/query_db" --prostt5-model "$model" \
  --threads "$threads" "${gpu_args[@]}" \
  >"$out/createdb.stdout.log" 2>"$out/createdb.stderr.log"
test -e "$out/query_db" && test -e "$out/query_db_ss"
foldseek convert2fasta "$out/query_db_ss" "$out/query.3di.fasta" \
  >"$out/convert.stdout.log" 2>"$out/convert.stderr.log"
test -s "$out/query.3di.fasta"
seqkit stats -T "$proteins" "$out/query.3di.fasta" >"$out/sequence-stats.tsv"
awk 'NR==2{n=$4} NR==3 && $4!=n{exit 1} END{if(NR!=3) exit 1}' \
  "$out/sequence-stats.tsv"
```

Standalone Hugging Face embedding/translation is a distinct workflow: pin model
revision, tokenizer, generation settings, precision, device, seed and batching.

## Decision tree

```text
Need structure-aware protein search from FASTA?
├─ Yes, Foldseek production → foldseek + prostt5 weights
├─ AA embeddings only → esm
├─ PLM embedding homology → plmsearch / deepblast
├─ Have AFDB/PDB structures → foldseek (coords)
└─ Classical sequence → mmseqs2 / diamond
```

## Validation, recovery, and provenance

Reconcile input proteins and 3Di records, lengths, invalid/ambiguous residues,
failed translations, truncation, device precision, and CPU/GPU reproducibility.
Use structural benchmarks or known controls to assess downstream retrieval.
Remember that 3Di-only databases lack coordinates and cannot provide TM-score,
LDDT, interfaces, residue geometry, or experimental structure confidence.

Use fresh output after changing FASTA, model, software, device, or options.
Record ProstT5/Hugging Face revision and checksum, Foldseek/transformers/torch
versions, hardware/precision, input checksum, command/logs, database components,
3Di checksum and failures. Predicted 3Di is a model representation, not a solved
structure or validated function.

## Related skills

`protein-language-model` · `foldseek` · `esm` · `esmc` · `saprot` ·
`plmsearch` · `deepblast` · `unicore` · `metagenomics-llm` ·
`homology-search` · `tool-selection`
