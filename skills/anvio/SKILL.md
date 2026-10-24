---
name: anvio
description: >
  Anvi'o — interactive multi-omics platform for metagenomic assemblies, MAG refinement,
  visualization, and SNP/profile exploration. Use when: (1) Manual or human-guided bin
  refinement, (2) Interactive contig profiles across samples, (3) Linking MAGs with
  coverage/SNVs/metatranscriptomes, (4) Producing Anvi'o interactive HTML reports.
  Complements automated ensemble binning (basalt/metawrap/dastool); not a replacement
  for CheckM2/GUNC QC.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "anvio, visualization, MAG, refinement, interactive"
  metagenomics.upstream: "https://github.com/merenlab/anvio"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "contigs-database/profile workflow statically reviewed; interactive refinement not executed here"
---

# Anvi'o

Upstream: [merenlab/anvio](https://github.com/merenlab/anvio) ·
https://anvio.org/

## Citation

Eren, A. M. *et al.* Anvi'o: an advanced analysis and visualization platform for
'omics data. *PeerJ* **3**, e1319 (2015). https://doi.org/10.7717/peerj.1319

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Anvi'o is a **platform**, not a single binner: contig databases, profiling BAM
coverage across samples, interactive interfaces for organizing contigs into
bins, SNV profiling, and multi-omics linking. Use it when automated bins need
**human-guided refinement** or when you must communicate contig-level evidence.

Typical place in this package:

```text
assembly + multi-sample BAMs
  → anvi'o contig DB + profile DB
  → import automatic bins (MetaBAT2 / BASALT / …) optional
  → interactive refinement
  → export bins → checkm2 / gunc / drep / gtdbtk
```

Do not treat interactive aesthetics as QC — still run `checkm2` / `gunc` /
`deepurify` as appropriate.

## Prerequisites

| Need | Notes |
|------|-------|
| Contigs | Assembly FASTA |
| BAM(s) | Sorted/indexed; multi-sample profiles are Anvi'o's strength |
| RAM / GUI | Large profiles need memory; interactive needs browser access |

## How to run

The BAM must have been mapped to the exact FASTA used for the contigs database.
If contig names need simplification, reformat **before mapping** and retain the
name map; do not simplify the FASTA and then profile an old BAM.

```bash
set -Eeuo pipefail
id="${1:?usage: build-anvio-profile.sh SAMPLE_ID CONTIGS BAM OUTPUT_DIR}"
contigs="${2:?usage: build-anvio-profile.sh SAMPLE_ID CONTIGS BAM OUTPUT_DIR}"
bam="${3:?usage: build-anvio-profile.sh SAMPLE_ID CONTIGS BAM OUTPUT_DIR}"
out="${4:?usage: build-anvio-profile.sh SAMPLE_ID CONTIGS BAM OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
test -s "$contigs" && test -s "$bam" || exit 2
samtools quickcheck -v "$bam"
{ test -s "$bam.bai" || test -s "${bam%.bam}.bai"; } || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

anvi-gen-contigs-database -f "$contigs" -o "$out/CONTIGS.db" -n "$id" \
  >"$out/gen-contigs.stdout.log" 2>"$out/gen-contigs.stderr.log"
anvi-run-hmms -c "$out/CONTIGS.db" -T "$threads" \
  >"$out/hmms.stdout.log" 2>"$out/hmms.stderr.log"
anvi-profile -i "$bam" -c "$out/CONTIGS.db" \
  -o "$out/PROFILE_${id}" -T "$threads" \
  >"$out/profile.stdout.log" 2>"$out/profile.stderr.log"
```

Profile each sample separately against the same contigs database, then merge the
resulting profile databases with a release-compatible `anvi-merge` command.

## Decision tree

```text
Need interactive MAG refinement / multi-omics viz?
├─ Yes → anvio
├─ Fully automated catalogue → basalt ★ / metawrap / dastool
└─ Only QC metrics → checkm2 / gunc / mag-qc
```

## Validation, recovery, and provenance

Require readable contigs/profile databases, completed logs, BAM/reference name
agreement, and expected contig/read counts. Before and after manual refinement,
export collections with stable bin IDs and rerun `checkm2`, `gunc`, taxonomy,
and read-support checks. Preserve the original automatic bins and an explicit
contig move/add/remove audit; screenshots alone are not reproducible evidence.

Do not overwrite databases after failed migrations or release changes. Record
Anvi'o release, database schemas, dependency versions, FASTA/BAM checksums,
commands, logs, profile/merge sample order, collection exports, refinement notes,
and final-bin checksums. Interactive judgment is curator evidence, not
experimental validation.

## Related skills

`basalt` · `metawrap` · `coverm` · `checkm2` · `gunc` · `deepurify` ·
`visualization` · `tool-selection` · `mag-qc`
