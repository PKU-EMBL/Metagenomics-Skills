---
name: anvio
description: >
  Anvi'o — interactive multi-omics platform for metagenomic assemblies, MAG
  refinement, visualization, and SNP/profile exploration. Use when: (1) Manual
  or human-guided bin refinement, (2) Interactive contig profiles across samples,
  (3) Linking MAGs with coverage/SNVs/metatranscriptomes, (4) Producing Anvi'o
  interactive HTML reports. Upstream: https://github.com/merenlab/anvio.
  Complements automated ensemble binning (basalt/metawrap/dastool); not a
  replacement for CheckM2/GUNC QC.
license: MIT
category: analysis-tools
tags: [anvio, visualization, MAG, refinement, interactive]
upstream: https://github.com/merenlab/anvio
stage: binning
---

# Anvi'o

Upstream: [merenlab/anvio](https://github.com/merenlab/anvio) ·
https://anvio.org/

## Citation

Eren, A. M. *et al.* Anvi'o: an advanced analysis and visualization platform for
'omics data. *PeerJ* **3**, e1319 (2015). https://doi.org/10.7717/peerj.1319

See also [docs/references.md](../../docs/references.md).

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

## How to run (pattern)

Exact subcommands evolve — verify with `anvi-script-reformat-fasta --help` /
current docs:

```bash
# illustrative workflow skeleton
anvi-script-reformat-fasta contigs.fa -o contigs_fixed.fa --simplify-names
anvi-gen-contigs-database -f contigs_fixed.fa -o CONTIGS.db -n PROJECT
anvi-run-hmms -c CONTIGS.db -T 16
anvi-profile -i sample.bam -c CONTIGS.db -o PROFILE_sample -T 16
# anvi-merge ... then anvi-interactive -p PROFILE.db -c CONTIGS.db
```

## Decision tree

```text
Need interactive MAG refinement / multi-omics viz?
├─ Yes → anvio
├─ Fully automated catalogue → basalt ★ / metawrap / dastool
└─ Only QC metrics → checkm2 / gunc / mag-qc
```

## Related skills

`basalt` · `metawrap` · `coverm` · `checkm2` · `gunc` · `deepurify` ·
`visualization` · `tool-selection`
`mag-qc`
