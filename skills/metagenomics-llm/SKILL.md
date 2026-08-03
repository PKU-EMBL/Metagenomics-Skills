---
name: metagenomics-llm
description: >
  Route genomic/protein language models and Steinegger-lab structure/sequence
  search for shotgun metagenomics. Use when: (1) Choosing gLMs vs PLMs vs
  classical homology, (2) MMseqs2 vs Foldseek vs PLM search, (3) Spacedust /
  AlphaGEM, (4) Distinguishing foundation-model corpora from SRA/MGnify
  reanalysis. For DNA gLMs use genome-language-model (omg, nucleotide-transformer,
  dnabert2, caduceus, evo2). Classical pipelines: metagenomics-workflow /
  tool-selection.
license: MIT
category: orchestration
tags: [LLM, PLM, gLM, Foldseek, MMseqs2, Folddisco, structure-search, AI]
---

# Metagenomics × LMs & structure search

Foundation models and **structure-aware search** (Steinegger / Söding stack)
are a **parallel track** to QC→assembly→binning. They help when homology is
remote, functions are dark, or you need embeddings — they do **not** replace
CheckM2, GTDB-Tk, or abundance profilers.

For **genome language models** (NT/NTv3, DNABERT-2, Caduceus, Evo 2, OMG/gLM2)
prefer the dedicated hub `genome-language-model`.

## Analytical thinking

### Steinegger stack (sequence → fold → multimer → motif)

| Conservation level | Prefer | Typical claim |
|--------------------|--------|---------------|
| Amino-acid sequence | `mmseqs2` (± `diamond`) | Catalogue search, NR, contig taxonomy |
| Single-chain fold | `foldseek` | AFDB/PDB structural homologs; ProstT5 from FASTA |
| Multimer / interface | `foldseek` `easy-multimersearch` | Complex TM / chain pairing |
| Local structural motif | `folddisco` | Catalytic / metal-site geometry |
| Gene neighborhood modules | `spacedust` | Conserved clusters (Foldseek-aware) |

### Language models & dark metabolism

| Claim type | Prefer | Do not treat as |
|------------|--------|-----------------|
| Genome language models (route all gLMs) | `genome-language-model` | Taxonomy or abundance tables |
| Metagenomic corpus + gLM2 | `omg` | ENA study reanalysis |
| Nucleotide Transformer / NTv3 | `nucleotide-transformer` | Experimental genome annotation |
| DNABERT-2 / Caduceus | `dnabert2` / `caduceus` | Taxonomy profiler |
| Generative long-context DNA (Evo 2) | `evo2` | Contig assembly quality |
| Remote protein homology (sequence-only PLM) | `plmsearch`, `deepblast` | Experimental structure proof |
| GEM + structure/dark metabolism | `alphagem` (± `gapseq`/`vmh`) | Flux measurements |
| Classical KO/COG annotation | `eggnog-mapper`, `dram`, `kegg` | Obsolete — still primary for many papers |

Hard rules:

1. Embeddings / LM / structure hits are **hypotheses** — pin model + DB + software
2. OMG/Hugging Face corpora ≠ ENA study reanalysis (`sra-ena` / `mgnify`)
3. Do not merge PLM / Foldseek rankings with BLAST/MMseqs tables unlabeled
4. GPU/memory needs differ wildly from KneadData/MEGAHIT nodes
5. Low pLDDT structures and over-long Folddisco motifs are common failure modes

## Decision tree

```text
AI / homology need in a metagenomics project?
│
├─ Genome language models (NT, DNABERT-2, Caduceus, Evo 2, gLM2, …)
│     → genome-language-model
├─ Sequence catalogue / contig taxonomy
│     → mmseqs2
├─ Structure search (AFDB/PDB) or ProstT5 from FASTA
│     → foldseek
├─ Multi-chain complexes / interfaces
│     → foldseek easy-multimersearch
├─ Short discontinuous motifs
│     → folddisco
├─ Remote homologs from sequence alone (PLM)
│     → plmsearch  or  deepblast (TM-Vec + alignment)
├─ Conserved gene clusters / functional modules
│     → spacedust
├─ Improve GEMs with structure / dark metabolism mining
│     → alphagem  (± gapseq, vmh)
├─ Classical function at catalogue scale
│     → eggnog-mapper / dram / humann
├─ Full homology-search menu (vector DB, Phylign, …)
│     → homology-search
├─ Trees / phylogenomics
│     → phylogenomics
└─ Unsure
      → this skill + tool-selection
```

## Where it sits in the pipeline

```text
contigs / MAG proteins (after QC)
   ├─ classical: eggnog-mapper · diamond · mmseqs2
   ├─ structure: foldseek · folddisco · spacedust
   ├─ vector DB / genome warehouse search → homology-search
   └─ LM-assisted: plmsearch · deepblast
genome language models
   └─ genome-language-model → omg · nucleotide-transformer · dnabert2 · caduceus · evo2
metabolic models
   └─ gapseq · alphagem · vmh
trees / evolution
   └─ phylogenomics
```

## Methods caveats

- Report software version, database release, and (for LMs) checkpoint URL
- For dark-matter genes, state that LM/structure annotations lack wet-lab support
- Prefer holding out known systems when claiming de novo discovery
  (`spacedust` vs `defensefinder` / PADLOC-style tools)
- Foldseek-Multimer metagenomic CRISPR–Cas examples illustrate sensitivity at
  <20% sequence identity — still validate priority systems

## Related skills

`genome-language-model` · `omg` · `nucleotide-transformer` · `dnabert2` ·
`caduceus` · `evo2` · `homology-search` · `phylogenomics` · `mmseqs2` ·
`foldseek` · `folddisco` · `erast` · `plmsearch` · `deepblast` · `spacedust` ·
`alphagem` · `eggnog-mapper` · `public-databases` · `tool-selection` ·
`metagenomics-workflow`
