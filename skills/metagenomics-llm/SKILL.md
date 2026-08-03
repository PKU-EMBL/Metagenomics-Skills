---
name: metagenomics-llm
description: >
  Route genomic / protein language models and AI-assisted annotation for
  shotgun metagenomics. Use when: (1) Choosing OMG/gLM2 vs classical homology,
  (2) Remote-homology search with PLMs (PLMSearch, DeepBLAST/TM-Vec),
  (3) Conserved gene-cluster discovery with structure-aware tools (Spacedust),
  (4) Distinguishing foundation-model pretraining corpora from SRA/MGnify
  study reanalysis, (5) Writing Methods limits for LLM/PLM claims. Child skills:
  omg, plmsearch, deepblast, spacedust, alphagem. For classical pipelines use
  metagenomics-workflow / tool-selection.
license: MIT
category: orchestration
tags: [LLM, PLM, gLM, foundation-model, AI, annotation, routing]
---

# Metagenomics × language models

Foundation models (nucleotide / protein / mixed-modality genomic LMs) are a
**parallel track** to QC→assembly→binning. They help when homology is remote,
functions are dark, or you need embeddings — they do **not** replace CheckM2,
GTDB-Tk, or abundance profilers.

## Analytical thinking

| Claim type | Prefer | Do not treat as |
|------------|--------|-----------------|
| Pretrain / fine-tune genomic LMs | `omg` (OMG corpus, gLM2) | Your sample’s taxonomy table |
| Remote protein homology (sequence-only) | `plmsearch`, `deepblast` | Experimental structure proof |
| Conserved gene neighborhoods / modules | `spacedust` (Foldseek-aware) | Operon wet-lab validation |
| GEM + structure/dark metabolism | `alphagem` (± `gapseq`/`vmh`) | Flux measurements |
| Classical KO/COG annotation | `eggnog-mapper`, `dram`, `kegg` | Obsolete — still primary for many papers |

Hard rules:

1. Embeddings / LM hits are **hypotheses** — pin model + checkpoint + DB
2. OMG/Hugging Face corpora ≠ ENA study reanalysis (`sra-ena` / `mgnify`)
3. Do not merge PLM rankings with BLAST/MMseqs tables unlabeled
4. GPU/memory needs differ wildly from KneadData/MEGAHIT nodes

## Decision tree

```text
AI / LM need in a metagenomics project?
│
├─ Pretraining data or mixed-modality gLM (gLM2)
│     → omg
├─ Find remote homologs from sequence alone
│     → plmsearch  or  deepblast (TM-Vec + alignment)
├─ Discover conserved gene clusters / functional modules
│     → spacedust
├─ Improve GEMs with structure / dark metabolism mining
│     → alphagem  (± gapseq, vmh)
├─ Classical function at catalogue scale
│     → eggnog-mapper / dram / humann
└─ Unsure
      → this skill + tool-selection
```

## Where it sits in the pipeline

```text
contigs / MAG proteins (after QC)
   ├─ classical: eggnog-mapper · diamond · mmseqs2
   └─ LM-assisted: plmsearch · deepblast · spacedust
genomic LM research / pretrain
   └─ omg (corpus) → gLM2 / other gLMs
metabolic models
   └─ gapseq · alphagem · vmh
```

## Methods caveats

- Report model name, size, checkpoint URL, prompt/embedding recipe, and date
- For dark-matter genes, state that LM annotations lack experimental support
- Prefer holding out known systems (e.g. defense) when claiming de novo discovery
  (`spacedust` vs `defensefinder` / PADLOC-style tools)

## Related skills

`omg` · `plmsearch` · `deepblast` · `spacedust` · `alphagem` · `eggnog-mapper` ·
`mmseqs2` · `diamond` · `dram` · `gapseq` · `defensefinder` · `public-databases` ·
`tool-selection` · `metagenomics-workflow`
