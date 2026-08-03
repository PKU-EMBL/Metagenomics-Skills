---
name: busco
description: >
  Benchmarking Universal Single-Copy Orthologs for genome completeness. Use this skill when working with busco: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://gitlab.com/ezlab/busco. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'completeness', 'busco']
upstream: https://gitlab.com/ezlab/busco
stage: assessment
---

# BUSCO

Upstream: [BUSCO](https://gitlab.com/ezlab/busco)

## Citation

Manni, M. *et al.* BUSCO update: novel and streamlined workflows along with broader and deeper phylogenetic coverage for scoring of eukaryotic, prokaryotic, and viral genomes. *Mol. Biol. Evol.* **38**, 4647–4654 (2021). https://doi.org/10.1093/molbev/msab199

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Useful for isolates/eukaryotes; for prokaryotic MAGs prefer **CheckM2** (+ GUNC). Do not mix BUSCO% with CheckM2% unlabeled.

## How to run

```bash
conda install -c bioconda busco  # if packaged; else follow upstream

busco -i genome.fa -l bacteria_odb10 -o temp/busco -m genome -c 16
```

## Key parameters

| `-l` | lineage DB | Match domain |
| `-m` | genome/proteins | |

## Decision notes

- Stage: **assessment** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

checkm2 · gunc · mag-qc · `tool-selection` · `metagenomics-workflow`
