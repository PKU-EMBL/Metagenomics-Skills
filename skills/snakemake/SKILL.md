---
name: snakemake
description: >
  Snakemake — Python-based workflow management for reproducible bioinformatics
  (rules, conda/container integration, cluster execution). Use when encoding
  shotgun metagenomics DAGs as Snakefiles or adopting community metagenomics
  snakemake pipelines. Upstream: https://github.com/snakemake/snakemake.
  Route via research-analysis / metagenomics-workflow / setup. Alternative:
  nextflow.
license: MIT
category: utilities
tags: [Snakemake, workflow, reproducibility, pipeline, conda, HPC]
upstream: https://github.com/snakemake/snakemake
stage: utilities
---

# Snakemake

Upstream: [snakemake/snakemake](https://github.com/snakemake/snakemake) ·
Docs: https://snakemake.readthedocs.io/

## Citation

Mölder, F. *et al.* Sustainable data analysis with Snakemake.
*F1000Res.* **10**, 33 (2021). https://doi.org/10.12688/f1000research.29032.2

Original: Köster, J. & Rahmann, S. Snakemake—a scalable bioinformatics workflow
engine. *Bioinformatics* **28**, 2520–2522 (2012).
https://doi.org/10.1093/bioinformatics/bts480

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Snakemake maps well to **rule-based** metagenomics DAGs (QC → assembly → … →
`multiqc` / tables for `research-analysis`). Use conda/mamba or containers per
rule; pin Snakemake major version and environment YAML hashes. Prefer dry-run
(`-n`) before cluster submit.

## How to run

```bash
# conda install -c bioconda snakemake
snakemake -j 16 --use-conda
# or: snakemake -j 100 --cluster 'sbatch ...' --latency-wait 60
```

## Decision tree

```text
Workflow manager?
├─ Snakemake / conda-centric → snakemake
├─ Nextflow / nf-core → nextflow
└─ Manual stages → metagenomics-workflow + setup
```

## Related skills

`nextflow` · `setup` · `metagenomics-workflow` · `research-analysis` ·
`tool-selection` · `multiqc`
