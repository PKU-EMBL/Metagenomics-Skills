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
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "Nextflow 26.10.3; nf-core/mag 5.5.0"
  metagenomics.command-status: "current run/report/trace/work-dir/resume interface reviewed; pipeline not executed here"
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
set -euo pipefail
samplesheet=${1:?usage: run-mag.sh SAMPLESHEET.csv FRESH_RUN_DIR}
run=${2:?usage: run-mag.sh SAMPLESHEET.csv FRESH_RUN_DIR}
[[ -s "$samplesheet" ]] || exit 2
[[ ! -e "$run" ]] || { echo "refusing to overwrite: $run" >&2; exit 3; }
mkdir -p "$run/logs" "$run/provenance" "$run/work"
export NXF_VER=26.10.3
nextflow -version >"$run/provenance/nextflow.version.txt" 2>&1
sha256sum "$samplesheet" >"$run/provenance/samplesheet.sha256"
printf 'pipeline\trevision\tprofile\n%s\t%s\t%s\n' \
  'nf-core/mag' '5.5.0' 'singularity' >"$run/provenance/run.tsv"
nextflow -log "$run/logs/nextflow.log" run nf-core/mag -r 5.5.0 \
  -profile singularity --input "$samplesheet" --outdir "$run/results" \
  -work-dir "$run/work" -with-report "$run/execution-report.html" \
  -with-trace "$run/trace.tsv" -with-timeline "$run/timeline.html" \
  -with-dag "$run/dag.html" 2>&1 | tee "$run/logs/console.log"
test -s "$run/execution-report.html"; test -s "$run/trace.tsv"
find "$run/results" -type f -size +0c -print -quit | grep -q .
awk -F '\t' 'NR==1 {for(i=1;i<=NF;i++) if($i=="status") c=i;
  if(!c) bad=2; next} c && $c !~ /^(COMPLETED|CACHED)$/ {bad=1}
  END {exit bad}' "$run/trace.tsv"
```

For the complete release-specific contract and output gates, use `$nf-core-mag`
or `$nf-core-taxprofiler`; do not transfer parameters between pipelines. Inspect
the pipeline schema before launch, because Nextflow options use one dash and
pipeline parameters use two.

## Decision tree

```text
Need reproducible pipeline orchestration?
├─ Nextflow / nf-core → nextflow
├─ Python/Snakefile ecosystem → snakemake
└─ Ad-hoc scripts only → setup + stage skills
```

## Validation, recovery, and provenance

Validate the samplesheet schema, unique sample IDs, paired R1/R2 identity and lane
policy before launch. Inspect trace failures/retries, final deliverables, MultiQC,
per-stage sample reconciliation and scientific quality gates; workflow completion
alone is not analytical validation. Include explicit no-hit/filtered samples in
final tables.

After an infrastructure interruption, repeat the identical command against the
same `work` directory with `-resume` and append a new console log. Do not resume
after changing inputs, parameters, code revision, containers or database
releases; start a fresh run. Archive Nextflow and Java versions, pipeline tag and
commit, full config/profile/params, samplesheet checksum, container digests,
database releases, work/output locations, reports/trace/timeline/DAG, commands,
logs, resource use and validation summaries. Avoid mutable branches and tags.

## Related skills

`snakemake` · `setup` · `metagenomics-workflow` · `research-analysis` ·
`tool-selection` · `multiqc`
