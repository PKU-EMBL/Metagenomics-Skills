---
name: deepurify
description: >
  Deepurify — multi-modal deep language model for MAG decontamination by matching
  contigs to taxonomic lineages and splitting chimeric bins into higher-quality
  sub-MAGs. Use when: (1) Cleaning contaminated MAGs after binning, (2) Rescuing
  near-threshold contaminated bins, (3) Complementing CheckM2/GUNC (detection vs contig
  removal).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "decontamination, MAG, Deepurify, QC"
  metagenomics.upstream: "https://github.com/ericcombiolab/Deepurify"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "2.4.3 interface"
  metagenomics.command-status: "deepurify clean CLI checked against upstream v2.4.3 documentation; not executed here"
---

# Deepurify

Upstream: [ericcombiolab/Deepurify](https://github.com/ericcombiolab/Deepurify)

## Citation

Zou, B. *et al.* A multi-modal deep language model for contaminant removal from
metagenome-assembled genomes. *Nat. Mach. Intell.* **6**, 1245–1255 (2024).
https://doi.org/10.1038/s42256-024-00908-5

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CheckM2/GUNC **score** contamination; Deepurify aims to **remove contaminant
contigs** and split chimeras into sub-MAGs using sequence↔taxonomy multimodal
embeddings. Paper reports substantial gains in high-quality MAG counts across
soil, ocean, plant, freshwater, and human faecal sets — treat as
benchmark-conditioned.

Recommended order:

```text
bins → checkm2 (± gunc)
    → deepurify on contaminated / borderline bins
    → re-QC with checkm2 / gunc
    → drep / gtdbtk
```

Do not skip re-QC after decontamination. Model errors can drop true contigs —
inspect high-value novel lineages manually (`anvio`).

## How to run

Use `clean` for an existing bin set. `iter-clean` is a separate contigs+BAM
re-binning workflow and must not be substituted silently.

```bash
set -Eeuo pipefail
bins="${1:?usage: deepurify-clean.sh BINS_DIR DB_DIR OUTPUT_DIR}"
db="${2:?usage: deepurify-clean.sh BINS_DIR DB_DIR OUTPUT_DIR}"
out="${3:?usage: deepurify-clean.sh BINS_DIR DB_DIR OUTPUT_DIR}"
suffix="${BIN_SUFFIX:-fa}"
threads="${THREADS:-16}"
gpu_num="${GPU_NUM:-0}"
test -d "$bins" && test -d "$db" || exit 2
find "$bins" -maxdepth 1 -type f -name "*.${suffix}" -print -quit | grep -q . || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$(dirname "$out")/logs"
name="$(basename "$out")"

deepurify clean -i "$bins" -o "$out" -db "$db" \
  --bin_suffix "$suffix" --gpu_num "$gpu_num" --num_process "$threads" \
  >"$(dirname "$out")/logs/${name}.deepurify.stdout.log" \
  2>"$(dirname "$out")/logs/${name}.deepurify.stderr.log"
```

For GPU execution, explicitly record device IDs, CUDA/PyTorch versions, and
batch/thread settings. Pin the Deepurify-DB snapshot and checksum.

## Decision tree

```text
MAG contamination problem?
├─ Detect / filter only → checkm2 / gunc / mag-qc
├─ Remove contigs / split chimeras → deepurify
├─ Interactive contig surgery → anvio
└─ Prevent upstream → multi-coverage binning + ensemble (basalt ★)
```

## Validation, recovery, and provenance

Reconcile every input MAG to unchanged, cleaned, split, rejected, or failed
outputs. Compare pre/post contig membership, total length, completeness,
contamination, GUNC, taxonomy, coverage coherence, and key genes; gains in one
quality score do not justify loss of biologically supported contigs. Rerun
`checkm2` and `gunc` independently on all retained sub-MAGs.

Never merge partial outputs from changed models/databases. Preserve original
bins and run changed settings under a new path. Record Deepurify/model/database
versions and checksums, dependency and hardware details, commands, logs,
input-output lineage, removed-contig tables, QC comparisons, and final checksums.

## Related skills

`checkm2` · `gunc` · `mag-qc` · `anvio` · `basalt` · `drep` · `tool-selection`
