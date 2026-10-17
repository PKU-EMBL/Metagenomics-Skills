---
name: fastani
description: >
  FastANI — alignment-free approximate mapping for high-throughput average nucleotide
  identity (ANI) among prokaryotic genomes/MAGs. Use when: (1) Reproducing literature
  that reports FastANI, (2) Pairwise/species-boundary ANI at moderate catalogue scales,
  (3) Comparing to skani for Methods. Prefer skani for very large MAG sets / incomplete
  genomes unless FastANI is required for compatibility.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ANI, FastANI, comparative-genomics"
  metagenomics.upstream: "https://github.com/ParBLiSS/FastANI"
  metagenomics.stage: "binning"
---

# FastANI

Upstream: [ParBLiSS/FastANI](https://github.com/ParBLiSS/FastANI)

## Citation

Jain, C., Rodriguez-R, L. M., Phillippy, A. M., Konstantinidis, K. T. & Aluru, S.
High throughput ANI analysis of 90K prokaryotic genomes reveals clear species
boundaries. *Nat. Commun.* **9**, 5114 (2018).
https://doi.org/10.1038/s41467-018-07641-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FastANI popularized scalable **~95% ANI species-boundary** analyses. Still widely
cited in Methods even when newer tools are faster.

| Tool | Prefer when |
|------|-------------|
| `skani` | Large MAG catalogues; incomplete MAGs; speed/memory |
| `fastani` | Compatibility with published FastANI thresholds / pipelines |
| `drep` | Dereplication workflow (may call ANI backends) |

State the ANI tool + version + cutoff (commonly 95% species; AF/alignment
fraction matters — report it).

## How to run

```bash
conda install -c bioconda fastani
fastani -q query.fa -r reference.fa -o temp/fastani/out.txt
# or --ql / --rl lists for many genomes
```

## Related skills

`skani` · `drep` · `gtdb` · `mgnify` · `coverm` · `tool-selection`
