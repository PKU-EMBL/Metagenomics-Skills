---
name: trimmomatic
description: >
  Flexible Illumina adapter/quality trimmer. Use for installation, parameter choice,
  execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, trimming"
  metagenomics.upstream: "https://github.com/usadellab/Trimmomatic"
  metagenomics.stage: "qc"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired-end legacy CLI template statically reviewed; not executed here"
---

# Trimmomatic

Upstream: [Trimmomatic](https://github.com/usadellab/Trimmomatic)

## Citation

Bolger, A. M., Lohse, M. & Usadel, B. Trimmomatic: a flexible trimmer for Illumina sequence data. *Bioinformatics* **30**, 2114–2120 (2014). https://doi.org/10.1093/bioinformatics/btu170

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Prefer **fastp** for most shotgun runs (speed + JSON). Use Trimmomatic when a lab SOP already pins ILLUMINACLIP settings.

## How to run

Use a pinned environment and the exact adapter FASTA required by the study SOP.

```bash
set -Eeuo pipefail
id="${1:?usage: trim-one.sh SAMPLE_ID ADAPTERS_FA}"
adapters="${2:?usage: trim-one.sh SAMPLE_ID ADAPTERS_FA}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
r1="seq/${id}_1.fq.gz"
r2="seq/${id}_2.fq.gz"
out="temp/qc"
threads="${THREADS:-8}"
for input in "$r1" "$r2" "$adapters"; do test -s "$input" || exit 2; done
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
mkdir -p "$out" logs
for suffix in 1P 1U 2P 2U; do
  test ! -e "$out/${id}_${suffix}.fq.gz" || exit 2
done

trimmomatic PE -phred33 -threads "$threads" \
  "$r1" "$r2" \
  "$out/${id}_1P.fq.gz" "$out/${id}_1U.fq.gz" \
  "$out/${id}_2P.fq.gz" "$out/${id}_2U.fq.gz" \
  "ILLUMINACLIP:${adapters}:2:30:10" SLIDINGWINDOW:4:20 MINLEN:50 \
  >"logs/${id}.trimmomatic.stdout.log" \
  2>"logs/${id}.trimmomatic.stderr.log"
```

## Key parameters

| `ILLUMINACLIP` | adapter fasta | Required |
| `SLIDINGWINDOW` | 4:20 typical | |
| `MINLEN` | ≥50 | |

## Decision notes

- Stage: **QC** (legacy Illumina trimmer)
- Prefer `fastp` for new pipelines unless reproducing Trimmomatic Methods
- Keep PE pairing; archive trim logs

## Validation, recovery, and provenance

```bash
for suffix in 1P 1U 2P 2U; do gzip -t "temp/qc/${id}_${suffix}.fq.gz"; done
r1_count="$(seqkit stats -T "temp/qc/${id}_1P.fq.gz" | awk 'NR==2 {print $4}')"
r2_count="$(seqkit stats -T "temp/qc/${id}_2P.fq.gz" | awk 'NR==2 {print $4}')"
test "$r1_count" = "$r2_count"
```

Use only `1P` and `2P` as the synchronized paired library unless a downstream
single-end branch explicitly consumes `1U`/`2U`. Inspect the summary for input,
both-surviving, forward-only, reverse-only, and dropped counts. Rerun into fresh
outputs after changing clipping or quality rules. Archive Trimmomatic/Java
versions, adapter FASTA checksum, full command, logs, and input/output checksums.

## Related skills

`fastp` · `fastqc` · `kneaddata` · `tool-selection` · `metagenomics-workflow`
