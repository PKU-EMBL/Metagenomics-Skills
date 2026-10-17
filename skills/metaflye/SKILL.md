---
name: metaflye
description: >
  Long-read metagenome assembly with Flye/metaFlye. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, long-read"
  metagenomics.upstream: "https://github.com/fenderglass/Flye"
  metagenomics.stage: "assembly"
---

# metaFlye

Upstream: [metaFlye](https://github.com/fenderglass/Flye)

## Citation

Kolmogorov, M. *et al.* metaFlye: scalable long-read metagenome assembly using repeat graphs. *Nat. Methods* **17**, 1103–1110 (2020). https://doi.org/10.1038/s41592-020-00971-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Primary long-read metagenome assembler for noisy ONT/PacBio CLR. For HiFi prefer metaMDBG/hifiasm-meta. Still map reads back for binning.

## How to run

```bash
conda install -c conda-forge -c bioconda flye

flye --meta --nano-raw reads.fastq.gz --out-dir temp/asm/flye -t 32
# or --pacbio-raw / --nano-hq per chemistry
```

## Key parameters

| `--meta` | metagenome mode | Required |
| read type flag | match chemistry | |

## Decision notes

- Stage: **assembly** (long-read metagenomes)
- Prefer ONT/PacBio community assemblies; polish when chemistry requires
- Downstream: long-read-aware binning (`lorbin`, SemiBin2 LR)

## Related skills

minimap2 · metamdbg · megahit · metaspades · `tool-selection` · `metagenomics-workflow`
