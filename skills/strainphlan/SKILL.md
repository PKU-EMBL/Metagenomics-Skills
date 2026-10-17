---
name: strainphlan
description: >-
  Reconstruct clade-specific consensus markers and infer strain phylogenies with StrainPhlAn in the MetaPhlAn 4 suite. Use when a target MetaPhlAn species/SGB has adequate marker breadth across samples and marker-level strain relatedness or phylogeny is required.
license: MIT
compatibility: Requires MetaPhlAn/StrainPhlAn 4.2.5, matching marker database, Bowtie2 or minimap2 mappings, and PhyloPhlAn dependencies.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "strainphlan,metaphlan,strain,markers,phylogeny,sgb"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "MetaPhlAn 4.2.5"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream source; not executed here"
---

# StrainPhlAn

StrainPhlAn builds consensus sequences for clade-specific markers and infers a phylogeny. It is not a whole-genome SNV caller and can suppress within-sample mixtures.

## Pin one database

Record the MetaPhlAn index name and database directory. All profiles, mappings, extracted markers, and StrainPhlAn runs must use the same index.

```bash
metaphlan --version
sample2markers.py --version
strainphlan --version
```

Do not use `latest` in a final reproducible command; resolve it to an explicit index ID.

## Generate mappings and consensus markers

```bash
set -euo pipefail
DB=/data/metaphlan
INDEX=mpa_vJan25_CHOCOPhlAnSGB_202503   # replace only with the installed pinned ID
sample=S01
metaphlan "${sample}_R1.fastq.gz,${sample}_R2.fastq.gz" --input_type fastq \
  --db_dir "$DB" -x "$INDEX" --mapout "${sample}.mapout.bz2" \
  -s "${sample}.sam.bz2" --nproc 16 -o "${sample}.profile.tsv" \
  >"${sample}.metaphlan.stdout.log" 2>"${sample}.metaphlan.stderr.log"
sample2markers.py -i "${sample}.sam.bz2" -f bz2 -o consensus_markers \
  -d "$INDEX" --db_dir "$DB" -n 16
find consensus_markers -type f -size +0c | grep -q .
```

Before cohort execution, confirm the exact installed index name rather than copying the example. For current MetaPhlAn source, `sample2markers.py` emits compressed JSON consensus-marker files.

## Choose and run a clade

Use `strainphlan --print_clades_only` or profiles to identify analyzable clades, then extract matching database markers:

```bash
CLADE=t__SGB00000   # use an observed clade ID
extract_markers.py -c "$CLADE" -o db_markers -d "$INDEX" --db_dir "$DB"
strainphlan -s consensus_markers/*.json.bz2 \
  -m "db_markers/${CLADE}.fna" -c "$CLADE" -o "strainphlan_${CLADE}" \
  -n 16 --phylophlan_mode accurate --non_interactive \
  >"strainphlan_${CLADE}.stdout.log" 2>"strainphlan_${CLADE}.stderr.log"
```

Inspect `--help` for release-specific marker filenames and reference-genome support.

## Quality gates

- report samples entering and retained after marker-count/breadth filters;
- inspect marker missingness, polymorphism, alignment length, and tree support;
- verify sample IDs and clade ID in all outputs;
- test sensitivity to breadth and marker-presence thresholds;
- screen temporal/subject duplicates and contamination before interpreting close clusters.

Default filtering includes minimum marker counts/percentages and marker presence across samples; do not weaken these solely to retain a desired group.

## Failure recovery and provenance

A failed clade often reflects insufficient marker coverage rather than software failure. Report it as not analyzable. Use a new output directory after changing database or thresholds. Preserve mappings, consensus JSON, marker FASTA, alignment/tree, versions, index files/checksums, and complete commands.

## Analytical thinking

Tree proximity is marker-level genetic relatedness, not direct transmission. Recombination, mixed strains, incomplete markers, and database representation can affect topology. Phrase results at the resolution supported by callable markers.

## Source

- https://github.com/biobakery/MetaPhlAn
