---
name: nf-core-mag
description: >-
  Run the nf-core/mag Nextflow pipeline for reproducible metagenome QC, assembly, mapping, binning, refinement, taxonomy, and annotation from short, long, hybrid, or preassembled inputs. Use when a pinned containerized end-to-end genome-resolved workflow is preferable to hand-wiring tools.
license: MIT
compatibility: Requires Nextflow compatible with nf-core/mag 5.5.0, Java, a container runtime or supported profile, compute/storage, and optional local databases.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "nf-core,mag,nextflow,assembly,binning,genome-resolved"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "5.5.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and schema reviewed against upstream; not executed here"
---

# nf-core/mag

nf-core/mag orchestrates read QC, assembly, binning/refinement, taxonomic classification, and annotation. Pin the pipeline release; modules and defaults change between releases.

## Samplesheet contract

For paired short reads in 5.5.0:

```csv
sample,group,short_reads_1,short_reads_2,long_reads,short_reads_platform,long_reads_platform
S01,cohortA,/data/S01_R1.fastq.gz,/data/S01_R2.fastq.gz,,ILLUMINA,
S02,cohortA,/data/S02_R1.fastq.gz,/data/S02_R2.fastq.gz,,ILLUMINA,
```

Paths must resolve, FASTQs must be gzip-compressed, sample/run identifiers must obey schema, and a samplesheet cannot mix single- and paired-end short-read modes. `group` controls co-abundance/co-binning by default, not necessarily coassembly; use `--coassemble_group` only by deliberate design.

Validate CSV paths before launch and run the pipeline's test profile on the chosen executor/container stack.

## Pinned run

```bash
set -euo pipefail
samples=${1:?usage: nfcore-mag.sh samplesheet.csv results_dir}
out=${2:?usage: nfcore-mag.sh samplesheet.csv results_dir}
[[ -s "$samples" ]] || exit 2
nextflow -version
nextflow pull nf-core/mag -r 5.5.0
nextflow run nf-core/mag -r 5.5.0 -profile docker \
  --input "$samples" --outdir "$out" \
  -with-report "${out}.execution_report.html" \
  -with-timeline "${out}.timeline.html" \
  -with-trace "${out}.trace.tsv" \
  >"${out}.nextflow.stdout.log" 2>"${out}.nextflow.stderr.log"
```

Use Singularity/Apptainer or an institutional profile as appropriate. Put study-specific parameters and database paths in a versioned `params.yaml`, then invoke `-params-file params.yaml`. Do not rely on automatic “latest” database downloads in a final analysis.

## Preassembled mode

Provide both the read samplesheet and `--assembly_input` (`id,group,assembler,fasta`). Reads must be those used for assemblies and already preprocessed because the pipeline skips preprocessing in this mode. Preserve assembler identity and whether each assembly is individual or grouped.

## Validate outputs

Do not equate Nextflow completion with scientific success. Require:

- a complete MultiQC report and pipeline-info execution records;
- expected sample count at QC and assembly stages;
- non-empty assemblies and mapped-read/coverage outputs;
- bin counts plus CheckM2/quality and GUNC/taxonomy checks where enabled;
- explicit accounting for samples/groups with no acceptable bins;
- database releases and module versions from software-version outputs.

Inspect `.nextflow.log`, trace failed/cached tasks, and module logs. Compare key tool thresholds with project requirements.

## Resume and recovery

After fixing infrastructure or resources, rerun the identical command with `-resume`. If inputs, release, database, or result-affecting parameters change, start a new run/output and do not present cached mixed provenance as one analysis. Preserve the work directory until deliverables pass gates.

## Analytical thinking

A standardized pipeline improves reproducibility but does not choose coassembly groups, host references, binners, or biological thresholds for you. Report pipeline release, profile/container digests, parameters, databases, and observed QC—not merely “nf-core/mag was run.”

## Source

- https://nf-co.re/mag/5.5.0
- https://github.com/nf-core/mag
