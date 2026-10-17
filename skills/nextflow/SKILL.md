---
name: nextflow
description: >
  Nextflow — workflow manager for scalable, reproducible bioinformatics pipelines (DSL2,
  containers, cloud/HPC executors). Use when packaging shotgun metagenomics stages into
  portable runs or adopting nf-core modules/pipelines. Alternative: snakemake.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "Nextflow, nf-core, workflow, reproducibility, pipeline, HPC"
  metagenomics.upstream: "https://github.com/nextflow-io/nextflow"
  metagenomics.stage: "utilities"
---

# Nextflow

Upstream: [nextflow-io/nextflow](https://github.com/nextflow-io/nextflow) ·
nf-core: https://nf-co.re · Docs: https://www.nextflow.io/docs/latest/

## Citation

Di Tommaso, P. *et al.* Nextflow enables reproducible computational workflows.
*Nat. Biotechnol.* **35**, 316–319 (2017).
https://doi.org/10.1038/nbt.3820

nf-core: Ewels, P. A. *et al.* The nf-core framework for community-curated
bioinformatics pipelines. *Nat. Biotechnol.* **38**, 276–278 (2020).
https://doi.org/10.1038/s41587-020-0439-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Nextflow orchestrates **containerized** processes with resumable execution —
ideal once tool choices from `tool-selection` are fixed. Prefer nf-core
pipelines/modules when they match your claim; otherwise write a thin DSL2
wrapper around this package’s skills. Pin Nextflow version, container engine
(Docker/Singularity/Apptainer), and `nextflow.config` profiles for HPC.

Workflow ≠ statistical Methods — still pin each bioinformatics tool/DB inside
processes.

## How to run

```bash
# install Nextflow; then e.g.
nextflow run nf-core/<pipeline> -profile singularity --input samplesheet.csv ...
# or: nextflow run main.nf -resume
```

## Decision tree

```text
Need reproducible pipeline orchestration?
├─ Nextflow / nf-core → nextflow
├─ Python/Snakefile ecosystem → snakemake
└─ Ad-hoc scripts only → setup + stage skills
```

## Related skills

`snakemake` · `setup` · `metagenomics-workflow` · `research-analysis` ·
`tool-selection` · `multiqc`
