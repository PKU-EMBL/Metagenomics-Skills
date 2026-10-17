---
name: genomad
description: >
  Identify plasmids, viruses, and other mobile genetic elements in assemblies or
  genomes. Use for plasmidome/virome mining, MGE-aware AMR context, and pre-CheckV viral
  candidate lists.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MGE, plasmid, virus, genome-mining"
  metagenomics.upstream: "https://github.com/apcamargo/genomad"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
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
always run **CheckV** before publishing vMAG completeness. For finer MGE detail
use `mobileog` (proteins), `isescan` (IS), `integronfinder` (integrons), and
`mob-suite` (MOB/replicon typing) or `plasmidfinder` / `staramr` (CGE replicons).

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

## Validation, recovery, and provenance

Require completed execution logs and virus/plasmid summary tables plus matching FASTA/gene outputs, even when a class has zero candidates. Reconcile every reported element to an input contig and coordinates, verify unique IDs after any trimming, and inspect score, hallmark genes, taxonomy, length, terminal repeats and provirus status. Pass viral sequences to `$checkv`; inspect conflicting plasmid/virus/chromosome classifications rather than forcing one label.

`--cleanup` removes evidence useful for diagnosis, so retain intermediates until validation. Use a new output after changing input/database/options. Record geNomad/MMseqs2 versions, database release/checksum, full command, input and result checksums, and filter code. Predictions indicate sequence-class evidence, not complete episomes, infective particles, host, or activity.

## Related skills

`virome-analysis` · `checkv` · `virsorter2` · `vcontact` · `plasmaag` · `mobileog` ·
`isescan` · `integronfinder` · `mob-suite` · `cge-finders` · `plasmidfinder` ·
`staramr` · `rgi` · `resfinder` · `antismash` · `microbial-mining` · `megahit`
