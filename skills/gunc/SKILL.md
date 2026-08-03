---
name: gunc
description: >
  Detect chimerism/contamination in prokaryotic genomes/MAGs. Use this skill when working with gunc: installing, choosing
  parameters, running commands, interpreting outputs, or troubleshooting.
  Upstream: https://github.com/grp-bork/gunc. For stage routing use tool-selection /
  metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['qc', 'contamination', 'chimerism']
upstream: https://github.com/grp-bork/gunc
stage: assessment
---

# GUNC

Upstream: [GUNC](https://github.com/grp-bork/gunc)

## Citation

Orakov, A. *et al.* GUNC: detection of chimerism and contamination in prokaryotic genomes. *Genome Biol.* **22**, 178 (2021). https://doi.org/10.1186/s13059-021-02393-0

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Complement CheckM2: GUNC targets **clade separation / chimerism**. Use both before publication claims on novel lineages.

## How to run

```bash
conda install -c bioconda gunc  # if packaged; else follow upstream

gunc run -i bins/ --db_file $GUNC_DB -r temp/gunc -t 16
```

## Key parameters

| DB | gunc download | Pin |
| with CheckM2 | combine filters | |

## Decision notes

- Stage: **assessment** in QC → assembly → mapping → binning → taxonomy → function
- Prefer ensemble binning (`basalt` recommended; `metawrap`; `dastool`) after single binners
- Pin software + DB versions in Methods

## Related skills

checkm2 · mag-qc · drep · basalt · `tool-selection` · `metagenomics-workflow`
