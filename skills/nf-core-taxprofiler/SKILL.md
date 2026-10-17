---
name: nf-core-taxprofiler
description: >-
  Run nf-core/taxprofiler for containerized multi-tool taxonomic classification/profiling of short reads, long reads, or FASTA against explicit database sheets. Use when comparing or standardizing Kraken2/Bracken, MetaPhlAn, mOTUs, Kaiju, Sylph, and related profiles with pinned Nextflow provenance.
license: MIT
compatibility: Requires Nextflow compatible with nf-core/taxprofiler 2.0.1, Java, a supported container/executor profile, and prebuilt classifier databases.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "nf-core,taxprofiler,nextflow,taxonomy,profiling,classification"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and schema reviewed against upstream; not executed here"
---

# nf-core/taxprofiler

Every taxprofiler tool is opt-in: a matching database-sheet row and `--run_<tool>` flag are both required.

## Input contracts

Read samplesheet first columns:

```csv
sample,run_accession,instrument_platform,fastq_1,fastq_2,fasta
S01,run1,ILLUMINA,/data/S01_R1.fastq.gz,/data/S01_R2.fastq.gz,
S02,run1,ILLUMINA,/data/S02_R1.fastq.gz,/data/S02_R2.fastq.gz,
```

Database sheet with explicit data type and parameters:

```csv
tool,db_name,db_params,db_type,db_path
kraken2,standard_202610,,short,/db/kraken2-standard-202610.tar.gz
bracken,standard_202610_bracken,;-r 150 -l S,short,/db/bracken-standard-202610.tar.gz
metaphlan,mpa_2025,,short,/db/metaphlan/
```

Use real pinned database names/paths; examples are structural, not download recommendations. For Bracken, parameters after `;` apply to Bracken and read length must match processed reads. Database names must be unique under upstream rules.

## Pinned run

```bash
set -euo pipefail
samples=${1:?usage: taxprofiler.sh samples.csv databases.csv results_dir}
dbs=${2:?usage: taxprofiler.sh samples.csv databases.csv results_dir}
out=${3:?usage: taxprofiler.sh samples.csv databases.csv results_dir}
[[ -s "$samples" && -s "$dbs" ]] || exit 2
nextflow pull nf-core/taxprofiler -r 2.0.1
nextflow run nf-core/taxprofiler -r 2.0.1 -profile docker \
  --input "$samples" --databases "$dbs" --outdir "$out" \
  --run_kraken2 --run_bracken --run_metaphlan \
  --run_profile_standardisation \
  -with-report "${out}.execution_report.html" \
  -with-trace "${out}.trace.tsv" \
  >"${out}.nextflow.stdout.log" 2>"${out}.nextflow.stderr.log"
```

The option names above are pinned to release 2.0.1 and must remain coupled to that release's generated parameter schema. Add preprocessing only deliberately; FASTA input bypasses preprocessing. Separate short- and long-read runs when tool suitability/parameters differ.

## Output verification

Require:

- MultiQC and pipeline-info reports;
- native per-tool outputs for every expected sample/database pair;
- Taxpasta standardized tables when requested;
- sample IDs and taxon identifiers preserved without accidental aggregation;
- classified/unclassified fractions and tool failure/no-hit states;
- software versions, database checksums/releases, and exact database-sheet parameters.

Standardized tables are structurally comparable, not necessarily quantitatively equivalent: Taxpasta may use direct counts, estimated counts, or transformed relative abundance depending on profiler. Never interpret cross-tool differences without checking those semantics.

## Resume and failure recovery

Use `-resume` only after correcting a failed run with unchanged input/release/result parameters. Missing output often means either the run flag or database row was omitted. Inspect `.nextflow.log`, trace, work-task logs, and database extraction before rerunning.

## Analytical thinking

Classifiers and profilers answer different questions and use different reference spaces. Agreement increases confidence but is not truth; disagreement should be traced to database, rank, abundance semantics, and read technology. Preserve unclassified fractions and negative-control results.

## Source

- https://nf-co.re/taxprofiler/2.0.1
- https://github.com/nf-core/taxprofiler
