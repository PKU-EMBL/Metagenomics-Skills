---
name: multiqc
description: >
  MultiQC — aggregate bioinformatics QC logs into a single interactive HTML report
  (FastQC, fastp, Bowtie2/BWA, Samtools, QUAST, …). Use after QC/mapping steps to audit
  libraries before biological statistics.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "MultiQC, QC, report, FastQC, research-analysis"
  metagenomics.upstream: "https://github.com/MultiQC/MultiQC"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# MultiQC

Upstream: [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) ·
https://multiqc.info/

## Citation

Ewels, P., Magnusson, M., Lundin, S. & Käller, M. MultiQC: summarize analysis
results for multiple tools and samples in a single report. *Bioinformatics*
**32**, 3047–3048 (2016). https://doi.org/10.1093/bioinformatics/btw354

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MultiQC is for **technical QC dashboards**, not alpha diversity or DA tests.
Point it at directories of tool logs after `fastqc` / `fastp` / mapping / QUAST.
Pin MultiQC version; module support varies by log format.

## How to run

```bash
set -euo pipefail
command -v multiqc >/dev/null
multiqc --version
[[ -d qc_logs ]] || exit 2
mkdir -p multiqc_report
multiqc qc_logs/ -o multiqc_report --force \
  >multiqc_report/multiqc.stdout.log 2>multiqc_report/multiqc.stderr.log
# Add `-c multiqc_config.yaml` when a versioned project config is present.
```

## Decision tree

```text
Need aggregated QC HTML?
├─ Yes → multiqc
├─ Biological diversity / DA → research-analysis → microeco / maaslin2
└─ Per-tool QC only → fastqc / fastp / quast skills
```

## Validation, recovery, and provenance

Require non-empty `multiqc_report.html` and `multiqc_data/`. Compare discovered sample/module counts with the manifest, inspect `multiqc_sources.txt` for source files, and review ignored/duplicate sample-name warnings. Missing modules usually mean absent, moved, or unsupported logs—not that QC passed. Define project-specific thresholds in a versioned config and retain outliers rather than hiding them.

Generate into a clean/versioned directory; `--force` deliberately replaces files and should not mix runs. Record MultiQC version/plugins, config, invocation path(s), source-log checksums or manifest, stdout/stderr, and report/data checksums. MultiQC summarizes observed logs; it does not validate upstream execution or biological quality automatically.

## Related skills

`research-analysis` · `fastqc` · `fastp` · `quast` · `samtools` · `setup` ·
`visualization` · `tool-selection`
