---
name: midas2
description: >-
  Profile species, single-nucleotide variants, and pangenome gene copy number across
  metagenomic cohorts with MIDAS2. Use when preparing a pinned MIDAS database, running
  per-sample species/SNP/gene modules, merging jointly callable population data, or
  defining strain-sharing gates from coverage-aware allele tables.
license: MIT
compatibility: Requires MIDAS2 1.1.3 on Linux, Bowtie2/samtools and other package dependencies, paired or single metagenomic reads, and a pinned MIDASDB such as UHGG.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MIDAS2,strain,SNV,pangenome,gene-copy-number,cohort"
  metagenomics.upstream: "https://github.com/pollardlab/MIDAS"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.1.3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "stable MIDAS2 CLI/output contract reviewed; not executed here"
---

# MIDAS2

MIDAS2 performs reference-based species, SNV, and pangenome gene-content analysis. Database
choice defines detectable species, representative genomes, and ascertainment. This contract
is for the released `midas2==1.1.3` CLI; the current `pollardlab/MIDAS` main branch also
contains MIDAS v3 work and must not be substituted without a separate interface review.

## Input contract

- QC-filtered reads with exact sample/mate manifest;
- one immutable MIDASDB name/directory and checksum manifest for the cohort;
- unique sample IDs safe for directory names;
- predeclared abundant-species, depth, breadth, base-quality, allele, and prevalence gates;
- subject/time/batch metadata kept outside outcome-driven species selection.

Do not mix UHGG and GTDB/custom database IDs in one merge. A database update requires a
new cohort result.

## Per-sample species and SNVs

```bash
set -euo pipefail
sample=${SAMPLE_ID:?set SAMPLE_ID}
r1=${READ1:?set READ1}
r2=${READ2:?set READ2}
db=${MIDASDB_DIR:?set MIDASDB_DIR}
dbname=${MIDASDB_NAME:-uhgg}
out=${OUTROOT:-results/midas2}
stdout="$out/${sample}.run.stdout.log"
stderr="$out/${sample}.run.stderr.log"
[[ -s "$r1" && -s "$r2" && -d "$db" ]] || exit 2
for path in "$out/$sample" "$stdout" "$stderr"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$out"
{
  midas2 run_species --sample_name "$sample" -1 "$r1" -2 "$r2" \
    --midasdb_name "$dbname" --midasdb_dir "$db" --num_cores 16 "$out"
  midas2 run_snps --sample_name "$sample" -1 "$r1" -2 "$r2" \
    --midasdb_name "$dbname" --midasdb_dir "$db" --num_cores 16 "$out"
} >"$stdout" 2>"$stderr"
[[ -s "$out/$sample/species/species_profile.tsv" && \
   -s "$out/$sample/snps/snps_summary.tsv" ]] || exit 3
```

Initialize/download the database in a controlled setup step with `midas2 database --init`,
then archive the resulting manifest/checksums. Database downloads during production should
be disabled or monitored.

## Cohort merge

Create a two-column TSV headed `sample_name` and `midas_outdir`, verify every per-sample
summary, then run:

```bash
set -euo pipefail
samples=${SAMPLES_LIST:?set SAMPLES_LIST}
db=${MIDASDB_DIR:?set MIDASDB_DIR}
dbname=${MIDASDB_NAME:-uhgg}
out=${MERGE_OUT:-results/midas2/merge}
[[ -s "$samples" && -d "$db" ]] || exit 2
for path in "$out" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")"
midas2 merge_snps --samples_list "$samples" --midasdb_name "$dbname" \
  --midasdb_dir "$db" --genome_coverage 0.70 --num_cores 16 "$out" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/snps_summary.tsv" ]] || exit 3
```

The 0.70 genome-coverage gate is an explicit example, not a universal strain-sharing
threshold. Choose it before group comparisons and report excluded sample/species pairs.
Use `run_genes`/`merge_genes` with a pinned pangenome index for gene copy-number analysis.

## Validation

- reconcile all sample/species pairs across species, SNP, and merged summaries;
- inspect mapped reads, fraction covered, depth, callable sites, and allele balance;
- compare only jointly callable positions and retain missing/no-call states;
- test mapping ambiguity, reference divergence, and mixed-strain signals;
- reproduce key pairwise links under stricter coverage and allele filters;
- place similarity against unrelated/background pairs before transmission claims.

## Recovery and provenance

Per-sample modules are reusable only with identical reads/database/options. A merge may be
rerun from immutable per-sample outputs under a new directory. Record MIDAS2/dependency
versions, MIDASDB release/checksums, commands, reads, sample list, species-selection and
merge filters, and every exclusion.

## Interpretation

SNV and gene-copy profiles are reference-conditioned. Low distance supports shared/related
populations over callable regions; it does not alone prove direct transmission, direction,
or a pure strain.

## Source

- https://github.com/pollardlab/MIDAS
- https://doi.org/10.1093/bioinformatics/btac713

## Related skills

`strain-resolved-analysis` · `strain-transmission` · `instrain` · `metasnv` ·
`strainge` · `strainfacts` · `bowtie2` · `samtools`
