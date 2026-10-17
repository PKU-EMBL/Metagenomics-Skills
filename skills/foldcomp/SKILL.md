---
name: foldcomp
description: >
  Foldcomp — compress and index large protein structure sets (Steinegger lab) for
  efficient storage and random access before Foldseek-scale searches. Use when: (1)
  Archiving AFDB-scale PDB collections, (2) Reducing disk for structure search
  pipelines, (3) Extracting sequences/pLDDT from Foldcomp DBs. Route via homology-search
  with foldseek.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Foldcomp, structure, compression, AFDB, Foldseek"
  metagenomics.upstream: "https://github.com/steineggerlab/foldcomp"
  metagenomics.stage: "function"
---

# Foldcomp

Upstream: [steineggerlab/foldcomp](https://github.com/steineggerlab/foldcomp)

## Citation

Kim, H., Mirdita, M. & Steinegger, M. Foldcomp: a library and format for
compressing and indexing large protein structure sets. *Bioinformatics* **39**,
btad153 (2023). https://doi.org/10.1093/bioinformatics/btad153

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Structure search needs structures on disk. Foldcomp provides a compact
**format + index** for large PDB/mmCIF collections used with Foldseek-family
tools. Infrastructure skill — not a homology algorithm itself.

## How to run

```bash
# binaries: https://mmseqs.com/foldcomp  or pip package — see upstream
foldcomp compress input_structures/ structures.fcz
foldcomp decompress structures.fcz out_dir/
# subset decompress / extract AA or pLDDT — see upstream Usage
```

## Decision tree

```text
Many protein structures to store/search?
├─ Compress/index archive → foldcomp
├─ Search → foldseek / folddisco / foldmason
└─ Sequence-only path → foldseek + ProstT5
```

## Related skills

`foldseek` · `foldmason` · `folddisco` · `homology-search` · `tool-selection`
