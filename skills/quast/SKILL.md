---
name: quast
description: >
  Assembly quality assessment (contiguity, misassemblies; metaQUAST for metagenomes). Use this skill when working with quast: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/ablab/quast. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['assembly', 'qc', 'quast']
upstream: https://github.com/ablab/quast
stage: assessment
---

# QUAST / metaQUAST

Upstream: [QUAST / metaQUAST](https://github.com/ablab/quast)

## Citation

Mikheenko, A., Saveliev, V. & Gurevich, A. MetaQUAST: evaluation of metagenome assemblies. *Bioinformatics* **32**, 1088–1090 (2016). https://doi.org/10.1093/bioinformatics/btv697

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Run after assembly **before** heavy binning to catch overly fragmented graphs.
metaQUAST adds reference-based misassembly metrics when suitable genomes exist;
without refs you still get contiguity stats (N50, length histograms).

Contiguity ≠ biological correctness. Do **not** choose assemblers on N50 alone —
combine with mapping rate, bin recovery (`mag-qc`), and compute cost.

## How to run

```bash
metaquast.py contigs.fa -o temp/quast -t 16
# or quast.py for generic stats without refs
```

## Key parameters

| Mode | When |
|------|------|
| `metaquast.py` | Metagenomes; optional reference set |
| `quast.py` | Quick contiguity without refs |
| Threads `-t` | Scale with CPU |

## Decision tree

```text
Assembly assessment?
├─ Have references → metaQUAST
├─ No refs → QUAST stats + downstream bin QC
└─ CAMI gold standards → cami / AMBER (not QUAST alone)
```

## Related skills

`megahit` · `metaspades` · `metaflye` · `metamdbg` · `mag-qc` · `cami` ·
`tool-selection`
