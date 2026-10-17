---
name: macrel
description: >
  Screen genomes and metagenomes for antimicrobial peptides (AMPs). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "AMP, antimicrobial-peptide, genome-mining"
  metagenomics.upstream: "https://github.com/BigDataBiology/macrel"
  metagenomics.stage: "mining"
---

# Macrel

Upstream: [Macrel](https://github.com/BigDataBiology/macrel)

## Citation

Santos-Júnior, C. D., Pan, S., Zhao, X. & Coelho, L. P. Macrel: antimicrobial peptide screening in genomes and metagenomes. *PeerJ* **8**, e10555 (2020). https://doi.org/10.7717/peerj.10555

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Macrel mines **small AMP-like peptides**. High false-discovery risk without experimental validation — report as computational candidates. Complementary to antiSMASH (BGCs) and RGI (AMR genes).

## How to run

```bash
conda install -c conda-forge -c bioconda macrel

macrel get-smorfs -f contigs.fa -o temp/macrel/${id} --threads 16
macrel peptides -f temp/macrel/${id}.smorfs.faa -o temp/macrel/${id}_amp
```

## Key parameters

| smORFs first | short ORFs | |
| peptides | AMP classifier | |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Related skills

antismash · rgi · prodigal · dram · `microbial-mining` · `tool-selection` · `metagenomics-workflow`
