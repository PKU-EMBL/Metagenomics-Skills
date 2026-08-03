---
name: colabfold
description: >
  ColabFold — accessible AlphaFold2/Multimer structure prediction with fast
  MMseqs2 MSAs (Steinegger / Mirdita / Ovchinnikov). Use when: (1) Predicting
  structures for MAG proteins before Foldseek, (2) Batch folding with
  colabfold_batch / LocalColabFold, (3) Generating MSAs for structure search.
  Upstream: https://github.com/sokrypton/ColabFold. Route via homology-search;
  pair with foldseek / foldcomp.
license: MIT
category: analysis-tools
tags: [ColabFold, AlphaFold, structure, MSA, MMseqs2]
upstream: https://github.com/sokrypton/ColabFold
stage: function
---

# ColabFold

Upstream: [sokrypton/ColabFold](https://github.com/sokrypton/ColabFold) ·
Local installer: [YoshitakaMo/localcolabfold](https://github.com/YoshitakaMo/localcolabfold)

## Citation

Mirdita, M. *et al.* ColabFold: making protein folding accessible to all.
*Nat. Methods* **19**, 679–682 (2022). https://doi.org/10.1038/s41592-022-01488-1

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

ColabFold supplies **structures** that power `foldseek` / `folddisco` /
`foldmason` / Foldseek-Multimer. For many dark ORFs, Foldseek+ProstT5 from
FASTA is faster than per-protein ColabFold — use ColabFold when you need
full models, complexes, or high-priority candidates.

| vs | Prefer ColabFold when |
|----|------------------------|
| `foldseek` + ProstT5 | Need 3D models / multimers / pLDDT maps |
| AFDB download only | Your sequences are absent from AFDB |

Filter low pLDDT before structure search. Pin ColabFold / AlphaFold params and
MSA source (public server vs local).

## How to run

```bash
# batch (after conda/pip or LocalColabFold install)
colabfold_batch input_sequences.fasta out_dir
# MSA only, then predict
colabfold_batch input_sequences.fasta out_dir --msa-only
colabfold_batch input_sequences.fasta out_dir
```

## Decision tree

```text
Need structures for MAG proteins?
├─ Already in AFDB → download / foldseek databases
├─ Priority ORFs / complexes → colabfold → foldseek
├─ Fast sequence→3Di without folding → foldseek --prostt5-model
└─ Store many PDBs compactly → foldcomp
```

## Related skills

`foldseek` · `folddisco` · `foldmason` · `foldcomp` · `hh-suite` · `mmseqs2` ·
`homology-search` · `tool-selection`
