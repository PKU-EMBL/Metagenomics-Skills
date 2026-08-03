---
name: prostt5
description: >
  ProstT5 — bilingual protein language model translating amino-acid sequences
  and Foldseek 3Di structure tokens (fine-tuned from ProtT5). Use when: (1)
  Building Foldseek DBs from FASTA via --prostt5-model, (2) Sequence-only
  structure-aware search without AlphaFold, (3) AA↔3Di representation tasks.
  Upstream: https://github.com/mheinzinger/ProstT5. HF: Rostlab/ProstT5.
  Parent ProtT5: Rostlab/prot_t5_xl_uniref50. Route via protein-language-model;
  production search usually via foldseek.
license: MIT
category: analysis-tools
tags: [ProstT5, ProtT5, PLM, protein-language-model, 3Di, Foldseek, Rostlab]
upstream: https://github.com/mheinzinger/ProstT5
stage: function
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

See also [docs/references.md](../../docs/references.md).

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

```bash
# preferred production path — Foldseek wraps ProstT5
foldseek databases ProstT5 weights tmp
foldseek createdb query.fasta queryDB --prostt5-model weights
# or:
foldseek easy-search query.fasta targetDB res.m8 tmp --prostt5-model weights
# GPU: --gpu 1 (Foldseek CUDA build); see foldseek skill

# standalone HF inference: follow mheinzinger/ProstT5 README
```

## Decision tree

```text
Need structure-aware protein search from FASTA?
├─ Yes, Foldseek production → foldseek + prostt5 weights
├─ AA embeddings only → esm
├─ PLM embedding homology → plmsearch / deepblast
├─ Have AFDB/PDB structures → foldseek (coords)
└─ Classical sequence → mmseqs2 / diamond
```

## Related skills

`protein-language-model` · `foldseek` · `esm` · `plmsearch` · `deepblast` ·
`unicore` · `metagenomics-llm` · `homology-search` · `tool-selection`
