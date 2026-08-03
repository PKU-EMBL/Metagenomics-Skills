---
name: genomad
description: >
  Identify plasmids, viruses, and other mobile genetic elements in assemblies
  or genomes. Use for plasmidome/virome mining, MGE-aware AMR context, and
  pre-CheckV viral candidate lists. Upstream: https://github.com/apcamargo/genomad.
license: MIT
category: analysis-tools
tags: [MGE, plasmid, virus, genome-mining]
upstream: https://github.com/apcamargo/genomad
stage: mining
---

# geNomad

Upstream: [apcamargo/genomad](https://github.com/apcamargo/genomad)

## Citation

Camargo, A. P. *et al.* Identification of mobile genetic elements with geNomad.
*Nat. Biotechnol.* **42**, 1303–1312 (2024).
https://doi.org/10.1038/s41587-023-01953-y

## Analytical thinking

geNomad scores contigs/genomes for **plasmid-like and virus-like** signals using
markers + neural networks. Use it to:

1. Flag MGEs before interpreting chromosomal BGCs/AMR
2. Build viral candidate sets for `checkv`
3. Separate plasmid-borne ARGs (`rgi` hits on plasmid contigs)

Do not equate “plasmid score high” with a complete circular plasmid. For viruses,
always run **CheckV** before publishing vMAG completeness.

Can run on **full assemblies** (pre-binning) or on bins; pre-binning catches
MGEs that never enter bacterial bins.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| DB | `genomad download-database` | Pin path + version |
| Input | Contigs or genomes FASTA | |
| CPU | 8 | 16+ |
| Disk | DB tens of GB class | SSD helpful |

## How to run

```bash
conda install -c bioconda genomad
genomad download-database db/genomad

genomad end-to-end \
  contigs.fa \
  temp/genomad/${id} \
  -d db/genomad \
  --threads 16 \
  --cleanup

# Key tables (names may include sample prefix)
# temp/genomad/${id}/${id}_summary/${id}_virus_summary.tsv
# temp/genomad/${id}/${id}_summary/${id}_plasmid_summary.tsv
```

## Key parameters

| Option | Guidance |
|--------|----------|
| `--splits` | Lower memory on huge assemblies (see docs) |
| `--cleanup` | Remove intermediate heavy files |
| score cutoffs | Filter summary TSVs for reporting |

## Decision tree

```text
MGE / virus goal?
├─ Plasmid + virus screen on assembly → genomad
├─ Virus-focused legacy SOP → virsorter2 (± genomad consensus)
└─ Publish viral genomes → checkv quality mandatory
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| DB path errors | Absolute path to downloaded DB |
| Memory errors | `--splits` / smaller input chunks |
| Empty virus table | Low viral signal or too-short contigs — check min length filters |

## Related skills

`checkv` · `virsorter2` · `rgi` · `antismash` · `microbial-mining` · `megahit`
