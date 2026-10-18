---
name: strainge
description: >-
  Detect, characterize, and compare low-abundance bacterial strains in metagenomes with
  StrainGST and StrainGR. Use for k-mer reference search, concatenated-reference design,
  strain-aware low-coverage variant calling, ACNI/gap comparisons, and longitudinal
  tracking under explicit reference, insert-size, coverage, and mixture gates.
license: MIT
compatibility: Requires StrainGE 1.3.9, a species/genus StrainGST database and reference genomes, BWA-MEM, samtools, MUMmer4, and paired or single reads.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "StrainGE,StrainGST,StrainGR,strain,low-abundance,variant"
  metagenomics.upstream: "https://github.com/broadinstitute/StrainGE"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.3.9"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/output contract reviewed against upstream; not executed here"
---

# StrainGE

StrainGST selects close references by k-mers; StrainGR then calls variants and genome gaps
against a carefully constructed concatenated reference. Reference choice and callable
fraction must accompany every comparison.

## Input contract

- prebuilt StrainGST HDF5 database, matching `k`, reference FASTAs, and similarities table;
- QC-filtered paired reads and measured/estimated insert size;
- related samples grouped before concatenated-reference construction;
- unique reference/scaffold/sample IDs;
- predeclared StrainGST acceptance and StrainGR callable/comparison gates.

## Search references

```bash
set -euo pipefail
sample=${SAMPLE_ID:?set SAMPLE_ID}
r1=${READ1:?set READ1}
r2=${READ2:?set READ2}
db=${STRAINGST_DB:?set STRAINGST_DB}
out=${OUTDIR:-results/strainge/$sample}
[[ -s "$r1" && -s "$r2" && -s "$db" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
{
  straingst kmerize -k 23 -o "$out/sample.hdf5" "$r1" "$r2"
  straingst run -O -o "$out/gst" "$db" "$out/sample.hdf5"
} >"$out/straingst.stdout.log" 2>"$out/straingst.stderr.log"
[[ -s "$out/gst.stats.tsv" && -s "$out/gst.strains.tsv" ]] || exit 3
```

The database and reads must use the same k-mer size. Inspect coverage, evenness, score, and
estimated abundance rather than accepting every returned reference.

## Characterize variants

Build one concatenated reference for a biologically related sample set from accepted
StrainGST results, then map and call:

```bash
set -euo pipefail
results_manifest=${GST_RESULTS_MANIFEST:?set GST_RESULTS_MANIFEST}
pattern=${REFERENCE_PATTERN:?set REFERENCE_PATTERN, including literal {ref}}
similarities=${SIMILARITIES:?set SIMILARITIES}
r1=${READ1:?set READ1}
r2=${READ2:?set READ2}
out=${OUTDIR:?set OUTDIR}
insert=${INSERT_SIZE:-300}
[[ -s "$results_manifest" && -s "$similarities" && -s "$r1" && -s "$r2" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
gst_results=()
while IFS= read -r path || [[ -n "$path" ]]; do
  [[ -s "$path" ]] || { echo "missing StrainGST result: $path" >&2; exit 2; }
  gst_results+=("$path")
done < "$results_manifest"
((${#gst_results[@]} > 0)) || exit 2
mkdir -p "$out"
{
  straingr prepare-ref -s "${gst_results[@]}" -p "$pattern" -S "$similarities" \
    -o "$out/refs_concat.fasta"
  bwa index "$out/refs_concat.fasta"
  bwa mem -I "$insert" -t 8 "$out/refs_concat.fasta" "$r1" "$r2" \
    | samtools sort -@ 4 -O BAM -o "$out/sample.bam" -
  samtools index "$out/sample.bam"
  straingr call "$out/refs_concat.fasta" "$out/sample.bam" \
    --hdf5-out "$out/sample.gr.hdf5" --summary "$out/sample.gr.tsv" --tracks all
} >"$out/straingr.stdout.log" 2>"$out/straingr.stderr.log"
[[ -s "$out/sample.gr.hdf5" && -s "$out/sample.gr.tsv" && -s "$out/sample.bam.bai" ]] || exit 3
```

The manifest avoids ambiguous shell globs and preserves paths as separate `-s` values.
Use only split-format `*.strains.tsv` results from StrainGST 1.3+.

Compare two call files with `straingr compare` and retain summary plus detail tables.
Require adequate `commonPct` before interpreting ACNI or shared alleles.

## Validation

- inspect StrainGST reference coverage/evenness and database representation;
- audit repetitive/shared regions in the concatenated reference;
- validate unique read mapping, insert-size choice, callable fraction, SNP/multi-allelic
  sites, gaps, and low/high-coverage masks;
- compare the same reference scaffolds across samples;
- test unrelated/background samples and stricter callable thresholds.

## Recovery and provenance

K-mer sets are reusable only with identical reads, k, and software. Rebuild references and
BAMs when accepted strains or insert size change. Record StrainGE/BWA/samtools/MUMmer
versions, database/reference checksums, k, thresholds, insert size, commands, and all
sample/reference exclusions.

## Interpretation

A close StrainGST reference is not necessarily the sampled strain. High ACNI over a small
callable region does not prove strain identity; shared strains do not prove direct or
directional transmission.

## Source

- https://github.com/broadinstitute/StrainGE
- https://doi.org/10.1186/s13059-022-02630-0

## Related skills

`strain-transmission` · `strain-resolved-analysis` · `instrain` · `midas2` ·
`strainfacts` · `bwa` · `samtools`
