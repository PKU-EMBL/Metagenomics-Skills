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
metaphlan \
  temp/hr/${id}_1.fastq,temp/hr/${id}_2.fastq \
  --input_type fastq \
  --bowtie2out temp/metaphlan/${id}.bowtie2.bz2 \
  -o result/metaphlan/${id}_profile.txt \
  --nproc 8
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

## Related skills

`humann` · `kraken2` · `motus` · `metabuli` · `sylph` · `visualization` · `tool-selection`
