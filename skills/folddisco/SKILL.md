---
name: folddisco
description: >
  Folddisco — fast discontinuous structural motif search across the protein
  universe (Steinegger lab). Use when: (1) Searching catalytic triads / zinc
  fingers / other short motifs in AFDB/PDB/ESM30, (2) Motif-level annotation
  after Foldseek fold hits, (3) Mining conserved geometry in MAG protein
  structures. Upstream: https://github.com/steineggerlab/folddisco.
  Web: https://search.foldseek.com/folddisco. Route via metagenomics-llm;
  complement foldseek (full-chain) and mmseqs2 (sequence).
license: MIT
category: analysis-tools
tags: [Folddisco, motif, structure-search, AFDB, Foldseek]
upstream: https://github.com/steineggerlab/folddisco
stage: mining
---

# Folddisco

Upstream: [steineggerlab/folddisco](https://github.com/steineggerlab/folddisco) ·
Web: https://search.foldseek.com/folddisco

## Citation

Kim, H., Kim, R. S., Mirdita, M., Yoon, J. & Steinegger, M. Structural motif
search across the protein universe with Folddisco. *Nat. Biotechnol.* (2026).
https://doi.org/10.1038/s41587-026-03162-9

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Foldseek finds similar **folds / chains**; many functions depend on a small
**discontinuous motif** (catalytic residues, metal sites). Folddisco indexes
geometric hashes so motif queries scale to AFDB50 / ESM30 / PDB. In the
Steinegger “levels of conservation” framing: sequence/fold (`mmseqs2` /
`foldseek`) → multimer (`foldseek` multimer) → **motif (`folddisco`)**.

| vs | Prefer Folddisco when |
|----|------------------------|
| `foldseek` | Motif / active-site geometry, not global fold TM |
| `mmseqs2` | Residues are discontinuous or sequence-divergent |
| HMM / PROSITE | Have a 3D motif definition from a structure |

Caveats: motif length limits (long selections fail on the web UI); hits need
manual residue chemistry checks; pin index version (v2 `*.tar.lz4` vs legacy).

## How to run

```bash
# example: catalytic triad against a prebuilt index
folddisco query -i index/h_sapiens_folddisco -p query/4CHA.pdb -q B57,B102,C195 -t 6

# whole-structure motif sampling (omit -q); long queries may use --sampling-ratio
folddisco query -i index/afdb50_v4_folddisco -p query.pdb -t 8 --skip-match

# prebuilt indices (examples): AFDB50, ESM30, PDB, Swiss-Prot
# https://opendata.mmseqs.org/folddisco/
```

Web: https://search.foldseek.com/folddisco

## Key parameters

| Setting | Notes |
|---------|-------|
| `-p` / `-q` | Query PDB/mmCIF and residue list (`B57,B102,C195`) |
| `-i` | Precomputed Folddisco index — pin release |
| `-d` / `-a` | Distance (Å) / angle (°) prefilter sensitivity |
| `--skip-match` | Geometric search without AA identity constraints |
| `--sampling-ratio` | Speed/sensitivity trade-off for long queries |

## Decision tree

```text
Structure-aware annotation need?
├─ Global fold / chain → foldseek
├─ Complex / interface → foldseek easy-multimersearch
├─ Short discontinuous motif → folddisco
├─ Sequence only → mmseqs2 / plmsearch
└─ Gene neighborhood modules → spacedust
```

## Related skills

`foldseek` · `metagenomics-llm` · `mmseqs2` · `spacedust` · `plmsearch` ·
`deepblast` · `microbial-mining` · `tool-selection`
