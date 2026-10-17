---
name: phylophlan
description: >
  PhyloPhlAn 3 — precise phylogenetic analysis of microbial isolates and
  metagenome-assembled genomes via marker sets, alignment, and tree building. Use when:
  (1) Reconstructing phylogenies across many MAGs/genomes, (2) Contextualizing novel
  lineages beyond a single GTDB-Tk row, (3) Generating inputs for IQ-TREE/FastTree.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PhyloPhlAn, phylogeny, MAG, markers, tree"
  metagenomics.upstream: "https://github.com/biobakery/phylophlan"
  metagenomics.stage: "taxonomy"
---

# PhyloPhlAn

Upstream: [biobakery/phylophlan](https://github.com/biobakery/phylophlan) ·
https://huttenhower.sph.harvard.edu/phylophlan

## Citation

Asnicar, F. *et al.* Precise phylogenetic analysis of microbial isolates and
genomes from metagenomes using PhyloPhlAn 3.0. *Nat. Commun.* **11**, 2500
(2020). https://doi.org/10.1038/s41467-020-16366-7

Segata, N. *et al.* PhyloPhlAn is a new method for improved phylogenetic and
taxonomic placement of microbes. *Nat. Commun.* **4**, 2304 (2013).
https://doi.org/10.1038/ncomms3304

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

PhyloPhlAn automates **marker selection → alignment → tree** for isolates and
MAGs. Use when GTDB-Tk classification is not enough (custom clades, publication
trees, multi-study genome sets). Tree quality still depends on genome QC and
chosen database/config.

| vs | Prefer PhyloPhlAn when |
|----|------------------------|
| `gtdbtk` | Need a reconstructed phylogeny, not only taxonomy labels |
| Manual `iqtree` | Want an end-to-end MAG phylogenomics workflow |
| `lucaphylo` | Standard marker MSA phylogeny is appropriate |

## How to run

```bash
conda install -c bioconda phylophlan
# follow upstream tutorials for database setup + config
# typical: genomes/ → phylophlan → MSA + tree (optionally refine with iqtree)
phylophlan -i genomes/ -o temp/phylophlan/ -d phylophlan \
  --diversity medium -f YOUR.cfg --nproc 16
```

Exact flags depend on installed PhyloPhlAn configs — pin version and config
name in Methods.

## Decision tree

```text
Many MAGs need a phylogeny?
├─ Taxonomy labels only → gtdbtk
├─ Marker-based genome tree workflow → phylophlan
│     └─ Optional final ML → iqtree
├─ Single MSA already in hand → iqtree / fasttree
└─ Extreme divergence / no MSA → lucaphylo
```

## Related skills

`phylogenomics` · `iqtree` · `fasttree` · `gtdbtk` · `gtdb` · `mag-qc` ·
`checkm2` · `tool-selection`
