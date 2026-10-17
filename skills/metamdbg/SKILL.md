---
name: metamdbg
description: >
  High-quality metagenome assembly from long accurate reads. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, hifi, long-read"
  metagenomics.upstream: "https://github.com/GaetanBenoitDev/metaMDBG"
  metagenomics.stage: "assembly"
---

# metaMDBG

Upstream: [metaMDBG](https://github.com/GaetanBenoitDev/metaMDBG)

## Citation

Benoit, G. *et al.* High-quality metagenome assembly from long accurate reads with metaMDBG. *Nat. Biotechnol.* **42**, 1378–1383 (2024). https://doi.org/10.1038/s41587-023-01983-6

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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
