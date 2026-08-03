---
name: protein-language-model
description: >
  Route protein language models (PLMs / pLMs) for metagenomics: representation
  models (ESM-2 / ESM family), bilingual sequence–structure models (ProstT5 /
  ProtT5), remote-homology search (PLMSearch, TM-Vec/DeepBLAST), and PLM
  phylogeny (LucaPhylo). Use when choosing AA embeddings, sequence→3Di for
  Foldseek, or PLM search — not for classical eggNOG/KEGG tables or DNA gLMs.
  Child skills: esm, prostt5, plmsearch, deepblast. DNA gLMs via
  genome-language-model. Structure search via foldseek / homology-search.
license: MIT
category: orchestration
tags: [protein-language-model, PLM, pLM, ESM, ProstT5, ProtT5, remote-homology]
---

# Protein language model

Protein foundation models are a **parallel track** to QC→assembly→binning and
to DNA `genome-language-model`. They provide AA embeddings, likelihoods,
sequence→3Di translation, or remote-homology rankings — they do **not** replace
eggNOG-mapper, DIAMOND/MMseqs2 catalogues, or Foldseek when structures exist.

PLM taxonomy for metagenomic proteins:

| Strategy | Role | Prefer here |
|----------|------|-------------|
| Representation PLM | Embeddings / MLM / property heads | `esm` (ESM-2 ± family) |
| Bilingual AA ↔ 3Di | Sequence→structure tokens for Foldseek | `prostt5` |
| Remote homology (sequence-only) | Dark / remote proteins | `plmsearch` · `deepblast` |
| Structure search (coords / AFDB) | Fold-level hits | `foldseek` (± `folddisco`) |
| Alignment-free PLM phylogeny | Divergent protein trees | `lucaphylo` |
| DNA / mixed-modality gLM | Contigs / genomes | `genome-language-model` |

## Analytical thinking

| Claim | Prefer | Do not treat as |
|-------|--------|-----------------|
| General AA embeddings / ESM Atlas context | `esm` | Taxonomy profiler |
| FASTA → Foldseek 3Di without AF | `prostt5` / `foldseek --prostt5-model` | Experimental structure |
| Remote homologs, sequence-only PLM | `plmsearch` | Wet-lab function proof |
| TM-score-like search + structural align | `deepblast` | Solved PDB coordinates |
| Have AFDB/PDB structures | `foldseek` | PLM embedding distance alone |
| Hyperbolic PLM placement | `lucaphylo` | Default MAG taxonomy (`gtdbtk`) |
| Classical KO/COG at catalogue scale | `eggnog-mapper` / `diamond` | Obsolete — still primary |

Hard rules:

1. Pin model name, size, checkpoint URL, and license
2. Do not merge PLM / Foldseek / BLAST–MMseqs tables unlabeled
3. ProstT5 3Di DBs lack Cα — no TM-score / LDDT features that need coordinates
4. Low-confidence embeddings and over-long dark ORFs are common failure modes
5. GPU needs for large PLMs differ from KneadData/MEGAHIT nodes

## Decision tree

```text
Protein language model need?
│
├─ AA embeddings / ESM-2 family → esm
├─ Sequence → 3Di for Foldseek → prostt5 (± foldseek)
├─ Remote homology, sequence-only → plmsearch
├─ TM-score search + structural alignment → deepblast
├─ Have structures / AFDB → foldseek (± folddisco)
├─ PLM phylogeny (no reliable MSA) → lucaphylo
├─ Classical function tables → eggnog-mapper / dram / humann
├─ DNA genome LMs → genome-language-model
└─ Unsure → this hub + metagenomics-llm / homology-search
```

## Related skills

`esm` · `prostt5` · `plmsearch` · `deepblast` · `lucaphylo` · `foldseek` ·
`genome-language-model` · `metagenomics-llm` · `homology-search` ·
`eggnog-mapper` · `public-databases` · `tool-selection`
