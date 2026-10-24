---
name: snakemake
description: >
  Snakemake — Python-based workflow management for reproducible bioinformatics (rules,
  conda/container integration, cluster execution). Use when encoding shotgun
  metagenomics DAGs as Snakefiles or adopting community metagenomics snakemake
  pipelines. Alternative: nextflow.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "Snakemake, workflow, reproducibility, pipeline, conda, HPC"
  metagenomics.upstream: "https://github.com/snakemake/snakemake"
  metagenomics.stage: "utilities"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "9.27.1"
  metagenomics.command-status: "current v9 dry-run, conda, executor and report interfaces reviewed; workflow not executed here"
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

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Snakemake maps well to **rule-based** metagenomics DAGs (QC → assembly → … →
`multiqc` / tables for `research-analysis`). Use conda/mamba or containers per
rule; pin Snakemake major version and environment YAML hashes. Prefer dry-run
(`-n`) before cluster submit.

## How to run

The template below assumes every final rule derives its paths from
`config["outdir"]`; enforce that convention in the workflow.

```bash
set -euo pipefail
workflow=${1:?usage: run-smk.sh WORKFLOW_DIR FRESH_RUN_DIR}
run=${2:?usage: run-smk.sh WORKFLOW_DIR FRESH_RUN_DIR}
workflow=$(cd "$workflow" && pwd)
snakefile="$workflow/workflow/Snakefile"
[[ -s "$snakefile" ]] || snakefile="$workflow/Snakefile"
[[ -s "$snakefile" ]] || exit 2
[[ ! -e "$run" ]] || { echo "refusing to overwrite: $run" >&2; exit 3; }
mkdir -p "$run/logs" "$run/provenance"
run=$(cd "$run" && pwd)
snakemake --version >"$run/provenance/snakemake.version.txt"
sha256sum "$snakefile" >"$run/provenance/snakefile.sha256"
snakemake --snakefile "$snakefile" --directory "$workflow" \
  --config outdir="$run/results" --dry-run --printshellcmds \
  >"$run/logs/dry-run.log" 2>&1
snakemake --snakefile "$snakefile" --directory "$workflow" \
  --config outdir="$run/results" --cores 16 --use-conda \
  --rerun-incomplete --printshellcmds --show-failed-logs \
  2>&1 | tee "$run/logs/run.log"
snakemake --snakefile "$snakefile" --directory "$workflow" \
  --config outdir="$run/results" --summary >"$run/summary.tsv"
snakemake --snakefile "$snakefile" --directory "$workflow" \
  --config outdir="$run/results" --report "$run/report.html" \
  >"$run/logs/report.log" 2>&1
test -s "$run/summary.tsv"; test -s "$run/report.html"
find "$run/results" -type f -size +0c -print -quit | grep -q .
```

For HPC, pin the matching executor plugin/profile and use, for example,
`--executor slurm --jobs 100`; do not copy scheduler settings across clusters.

## Decision tree

```text
Workflow manager?
├─ Snakemake / conda-centric → snakemake
├─ Nextflow / nf-core → nextflow
└─ Manual stages → metagenomics-workflow + setup
```

## Validation, recovery, and provenance

Lint/test the workflow, dry-run the intended targets, inspect wildcard expansion,
DAG/sample counts, paired-read mapping and all final target files. Review summary,
rule logs, benchmark tables, incomplete markers and domain-specific QC; a zero
exit code does not prove biological validity. Rules must use atomic outputs and
retain explicit no-hit/filtered states.

For an interrupted but otherwise unchanged run, repeat the exact execution with
`--rerun-incomplete` and append a recovery log. Use a fresh output root after any
input, config, rule, wrapper, environment/container or database change. Never use
`--touch` to represent work that was not performed. Archive Snakemake/Python and
executor-plugin versions, workflow commit, config/profile, input manifests and
checksums, conda locks or container digests, database releases, rule commands/logs,
benchmarks, summary/report and validation results.

## Related skills

`nextflow` · `setup` · `metagenomics-workflow` · `research-analysis` ·
`tool-selection` · `multiqc`
