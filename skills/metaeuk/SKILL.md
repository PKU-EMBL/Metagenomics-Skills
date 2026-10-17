---
name: metaeuk
description: >
  MetaEuk — sensitive gene discovery and annotation on eukaryotic metagenomic contigs
  using MMseqs2 homology + exon dynamic programming (Söding lab). Use when: (1) Calling
  genes on eukaryotic contigs/MAGs, (2) Annotating via protein or profile targets, (3)
  Contig taxonomy via MetaEuk predictions. Not a prokaryotic default (prefer
  prodigal/bakta).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MetaEuk, eukaryotic, gene-prediction, MMseqs2, metagenomics"
  metagenomics.upstream: "https://github.com/soedinglab/metaeuk"
  metagenomics.stage: "function"
---

# MetaEuk

Upstream: [soedinglab/metaeuk](https://github.com/soedinglab/metaeuk)

## Citation

Levy Karin, E., Mirdita, M. & Söding, J. MetaEuk—sensitive, high-throughput
gene discovery and annotation for large-scale eukaryotic metagenomics.
*Microbiome* **8**, 48 (2020). https://doi.org/10.1186/s40168-020-00808-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Prokaryotic callers (`prodigal`) miss spliced eukaryotic genes. MetaEuk uses
**MMseqs2** searches against protein/profile DBs plus exon-set DP — for
eukaryotic contigs and microeukaryote MAGs.

| vs | Prefer MetaEuk when |
|----|---------------------|
| `prodigal` / `bakta` | Eukaryotic / spliced genes |
| `mmseqs2` alone | Need gene models (FASTA/GFF), not only hits |

## How to run

```bash
conda install -c bioconda metaeuk
metaeuk easy-predict contigs.fna proteins_or_profiles.faa predsResults tmp
# outputs: predsResults.fas, .codon.fas, .gff, headersMap.tsv
```

## Decision tree

```text
Gene calling on contigs?
├─ Prokaryotic → prodigal / bakta / prokka
├─ Eukaryotic metagenomes → metaeuk
└─ Then annotate → mmseqs2 / eggnog-mapper / foldseek
```

## Related skills

`mmseqs2` · `prodigal` · `bakta` · `homology-search` · `eggnog-mapper` ·
`tool-selection`
