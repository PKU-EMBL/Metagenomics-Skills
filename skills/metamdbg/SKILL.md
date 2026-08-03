---
name: metamdbg
description: >
  High-quality metagenome assembly from long accurate reads. Use this skill when working with metamdbg: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/GaetanBenoitDev/metaMDBG. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['assembly', 'hifi', 'long-read']
upstream: https://github.com/GaetanBenoitDev/metaMDBG
stage: assembly
---

# metaMDBG

Upstream: [metaMDBG](https://github.com/GaetanBenoitDev/metaMDBG)

## Citation

Benoit, G. *et al.* High-quality metagenome assembly from long accurate reads with metaMDBG. *Nat. Biotechnol.* **42**, 1378–1383 (2024). https://doi.org/10.1038/s41587-023-01983-6

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Preferred for PacBio HiFi / accurate long-read metagenomes. Pair with long-read-aware binning (SemiBin2/LorBin/BASALT).

## How to run

```bash
conda install -c bioconda metamdbg  # if packaged; else follow upstream

metaMDBG asm --out temp/asm/metamdbg --in reads.fastq.gz --threads 32
```

## Key parameters

| accurate long reads | HiFi/duplex | |
| check upstream CLI | version-sensitive | |

## Decision notes

- Stage: **assembly** (long accurate reads)
- Prefer HiFi / accurate long reads; follow with long-read binning (`lorbin` / SemiBin2 LR)
- Pin version; report polish status

## Related skills

metaflye · minimap2 · semibin2 · basalt · `tool-selection` · `metagenomics-workflow`
