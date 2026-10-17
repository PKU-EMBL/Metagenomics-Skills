---
name: saprot
description: >
  SaProt — Westlake University structure-aware protein language model using an AA+3Di
  (Foldseek) structure-aware vocabulary (ICLR 2024). Use when: (1) Structure-informed
  PLM embeddings for function / fitness / variant tasks, (2) Comparing against ESM-2
  with Foldseek SA tokens available, (3) SaProt 1.3B AA-only or SA-token workflows
  (incl. AFDB/OMG/NCBI-trained checkpoints). HF: westlake-repl/SaProt_*. Related
  Westlake tools (ProTrek, etc.) — cite separately if used.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "SaProt, Westlake, PLM, protein-language-model, Foldseek, 3Di, ICLR"
  metagenomics.upstream: "https://github.com/westlake-repl/SaProt"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot e91e485; SaProt_650M_AF2 revision d9b9ad00"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Hugging Face API reviewed; not executed here"
---

# SaProt (Westlake)

Upstream: [westlake-repl/SaProt](https://github.com/westlake-repl/SaProt) ·
HF: https://huggingface.co/westlake-repl ·
OpenReview: https://openreview.net/forum?id=6MRm3G4NiU

## Citation

Su, J. *et al.* SaProt: Protein Language Modeling with Structure-aware
Vocabulary. *International Conference on Learning Representations* (ICLR)
(2024). https://openreview.net/forum?id=6MRm3G4NiU

Preprint: https://doi.org/10.1101/2023.10.01.560349

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

SaProt builds a **structure-aware vocabulary**: residue tokens combined with
Foldseek **3Di** structure tokens (SA tokens), trained on large AF2/PDB-scale
structure–sequence corpora (Westlake REPL lab). Strong on many structure/function
downstream tasks when SA input is available.

Critical upstream caveats:

- **35M / 650M**: optimal with **SA-token** input; frozen AA-only embeddings are
  weak — fine-tune if forced to AA-only
- **1.3B** (e.g. `SaProt_1.3B_AFDB_OMG_NCBI`): works better with both SA and
  AA-only modes; metagenome-relevant OMG/NCBI mixing noted in checkpoint names
- SA tokens need structures or Foldseek 3Di — for FASTA→3Di production search
  prefer `foldseek` + `prostt5`; SaProt is the **PLM**, not a search engine

| vs | Prefer SaProt when |
|----|---------------------|
| `esm` / `esmc` | Have structures / SA tokens and want structure-aware PLM |
| `prostt5` | Downstream PLM tasks vs building Foldseek 3Di DBs |
| `plmsearch` | Embedding/finetune model vs remote-homology search wrapper |

Related Westlake releases (ProTrek, Pinal, Evolla, …) — mention only if the
project uses them; keep this skill focused on SaProt.

## How to run

SaProt expects two-character structure-aware tokens (amino acid plus Foldseek 3Di state); `#` masks low-confidence structure in the reviewed upstream convention.

```python
import torch
from transformers import EsmForMaskedLM, EsmTokenizer

repo = "westlake-repl/SaProt_650M_AF2"
revision = "d9b9ad00ef61c0990e611b2b43f2231c7de24b38"
tokenizer = EsmTokenizer.from_pretrained(repo, revision=revision)
model = EsmForMaskedLM.from_pretrained(repo, revision=revision).eval()
sa_sequence = "M#EvVpQpL#VyQdYaKv"
inputs = tokenizer(sa_sequence, return_tensors="pt")
with torch.inference_mode():
    output = model(**inputs)
assert output.logits.shape[:2] == inputs["input_ids"].shape
assert torch.isfinite(output.logits).all()
print(repo, revision, tokenizer.tokenize(sa_sequence), tuple(output.logits.shape))
```

Generate SA tokens from the exact structure/chain with the pinned Foldseek encoder, preserve residue mapping, and mask low-pLDDT AF2 regions under a declared threshold. Do not feed ordinary amino-acid strings to an SA-token analysis without using a documented sequence-only checkpoint/mode.

## Decision tree

```text
Structure-aware protein LM?
├─ AA+3Di SaProt (Westlake) → saprot
├─ Sequence-only modern embeddings → esmc (± esm)
├─ FASTA → Foldseek search → prostt5 + foldseek
└─ Remote homology ranking → plmsearch / deepblast
```

## Validation, recovery, and provenance

Require one-to-one amino-acid/3Di residue mapping, valid even-length SA strings, chain and structure IDs, confidence-mask accounting, finite tensors and stable sequence order. Compare against sequence-only ESM and structure-search baselines on leakage-resistant splits; inspect effects of low-confidence masking. A loaded model and high score do not validate function or mutation effects.

Record SaProt repository/checkpoint immutable revisions and license, Transformers/PyTorch/Foldseek versions, structure source and checksum, chain extraction, pLDDT threshold, token strings/checksums, device/dtype, pooling/head, code/seeds and outputs. Structure-aware predictions remain computational.

## Related skills

`protein-language-model` · `esmc` · `esm` · `prostt5` · `foldseek` ·
`plmsearch` · `omg` · `metagenomics-llm` · `tool-selection`
