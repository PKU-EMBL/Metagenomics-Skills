---
name: omg
description: >
  Open MetaGenomic (OMG) corpus and gLM2 mixed-modality genomic language model — large
  pretraining data from IMG + MGnify (Tbp-scale DNA + billions of CDS). Use when: (1)
  Pretraining or evaluating genomic LMs, (2) Using gLM2 embeddings for function /
  coevolution / regulatory syntax, (3) Distinguishing ML corpora from study reanalysis.
  Hugging Face: tattabio/OMG, tattabio/gLM2_650M.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "OMG, gLM2, foundation-model, pretraining, HuggingFace"
  metagenomics.upstream: "https://github.com/TattaBio/OMG"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "OMG revision c648c026; gLM2 revision 08754cba"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "dataset streaming and model APIs reviewed; not executed here"
---

# OMG corpus / gLM2

Dataset: https://huggingface.co/datasets/tattabio/OMG ·
Model: https://huggingface.co/tattabio/gLM2_650M ·
Code: [TattaBio/OMG](https://github.com/TattaBio/OMG)

## Citation

Cornman, A. *et al.* The OMG dataset: An Open MetaGenomic corpus for
mixed-modality genomic language modeling. *bioRxiv*
https://doi.org/10.1101/2024.08.14.607850 (2024).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `metagenomics-llm`.

## Analytical thinking

OMG aggregates and filters metagenomic sequence from **JGI IMG** and **EMBL
MGnify** into a mixed-modality corpus (amino acids for CDS, nucleic acids for
intergenic regions; ~3.1 Tbp + ~3.3B CDS in the preprint) for genomic language
modeling. **gLM2** (Tatta Bio / Hwang et al.) uses genomic context for
functional representations and can capture **cross-protein coevolutionary**
signal better than single-protein ESM2 or short-context Evo-1 in the OMG/gLM2
analyses — still not a substitute for experimental contacts or classical
taxonomy.

| Use | Yes | No |
|-----|-----|-----|
| Pretrain / fine-tune / embed with gLM2 | ✓ | |
| Replace MetaPhlAn/Kraken for your cohort | | ✗ |
| Cite as “we downloaded OMG instead of ENA runs” for a clinical study | | ✗ without justification |

Always separate **ML corpus access** from **biological sample reanalysis**
(`sra-ena`, `mgnify` analyses).

## How to access

Stream and schema-check before any bulk download:

```python
from datasets import load_dataset

revision = "c648c026ec46ffa2614610a59cb3c8187cdc984f"
ds = load_dataset("tattabio/OMG", revision=revision,
                  split="train", streaming=True)
row = next(iter(ds))
required = {"CDS_seqs", "IGS_seqs", "CDS_position_ids", "IGS_position_ids"}
assert required <= row.keys()
assert len(row["CDS_seqs"]) == len(row["CDS_position_ids"])
assert len(row["IGS_seqs"]) == len(row["IGS_position_ids"])
print(revision, sorted(row), len(row["CDS_seqs"]), len(row["IGS_seqs"]))
```

For gLM2, use `AutoModel`/`AutoTokenizer` with `trust_remote_code=True` and immutable revision `08754cba59a1f97d517f873fad6c672d2b1abdc7`; uppercase amino acids, lowercase nucleotides, and prepend each genomic element with `<+>` or `<->` as required by the model card. Review remote code before loading. Expect large disk/GPU use.

## Decision tree

```text
Need metagenome-scale LM resources?
├─ Pretrain corpus / gLM2 embeddings → omg
├─ DNA NT / DNABERT-2 / Caduceus / Evo 2 → genome-language-model
├─ Protein remote search only → plmsearch / deepblast
└─ Public study FASTQ → sra-ena / mgnify (not OMG)
```

## Validation, recovery, and provenance

Validate schema, element-position ordering, CDS/IGS counts, strand tokens, character case/alphabet, context truncation and duplicate/leakage policy. For embeddings require finite tensors and ID-to-row maps; for fine-tuning freeze taxonomic/source-aware splits and compare non-LM baselines. Streaming one row validates access/schema only, not corpus completeness.

Record dataset/model immutable revisions, dataset card/license and access date, `datasets`/Transformers/PyTorch/CUDA versions, filters/shards/splits, code/seeds, downloaded artifact hashes and derived-output checksums. OMG records are an ML corpus with source-specific biases; gLM2 outputs are predictions, not cohort observations.

## Related skills

`genome-language-model` · `metagenomics-llm` · `nucleotide-transformer` ·
`dnabert2` · `caduceus` · `evo2` · `mgnify` · `public-databases` ·
`plmsearch` · `spacedust` · `eggnog-mapper`
