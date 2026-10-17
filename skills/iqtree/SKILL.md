---
name: iqtree
description: >
  IQ-TREE 2 — fast maximum-likelihood phylogenetic inference with model selection and
  ultrafast bootstrap. Use when: (1) Building publication-grade trees from marker or
  concatenated MSAs, (2) Following PhyloPhlAn / custom alignments for MAG phylogenomics,
  (3) Replacing draft FastTree topologies for final figures.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "IQ-TREE, phylogeny, maximum-likelihood, tree, bootstrap"
  metagenomics.upstream: "https://github.com/iqtree/iqtree2"
  metagenomics.stage: "taxonomy"
---

# IQ-TREE 2

Upstream: [iqtree/iqtree2](https://github.com/iqtree/iqtree2) · http://www.iqtree.org

## Citation

Minh, B. Q. *et al.* IQ-TREE 2: new models and efficient methods for phylogenetic
inference in the genomic era. *Mol. Biol. Evol.* **37**, 1530–1534 (2020).
https://doi.org/10.1093/molbev/msaa015

Nguyen, L.-T., Schmidt, H. A., von Haeseler, A. & Minh, B. Q. IQ-TREE: a fast
and effective stochastic algorithm for estimating maximum-likelihood phylogenies.
*Mol. Biol. Evol.* **32**, 268–274 (2015). https://doi.org/10.1093/molbev/msu300

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Default **ML tree** engine for metagenomic phylogenomics after you have a
clean MSA (from `phylophlan`, marker genes, or curated orthologs). ModelFinder
chooses substitution models; UFBoot gives rapid support values — report both
model and support method.

| vs | Prefer IQ-TREE when |
|----|---------------------|
| `fasttree` | Final / publication trees |
| `gtdbtk` | You need a custom tree, not only GTDB placement |
| `lucaphylo` | MSA-based classical phylogeny is appropriate |

Garbage in → garbage trees: remove poor MAGs, dubious alignments, and
outgroup contamination first.

## How to run

```bash
# typical: MSA in PHYLIP/FASTA → ML tree + UFBoot
iqtree2 -s markers.fa -m MFP -B 1000 -T AUTO -prefix temp/iqtree/run
# outputs: *.treefile, *.iqtree, *.log — pin version in Methods
```

## Key parameters

| Setting | Notes |
|---------|-------|
| `-m MFP` | ModelFinder Plus — state selected model |
| `-B 1000` | Ultrafast bootstrap replicates |
| `-T` | Threads |
| Partition models | Use when concatenating heterogeneous markers |

## Decision tree

```text
Need a sequence-based tree?
├─ Draft / exploratory large MSA → fasttree
├─ Publication ML tree → iqtree
├─ Genome set workflow → phylophlan (± iqtree backend)
└─ MSA impossible / extreme divergence → lucaphylo
```

## Related skills

`phylogenomics` · `fasttree` · `phylophlan` · `gtdbtk` · `lucaphylo` ·
`mag-qc` · `tool-selection`
