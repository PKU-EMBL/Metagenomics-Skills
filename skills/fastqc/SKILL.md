---
name: fastqc
description: >
  QC reports for Illumina FASTQ before/after trimming. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, fastq"
  metagenomics.upstream: "https://github.com/s-andrews/FastQC"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# FastQC

Upstream: [FastQC](https://github.com/s-andrews/FastQC)

## Citation

Andrews, S. FastQC: a quality control tool for high throughput sequence data (2010). https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FastQC is a **report**, not a cleaner. Use it to audit raw and cleaned reads; do trimming with fastp/cutadapt.

## How to run

```bash
set -euo pipefail
command -v fastqc >/dev/null
fastqc --version
mkdir -p temp/qc
[[ -s "seq/${id}_1.fq.gz" && -s "seq/${id}_2.fq.gz" ]] || exit 2
fastqc seq/${id}_1.fq.gz seq/${id}_2.fq.gz -o temp/qc -t 8 \
  >temp/qc/${id}.fastqc.stdout.log 2>temp/qc/${id}.fastqc.stderr.log
```

## Key parameters

| `-o` | output dir | HTML+zip reports |
| `-t` | threads | |

## Decision notes

- Stage: **QC** (report-only)
- Prefer before/after trimming for QC reports; does not modify reads
- Pair with `fastp` JSON/HTML for actionable filters

## Validation, recovery, and provenance

Require one non-empty HTML and ZIP report per input, then inspect `summary.txt`/`fastqc_data.txt` inside each ZIP and compare sample/read labels to the manifest. Review sequence quality, adapters, duplication, overrepresented sequences, GC, and length together; individual WARN/FAIL flags are technology- and library-dependent and are not automatic rejection rules.

Run before and after cleaning, retain both reports, and aggregate with `$multiqc`. On truncated ZIP/HTML or a sample-count mismatch, discard that report directory and rerun. Record FastQC version, command, input checksum, and what corrective action—if any—was actually taken.

## Related skills

fastp · kneaddata · `tool-selection` · `metagenomics-workflow`
