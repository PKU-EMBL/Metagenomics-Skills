---
name: phylogenomics
description: >
  Route phylogenetic and evolutionary analyses for shotgun metagenomics and MAGs:
  GTDB-Tk placement, genome/marker trees (PhyloPhlAn, IQ-TREE, FastTree), alignment-free
  PLM phylogeny (LucaPhylo), and ANI species boundaries (skani/FastANI). Use when
  building or interpreting trees, placing genomes, or choosing classical vs AI phylogeny
  — not for read profilers alone.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "phylogeny, tree, IQ-TREE, PhyloPhlAn, evolution, GTDB, routing"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "tree/placement/ANI routing reviewed; execution is delegated to child skills"
---

# Phylogenomics / evolutionary routing

Taxonomy labels, species ANI, and phylogenetic trees are **different claims**.
This hub routes evolutionary analyses after HQ genomes/MAGs exist.

## Analytical thinking

| Need | Prefer | Notes |
|------|--------|-------|
| Bacterial/archaeal MAG taxonomy | `gtdbtk` (+ `gtdb`) | Placement into GTDB; pin release |
| Multi-genome / MAG phylogeny | `phylophlan` | Marker sets + tree; feed `iqtree`/`fasttree` |
| Structural core-gene phylogeny | `unicore` | Foldseek/ProstT5 cores (Steinegger) |
| Publication-grade ML tree | `iqtree` | ModelFinder, UFBoot; after MSA |
| Fast approximate tree (large MSA) | `fasttree` | Screen / draft; upgrade to IQ-TREE for final |
| Alignment-free PLM / hyperbolic phylo | `lucaphylo` | Divergent proteins; experimental vs classical MSA |
| Species / strain boundary | `skani` · `fastani` | Distance, not a tree |
| Gene tree vs species tree | State clearly | HGT / paralogs break naive concatenation |

Hard rules:

1. Filter with `checkm2` / `gunc` before tree claims
2. Pin alignment + model + bootstrap / UFBoot settings
3. Do not treat ANI clusters as phylogenies
4. AI/PLM trees (`lucaphylo`) are complementary — do not replace GTDB-Tk Methods
   without justification
5. Research talks (evolutionary LMs, trajectory models) are frontier context only —
   not production defaults here

RAxML-NG / ASTRAL remain valid for specialized species-tree workflows; prefer
documenting them explicitly if used instead of IQ-TREE2.

## Required phylogenomic deliverable

Define taxa and outgroup, orthology/marker rule, alignment and trimming, partition
or concatenation strategy, substitution-model selection, support procedure,
rooting, missing-data and contamination filters, and tree purpose before running.
Deliver sequence/marker manifests, per-marker and concatenated alignments,
partition/model files, uncollapsed tree with branch lengths/support, logs,
software/database provenance, and a taxon inclusion/exclusion audit.

Inspect marker occupancy, paralogy, recombination/HGT, compositional bias,
long-branch attraction, topology sensitivity, support calibration, and gene-tree
conflict. Do not convert weakly supported placements, ANI thresholds, taxonomy
labels, or PLM distances into a resolved evolutionary history.

## Decision tree

```text
Evolutionary / tree need?
│
├─ Assign MAG to GTDB taxonomy → gtdbtk
├─ Build genome phylogeny from many MAGs → phylophlan
│     ├─ Draft / huge MSA → fasttree
│     └─ Final ML tree → iqtree
├─ Structural core genes / 3Di → unicore
├─ Species demarcation (ANI) → skani / fastani
├─ Highly divergent proteins, MSA fails → lucaphylo (± classical backup)
└─ Homology search only (not a tree) → homology-search
```

## Related skills

`gtdbtk` · `gtdb` · `phylophlan` · `unicore` · `iqtree` · `fasttree` ·
`lucaphylo` · `foldseek` · `foldmason` · `skani` · `fastani` ·
`homology-search` · `metagenomics-llm` · `mag-qc` · `tool-selection`
