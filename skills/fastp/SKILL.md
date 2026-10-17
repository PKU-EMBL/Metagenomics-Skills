---
name: fastp
description: >
  Ultra-fast FASTQ QC/adapter trimming for Illumina/MGI short reads. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, fastq, trimming"
  metagenomics.upstream: "https://github.com/OpenGene/fastp"
  metagenomics.stage: "qc"
---

# fastp

Upstream: [OpenGene/fastp](https://github.com/OpenGene/fastp)

## Citation

Chen, S., Zhou, Y., Chen, Y. & Gu, J. fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics* **34**, i884–i890 (2018). https://doi.org/10.1093/bioinformatics/bty560

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Use fastp **before** host depletion or assembly so adapter/low-quality bases do
not create false k-mers or broken PE pairs. Prefer fastp for short reads; for
ONT/PacBio use long-read QC tools (e.g. fastplong), not fastp.

Always archive HTML/JSON reports — they are the audit trail for “reads were clean”.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Illumina/MGI PE or SE FASTQ(.gz) | Phred33 |
| CPU | 4 threads | 8–16 |
| Disk | ~1–2× input for outputs | Separate `temp/qc` |

## How to run

Install in a pinned environment (for example, `micromamba install -n <env> -c
conda-forge -c bioconda fastp=<version>`), then preserve raw reads as immutable
inputs:

```bash
set -Eeuo pipefail
id="${1:?usage: qc-one.sh SAMPLE_ID}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || {
  echo "unsafe sample ID: $id" >&2; exit 2;
}
r1="seq/${id}_1.fq.gz"  # resolve explicit paths from the manifest in production
r2="seq/${id}_2.fq.gz"
out="temp/qc"
threads="${THREADS:-8}"
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || { echo "invalid THREADS: $threads" >&2; exit 2; }

for file in "$r1" "$r2"; do
  test -s "$file" || { echo "missing/empty input: $file" >&2; exit 2; }
done
mkdir -p "$out" logs
for file in \
  "$out/${id}_1.fastq.gz" "$out/${id}_2.fastq.gz" \
  "$out/${id}_fastp.json" "$out/${id}_fastp.html" \
  "logs/${id}.fastp.stdout.log" "logs/${id}.fastp.stderr.log"; do
  test ! -e "$file" || { echo "refusing to overwrite: $file" >&2; exit 2; }
done

fastp \
  -i "$r1" -I "$r2" \
  -o "$out/${id}_1.fastq.gz" -O "$out/${id}_2.fastq.gz" \
  -j "$out/${id}_fastp.json" -h "$out/${id}_fastp.html" \
  --thread "$threads" \
  >"logs/${id}.fastp.stdout.log" 2>"logs/${id}.fastp.stderr.log"
```

## Key parameters

| Parameter | Typical | Notes |
|-----------|---------|-------|
| `-i/-I` | R1/R2 | Required for PE |
| `-o/-O` | paired `.fastq.gz` | Suffix controls compression; never mix sample IDs |
| `-j/-h` | JSON/HTML | Always keep |
| `-w` | 8 | Threads |
| `--detect_adapter_for_pe` | on when unsure | Auto adapter detection |

## Output

```text
temp/qc/${id}_1.fastq.gz
temp/qc/${id}_2.fastq.gz
temp/qc/${id}_fastp.json
temp/qc/${id}_fastp.html
logs/${id}.fastp.stdout.log
logs/${id}.fastp.stderr.log
```

## Decision tree

```text
Short-read shotgun?
├─ Yes → fastp
└─ Long-read only → not fastp (use long-read QC)
```

## Verify

```bash
test -s "temp/qc/${id}_fastp.json"
test -s "temp/qc/${id}_fastp.html"
seqkit stats -T "temp/qc/${id}_1.fastq.gz" "temp/qc/${id}_2.fastq.gz"
jq '{before: .summary.before_filtering,
     after: .summary.after_filtering,
     duplication_rate: .duplication.rate,
     adapter_trimmed_reads: .adapter_cutting.adapter_trimmed_reads}' \
  "temp/qc/${id}_fastp.json"
```

Require equal retained R1/R2 record counts and inspect unexpectedly large read or
base loss. Archive JSON/HTML and logs; do not call the library “clean” from exit
status alone.

## Related skills

`kneaddata` → next for host removal · `setup` for env install

