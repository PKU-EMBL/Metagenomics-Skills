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

Steinegger, M. & Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. *Nat. Biotechnol.* **35**, 1026–1028 (2017). https://doi.org/10.1038/nbt.3988

Mirdita, M. *et al.* Fast and sensitive taxonomic assignment to metagenomic contigs. *Bioinformatics* **37**, 3029–3031 (2021). https://doi.org/10.1093/bioinformatics/btab184

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Two common metagenome uses:

| Mode | Role |
|------|------|
| `easy-cluster` / linclust | NR gene/protein catalogues (complement/alternative to `cd-hit`) |
| `easy-taxonomy` | Contig-level taxonomy vs a taxDB |

Also underlies many other tools' search stacks. Memory and DB layout matter —
pin release and sensitivity (`-s`).

| vs | Prefer MMseqs2 when |
|----|---------------------|
| `cd-hit` | Much larger catalogues / speed |
| `diamond` | Need MMseqs taxonomy workflows or linclust-scale clustering |
| `kraken2` | Contig taxonomy via proteins/profiles (different claim) |

## How to run

```bash
mmseqs easy-cluster genes.faa temp/mmseqs/clu temp/mmseqs/tmp \
  --min-seq-id 0.9 -c 0.8 --cov-mode 1
mmseqs easy-taxonomy contigs.fa taxonomyDB temp/mmseqs/tax temp/mmseqs/tmp
```

## Key parameters

| Setting | Notes |
|---------|-------|
| `--min-seq-id` / `-c` | Catalogue identity & coverage — declare for NR |
| taxDB | Required for easy-taxonomy; pin |
| tmp dir | Fast local disk |

## Decision tree

```text
Need clustering or contig taxonomy?
├─ Huge protein NR → mmseqs2 easy-cluster
├─ Classic small NR → cd-hit still fine
├─ Contig taxonomy → mmseqs2 easy-taxonomy
└─ BLASTP-like single search → diamond / mmseqs search
```

## Related skills

`cd-hit` · `diamond` · `eggnog-mapper` · `prodigal` · `kraken2` · `metabuli` ·
`tool-selection`
