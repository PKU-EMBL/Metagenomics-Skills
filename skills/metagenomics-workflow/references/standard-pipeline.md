# Execution gates for an end-to-end run

Read this reference when the user asks the agent to **prepare or execute** more
than one pipeline stage. For high-level tool choice, the parent `SKILL.md` is
enough.

## 1. Declare the run contract

Before generating commands, record:

```yaml
mode: plan | prepare | execute | review
question: "..."
statistical_unit: "..."
read_type: illumina-pe | illumina-se | ont | hifi | hybrid
sample_sheet: /absolute/path/samples.tsv
project_root: /absolute/path/project
resources: {cpus: 0, memory_gb: 0, scratch_gb: 0, scheduler: local}
network_allowed: false
route: read-profile | genome-resolved | mining | combined
```

Unknown values remain `null`; do not replace them with invented defaults.

## 2. Build a stage table

For every selected stage specify all six columns:

| Stage | Inputs | Outputs | Tool/config | Resources | Pass gate |
|-------|--------|---------|-------------|-----------|-----------|
| QC | immutable raw FASTQ | paired clean FASTQ + JSON/HTML | pinned parameters | CPU/RAM/scratch | synchronized pairs; loss explained |
| Assembly | clean reads | contigs + report | per-sample/coassembly decision | memory estimate | non-empty FASTA; IDs unique; QUAST reviewed |
| Mapping | reads + exact assembly | sorted BAM + BAI | index checksum | CPU/temp disk | flagstat/depth sane; BAM indexed |
| Binning | contigs + matching coverage | bins + membership map | single/ensemble route | high-memory node | bins non-empty; provenance retained |
| MAG QC | bins | QC table + accepted/rejected IDs | declared thresholds | DB path | CheckM2-style QC + chimerism; failures retained |
| Taxonomy/function | stable accepted IDs | typed/annotated tables | exact DB releases | DB + CPU | all input IDs accounted for |
| Mining | contigs/MAGs + context | evidence table | thresholds + DB | varies | predictions retain coordinates/scores/context |
| Statistics | sample-level table + metadata | models/figures | contrast/covariates/FDR | R/Python env | IDs join; diagnostics; effect sizes + uncertainty |

A stage cannot consume data until the preceding pass gate has evidence.

## 3. Preflight checklist

- [ ] Sample IDs are unique and join metadata one-to-one
- [ ] Paired files exist, are readable, and have compatible record counts
- [ ] Controls and host/background references are identified
- [ ] Binaries/containers report versions
- [ ] Database paths exist and releases are recorded
- [ ] Input and index checksums are captured
- [ ] Output, log, temp, and provenance directories are writable
- [ ] Free scratch exceeds the stage estimate
- [ ] Resume behavior and overwrite policy are explicit
- [ ] A pilot sample or dry run is selected

If any mandatory item fails, return a preflight report and stop before expensive
execution.

## 4. Safe command shape

Generated shell entrypoints should start with strict error handling and write to
new stage directories:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

project_root="${1:?usage: run-stage.sh PROJECT_ROOT}"
mkdir -p "$project_root"/{logs,temp,result,provenance}
```

Quote every path; validate required variables before use; avoid `rm -rf` and
unscoped globs. Capture the exact command, standard output/error, exit status,
and tool version. A successful exit status is necessary but not a biological
quality check.

## 5. Pilot and scale-out

1. Run one representative sample or small partition.
2. Inspect all boundary checks, not only file existence.
3. Estimate full-run CPU-hours, peak RAM, scratch, and final storage.
4. Confirm the estimate and any large download with the user.
5. Scale through Nextflow/Snakemake or scheduler arrays with bounded retries.
6. Resume only when inputs, parameters, tools, and database releases match.

## 6. Delivery bundle

```text
provenance/
├── samples.tsv
├── analysis-plan.yaml
├── software-versions.tsv
├── database-manifest.tsv
├── input-checksums.sha256
├── validation-summary.tsv
├── commands/
└── logs/
```

The final summary must distinguish:

- **executed and verified**
- **executed but failed a gate**
- **prepared but not executed**
- **not attempted / blocked**

Never turn a computational BGC, AMR, virus, pathway, or interaction prediction
into an experimentally validated claim.
