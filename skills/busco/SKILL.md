---
name: busco
description: >
  Benchmarking Universal Single-Copy Orthologs for genome completeness. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, completeness, busco"
  metagenomics.upstream: "https://gitlab.com/ezlab/busco"
  metagenomics.stage: "assessment"
---

# BUSCO

Upstream: [BUSCO](https://gitlab.com/ezlab/busco)

## Citation

Manni, M. *et al.* BUSCO update: novel and streamlined workflows along with broader and deeper phylogenetic coverage for scoring of eukaryotic, prokaryotic, and viral genomes. *Mol. Biol. Evol.* **38**, 4647–4654 (2021). https://doi.org/10.1093/molbev/msab199

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

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

- Stage: **assessment** (gene-set completeness; complementary to CheckM2 for some lineages)
- Prefer lineage-appropriate BUSCO DB; do not treat BUSCO % as MAG contamination
- Pin software + DB versions in Methods

## Related skills

checkm2 · gunc · mag-qc · `tool-selection` · `metagenomics-workflow`
