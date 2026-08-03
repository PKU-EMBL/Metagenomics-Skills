---
name: preprocessing
description: >
  Read quality control and host depletion for shotgun metagenomes.
  Use this skill when: (1) Running fastp on paired-end libraries,
  (2) Removing host reads with KneadData/Bowtie2,
  (3) Fixing paired-end ID mismatches,
  (4) Preparing dehosted reads for profiling or assembly,
  (5) Summarizing QC metrics before downstream analysis.

  For study design, use study-design.
  For profiling, use read-based.
license: MIT
category: analysis-tools
tags: [qc, fastp, kneaddata, host-depletion]
---

# Preprocessing

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Linux x86_64 | Same |
| Threads | 4 | 16+ |
| Temp disk | 3× raw | 5× raw |
| Metadata | `result/metadata.txt` | Unix newlines |

## How to run

### 1. fastp

```bash
fastp -i seq/${i}_1.fq.gz -I seq/${i}_2.fq.gz \
  -j temp/qc/${i}_fastp.json -h temp/qc/${i}_fastp.html \
  -o temp/qc/${i}_1.fastq -O temp/qc/${i}_2.fastq
```

### 2. KneadData host removal

```bash
kneaddata -i1 temp/qc/${i}_1.fastq -i2 temp/qc/${i}_2.fastq \
  -o temp/hr --bypass-trim --bypass-trf --reorder \
  --bowtie2-options '--very-sensitive --dovetail' \
  -db ${db}/kneaddata/human/hg_39 \
  --remove-intermediate-output -v -t 8
```

**Always use `--reorder`.** Mate mismatches break MetaWRAP, salmon, and BASALT.

## Key parameters

| Parameter | Default guidance | Description |
|-----------|------------------|-------------|
| Host DB | study-specific | Human/mouse/plant Bowtie2 index |
| `--reorder` | on | Keep PE IDs paired |
| Threads | 4–16 | Per-sample KneadData |

## Output format

```text
temp/qc/${id}_fastp.json
temp/hr/${id}_1.fastq
temp/hr/${id}_2.fastq
result/qc/sum.txt
```

## Decision tree

```text
Need host removal?
│
├─ Host-associated (human/animal/plant) → KneadData with matching host index
├─ Environmental with negligible host → QC only; document decision
└─ Human data for public release → deposit dehosted reads
```

## Verify

```bash
paste <(head -n40 temp/hr/${i}_1.fastq | grep ^@) \
      <(head -n40 temp/hr/${i}_2.fastq | grep ^@)
```

## Related skills

- `setup` — databases and envs
- `read-based` — next for composition tables
- `gene-catalogue` — next for assembly path
