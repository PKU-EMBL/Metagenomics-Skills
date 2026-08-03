---
name: plass
description: >
  PLASS — protein-level assembler that recovers many more protein sequences
  from metagenomic reads than nucleotide assembly alone (Söding / Steinegger).
  Same package ships PenguiN (protein-guided nucleotide assembly). Use when:
  (1) Maximizing protein catalogue recovery from reads, (2) Building inputs for
  MMseqs/HH-suite/BFD-style search, (3) Viral/strain-resolved assemblies via
  PenguiN. Upstream: https://github.com/soedinglab/plass.
  Route via homology-search / assembly stages.
license: MIT
category: analysis-tools
tags: [PLASS, PenguiN, assembly, protein, metagenomics]
upstream: https://github.com/soedinglab/plass
stage: assembly
---

# PLASS / PenguiN

Upstream: [soedinglab/plass](https://github.com/soedinglab/plass)

## Citation

Steinegger, M., Mirdita, M. & Söding, J. Protein-level assembly increases
protein sequence recovery from metagenomic samples manyfold. *Nat. Methods*
**16**, 603–606 (2019). https://doi.org/10.1038/s41592-019-0437-4

Jochheim, A. *et al.* Strain-resolved de-novo metagenomic assembly of viral
genomes and microbial 16S rRNAs. *Microbiome* **12**, 187 (2024).
https://doi.org/10.1186/s40168-024-01904-y

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Nucleotide assemblers miss many coding sequences. **PLASS** assembles at the
**protein** level from reads → denser protein catalogues for search/annotation.
**PenguiN** uses protein guidance for nucleotide assemblies (viruses/16S use
cases in the paper). Complements MEGAHIT/metaSPAdes, does not replace contig
binning paths.

Soil/Marine reference catalogues from PLASS and BFD HH-suite DBs are linked
from upstream.

## How to run

```bash
conda install -c bioconda plass
plass assemble reads_1.fastq.gz reads_2.fastq.gz assembly.fas tmp
# single-end
plass assemble reads.fastq.gz assembly.fas tmp
# PenguiN nucleotide workflows — see upstream (penguin guided_nuclassemble …)
```

## Decision tree

```text
Goal from metagenomic reads?
├─ Contigs for binning → megahit / metaspades
├─ Maximize protein recovery for search → plass
├─ Protein-guided nt assembly (viruses/…) → penguin (plass package)
└─ Then search proteins → mmseqs2 / hh-suite / foldseek
```

## Related skills

`megahit` · `metaspades` · `mmseqs2` · `hh-suite` · `homology-search` ·
`prodigal` · `tool-selection`
