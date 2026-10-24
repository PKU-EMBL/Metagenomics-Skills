---
name: cutadapt
description: >
  Adapter/primer trimming for short and long reads. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, adapters"
  metagenomics.upstream: "https://github.com/marcelm/cutadapt"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired-end CLI template statically reviewed; not executed here"
---

# Cutadapt

Upstream: [Cutadapt](https://github.com/marcelm/cutadapt)

## Citation

Martin, M. Cutadapt removes adapter sequences from high-throughput sequencing reads. *EMBnet J.* **17**, 10–12 (2011). https://doi.org/10.14806/ej.17.1.200

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Use when adapters/primers are known exactly (amplicon-like primers on shotgun libraries, custom oligos). For general Illumina shotgun QC prefer fastp.

## How to run

Use a pinned environment and resolve paths from the sample manifest rather than
constructing biological groups from filenames.

```bash
set -Eeuo pipefail
id="${1:?usage: trim-one.sh SAMPLE_ID}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
r1="seq/${id}_1.fq.gz"
r2="seq/${id}_2.fq.gz"
out="temp/qc"
threads="${THREADS:-8}"
adapter_r1="${ADAPTER_R1:-AGATCGGAAGAGC}"
adapter_r2="${ADAPTER_R2:-AGATCGGAAGAGC}"
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
[[ "$adapter_r1" =~ ^[ACGTNacgtn]+$ && "$adapter_r2" =~ ^[ACGTNacgtn]+$ ]] || exit 2
for input in "$r1" "$r2"; do test -s "$input" || exit 2; done
mkdir -p "$out" logs
for target in "$out/${id}_1.fq.gz" "$out/${id}_2.fq.gz" \
  "$out/${id}.cutadapt.json"; do
  test ! -e "$target" || { echo "refusing to overwrite: $target" >&2; exit 2; }
done

cutadapt -j "$threads" -a "$adapter_r1" -A "$adapter_r2" \
  --minimum-length 50 --pair-filter any \
  --json "$out/${id}.cutadapt.json" \
  -o "$out/${id}_1.fq.gz" -p "$out/${id}_2.fq.gz" \
  "$r1" "$r2" \
  >"logs/${id}.cutadapt.stdout.log" \
  2>"logs/${id}.cutadapt.stderr.log"
```

Cutadapt checks paired input length and writes retained reads as pairs. State the
adapter sequences, minimum length, and `--pair-filter` policy in Methods.

## Key parameters

| `-a/-A` | adapters | R1/R2 |
| `-j` | threads | |

## Decision notes

- Stage: **QC** — adapter/primer trimming before host depletion / assembly
- Prefer when custom adapters or amplicon primers matter; else `fastp` often enough
- Keep trimmed PE pairing consistent for KneadData / assembly

## Validation, recovery, and provenance

```bash
gzip -t "temp/qc/${id}_1.fq.gz" "temp/qc/${id}_2.fq.gz"
test -s "temp/qc/${id}.cutadapt.json"
r1_count="$(seqkit stats -T "temp/qc/${id}_1.fq.gz" | awk 'NR==2 {print $4}')"
r2_count="$(seqkit stats -T "temp/qc/${id}_2.fq.gz" | awk 'NR==2 {print $4}')"
test "$r1_count" = "$r2_count"
```

Inspect the JSON/log for adapter yield, retained pairs, length loss, and warnings;
a zero exit code does not establish that the specified oligos were appropriate.
Rerun into fresh paths after changing adapters or filters. Record Cutadapt
version, exact oligos, pair-filter policy, input/output checksums, command, and
logs.

## Related skills

`fastp` · `trimmomatic` · `tool-selection` · `metagenomics-workflow`
