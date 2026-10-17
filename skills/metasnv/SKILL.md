---
name: metasnv
description: >-
  Call cohort-wide metagenomic SNVs, filter allele frequencies, calculate sample distances/diversity, and infer subpopulations with metaSNV v2. Use for reference-based prokaryotic population analysis when consistently mapped BAMs and sufficient breadth/depth are available.
license: MIT
compatibility: Requires metaSNV 2.0.1+, sorted/indexed non-empty BAMs, a multi-genome reference, htslib, Python, and R for subpopulation analysis.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "metasnv,snv,strain,population-genomics,microdiversity,bam"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0.1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# metaSNV

metaSNV v2 performs multi-sample SNV calling and downstream population analysis against a fixed reference database.

## Input contract

`all_samples` is a text file containing one absolute BAM path per line, with no duplicates or empty mappings. BAMs must derive from the same reference FASTA used by metaSNV, be coordinate-sorted/indexed, and use consistent mapping/filtering. The reference directory must be writable for generated indexes.

```bash
set -euo pipefail
list=all_samples
ref=references.fna
[[ -s "$list" && -s "$ref" ]] || exit 2
[[ $(sort "$list" | uniq -d | wc -l) -eq 0 ]] || { echo duplicate BAMs >&2; exit 2; }
while IFS= read -r bam; do
  [[ -s "$bam" && -s "${bam}.bai" ]] || { echo "missing BAM/index: $bam" >&2; exit 2; }
  samtools quickcheck -v "$bam"
done < "$list"
metaSNV.py --help >/dev/null
```

Archive reference and annotation checksums. The upstream ProGenomes2 representative database is an option, not a mandatory biological choice.

## Run SNVs and post-processing

```bash
out=metasnv_out
metaSNV.py --threads 16 "$out" "$list" "$ref" \
  >metasnv.call.stdout.log 2>metasnv.call.stderr.log
find "$out/snpCaller" -type f -size +0c | grep -q . || exit 3

metaSNV_Filtering.py --n_threads 16 "$out" \
  >metasnv.filter.stdout.log 2>metasnv.filter.stderr.log
find "$out/filtered/pop" -type f -name '*.filtered.freq' -size +0c | grep -q . || exit 3

metaSNV_DistDiv.py --n_threads 16 --filt "$out/filtered/pop" --dist \
  >metasnv.distance.stdout.log 2>metasnv.distance.stderr.log
find "$out/distances" -type f -size +0c | grep -q . || exit 3
```

Provide `--db_ann` during calling only when annotation coordinates exactly match the reference and codon-effect output is required.

Optional subpopulation analysis additionally needs study-compatible gene/species abundance tables:

```bash
metaSNV_subpopr.R --procs 16 -i metasnv_out \
  -g geneAbundances.tsv -a speciesAbundances.tsv \
  >metasnv.subpop.stdout.log 2>metasnv.subpop.stderr.log
```

## Validate

- quantify mapped reads, breadth, depth, and callable positions by sample/reference before comparison;
- inspect SNV counts and filtered allele-frequency files for outliers/empty taxa;
- verify every distance matrix is symmetric with zero diagonal and labeled samples;
- report the number of samples/callable sites contributing to each species;
- repeat key analyses under stricter coverage and mapping filters.

Do not compare samples whose apparent distance is driven by non-overlapping callable regions.

## Recovery and provenance

Use a fresh output directory when the reference or result-affecting parameters change. Keep stage logs and detect partial split files after interrupted parallel calling. Capture metaSNV scripts/environment, mapper/version/options, reference/database release, BAM checksums, and filtering parameters.

## Analytical thinking

Results are conditional on reference selection and mapping specificity. SNV similarity can indicate related populations but not direct transmission; subpopulation clusters are model-derived and require ecological/epidemiological context.

## Source

- https://github.com/metasnv-tool/metaSNV
