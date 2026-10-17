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

```bash
# Hugging Face datasets / transformers patterns — verify current API
# huggingface-cli download tattabio/OMG
# or datasets.load_dataset("tattabio/OMG")
# gLM2_650M weights: tattabio/gLM2_650M
```

Pin dataset revision + model checkpoint in Methods. Expect large disk and GPU.

## Decision tree

```text
Need metagenome-scale LM resources?
├─ Pretrain corpus / gLM2 embeddings → omg
├─ DNA NT / DNABERT-2 / Caduceus / Evo 2 → genome-language-model
├─ Protein remote search only → plmsearch / deepblast
└─ Public study FASTQ → sra-ena / mgnify (not OMG)
```

## Related skills

`genome-language-model` · `metagenomics-llm` · `nucleotide-transformer` ·
`dnabert2` · `caduceus` · `evo2` · `mgnify` · `public-databases` ·
`plmsearch` · `spacedust` · `eggnog-mapper`
