---
name: mmseqs2
description: >
  Ultra-fast protein search, clustering, and contig taxonomy. Use this skill when working with mmseqs2: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/soedinglab/MMseqs2. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['cluster', 'search', 'taxonomy']
upstream: https://github.com/soedinglab/MMseqs2
stage: function
---

# MMseqs2

Upstream: [MMseqs2](https://github.com/soedinglab/MMseqs2)

## Citation

Mirdita, M. *et al.* Fast and sensitive taxonomic assignment to metagenomic contigs. *Bioinformatics* **37**, 3029–3031 (2021). https://doi.org/10.1093/bioinformatics/btab184

Steinegger, M. & Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. *Nat. Biotechnol.* **35**, 1026–1028 (2017). https://doi.org/10.1038/nbt.3988

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Use for large-scale clustering (alternative/complement to CD-HIT) and `easy-taxonomy` on contigs. Memory/DB layout matters — pin release.

## How to run

```bash
conda install -c bioconda mmseqs2  # if packaged; else follow upstream

mmseqs easy-cluster genes.faa temp/mmseqs/clu temp/mmseqs/tmp --min-seq-id 0.9 -c 0.8
mmseqs easy-taxonomy contigs.fa taxonomyDB temp/mmseqs/tax temp/mmseqs/tmp
```

## Key parameters

| easy-cluster | NR genes | |
| easy-taxonomy | contigs | Needs taxDB |

## Decision notes

- Stage: **function** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

cd-hit · diamond · eggnog-mapper · kraken2 · `tool-selection` · `metagenomics-workflow`
