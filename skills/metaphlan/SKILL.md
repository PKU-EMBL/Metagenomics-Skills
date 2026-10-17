---
name: metaphlan
description: >
  Marker-gene taxonomic profiling of metagenomes. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, marker, profiling"
  metagenomics.upstream: "https://github.com/biobakery/MetaPhlAn"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "4.2.5 interface"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream source; not executed here"
---

# MetaPhlAn

Upstream: [biobakery/MetaPhlAn](https://github.com/biobakery/MetaPhlAn)

## Citation

Blanco-Míguez, A. *et al.* Extending and improving metagenomic taxonomic profiling with uncharacterized species using MetaPhlAn 4. *Nat. Biotechnol.* **41**, 1633–1644 (2023). https://doi.org/10.1038/s41587-023-01688-w

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MetaPhlAn 4 profiles via **SGB-specific marker genes** (species-level genome
bins), including many unknown SGBs built from MAGs — not only named species.
Detection uses a sufficient fraction of markers (default **20%**); abundance uses
within-sample-normalized average marker coverage.

From the paper / practical implications:

- Expands profiling into uncharacterized diversity vs isolate-only markers.
- Presence calls aim for low false positives; coverage ~≥0.5× was associated with
  reliable detection in isolate-based checks in that work — rare taxa near noise
  need cautious language.
- MetaPhlAn authors note high false-positive rates for some Bracken settings in
  their comparisons — do **not** treat Kraken+Bracken and MetaPhlAn as
  interchangeable species tables.
- Cannot report taxa lacking markers in the installed database.

Often invoked inside HUMAnN; use this skill when MetaPhlAn outputs/parameters
are primary deliverables.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Dehosted PE/SE FASTQ | From `kneaddata` |
| Database | MetaPhlAn DB matching software version | Pinned release (SGB DB) |
| RAM | 16–32 GB | 64 GB |

## How to run

```bash
set -euo pipefail
DB=${METAPHLAN_DB:?set METAPHLAN_DB}
INDEX=${METAPHLAN_INDEX:?set an explicit installed index name}
mkdir -p temp/metaphlan result/metaphlan
[[ -s "temp/hr/${id}_1.fastq" && -s "temp/hr/${id}_2.fastq" ]] || exit 2
metaphlan \
  "temp/hr/${id}_1.fastq,temp/hr/${id}_2.fastq" \
  --input_type fastq --db_dir "$DB" -x "$INDEX" \
  --mapout "temp/metaphlan/${id}.mapout.bz2" \
  -o "result/metaphlan/${id}_profile.txt" --nproc 8 \
  2>"temp/metaphlan/${id}.stderr.log"
```

Merge profiles across samples with MetaPhlAn utility scripts / HUMAnN join tools.

## Interpretation

| Output | Means | Does not mean |
|--------|-------|---------------|
| Relative abundance | Marker-supported composition | Absolute CFU/load |
| SGB / unknown clade | Marker package present | Cultured species name |
| Unclassified | No markers hit | Community is empty |

## Decision tree

```text
Need marker-based species/SGBs?
├─ Yes → metaphlan (alone or via humann)
├─ Pathways too → humann
├─ Joint DNA+AA read class → metabuli
├─ Custom large DNA DB → kraken2 (+ bracken)
└─ Sketch containment → sylph
```

## Validation, recovery, and provenance

Require a non-empty profile with MetaPhlAn metadata headers and clade rows or an explicitly documented no-detection result. Confirm `#mpa_v...`/database identity, sample ID, estimated reads, relative-abundance sum within format tolerance, rank parsing, and absence of duplicate taxa. Review unknown SGBs, low-marker detections, controls, and unexpectedly high unclassified fractions; merge only profiles from one database release.

Preserve the mapout to rerun profiling without remapping when the installed release supports it. Record MetaPhlAn/Bowtie2 versions, explicit index and database manifest/checksum, command, read checksums, mapout/profile checksums, and stderr. Relative abundance and marker detection do not establish absolute load, viability, or taxon absence below detection.

## Related skills

`humann` · `kraken2` · `motus` · `metabuli` · `sylph` · `visualization` · `tool-selection`
