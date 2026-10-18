---
name: hicbin
description: >-
  Recover metagenome-assembled genomes from metagenomic Hi-C contact maps with HiCBin,
  HiCzin normalization, spurious-contact filtering, and Leiden clustering. Use when
  preparing name-sorted Hi-C BAMs, taxonomy/coverage inputs, selecting restriction enzymes,
  or benchmarking proximity bins and host-link evidence against MetaTOR or conventional binners.
license: MIT
compatibility: Requires HiCBin 1.1.0 source, Python/R environment with glmmTMB, BWA, samtools, shotgun contig depth, species-level contig taxonomy CSV, and name-sorted Hi-C BAM.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "HiCBin,metaHi-C,HiCzin,binning,Leiden,proximity-ligation"
  metagenomics.upstream: "https://github.com/dyxstat/HiCBin"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.1.0 commit b356c9f50da4"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "source CLI/input/output contract reviewed; not executed here"
---

# HiCBin

HiCBin normalizes metagenomic Hi-C contacts, filters putative spurious contacts, and uses
Leiden clustering to recover MAGs. It is an alternative proximity-binning method, not an
independent experiment when run on the same Hi-C library as MetaTOR.

## Input contract

- assembly FASTA, with the same contig IDs used everywhere;
- Hi-C BAM filtered for unmapped/secondary/supplementary records and sorted by read name;
- species-level contig taxonomy CSV in the documented seven-column layout;
- MetaBAT2-style shotgun depth table from non-Hi-C reads;
- exact restriction enzyme names, or an explicit enzyme-free HiCzin_LC decision;
- pinned R/glmmTMB environment and a fresh output directory.

Taxonomy is used to detect spurious contacts and can introduce reference bias. Audit
unknown/misclassified contigs and repeat the analysis without or with alternative taxonomy
where scientifically justified.

## Run the pipeline

```bash
set -euo pipefail
root=${HICBIN_HOME:?set HICBIN_HOME to pinned source checkout}
assembly=${ASSEMBLY:?set ASSEMBLY}
bam=${HIC_BAM:?set HIC_BAM to read-name-sorted BAM}
tax=${CONTIG_TAXONOMY:?set CONTIG_TAXONOMY}
depth=${CONTIG_DEPTH:?set CONTIG_DEPTH}
out=${OUTDIR:-results/hicbin}
[[ ${HIC_ENZYMES+x} ]] || {
  echo "set HIC_ENZYMES to a comma-separated list, or explicitly to empty" >&2; exit 2;
}
[[ -s "$root/hicbin.py" && -s "$assembly" && -s "$bam" && \
   -s "$tax" && -s "$depth" ]] || exit 2
for path in "$out" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
enzyme_args=()
if [[ -n "$HIC_ENZYMES" ]]; then
  IFS=',' read -r -a enzymes <<<"$HIC_ENZYMES"
  for enzyme in "${enzymes[@]}"; do
    [[ -n "$enzyme" ]] || exit 2
    enzyme_args+=(-e "$enzyme")
  done
fi
mkdir -p "$(dirname "$out")"
python "$root/hicbin.py" pipeline "${enzyme_args[@]}" -v \
  "$assembly" "$bam" "$tax" "$depth" "$out" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/hicbin.log" && -d "$out/BIN" ]] || exit 3
```

Set `HIC_ENZYMES` to the actual enzyme names separated by commas. Set it explicitly to
an empty string only when intentionally using the documented enzyme-free mode.

## Post-processing

Assess initial bins independently. For bins meeting a predeclared completeness/
contamination rule, provide the headerless contaminated-bin list to `hicbin.py recluster`,
then run `merge_bins.py`. Preserve both initial and post-processed assignments; do not
select the version with more desired genomes without a fixed quality rule.

## Validation

- verify BAM query-name sorting, pair counts, mapping-quality/match filters, and duplicates;
- inspect restriction-site model, HiCzin fit, spurious-contact threshold, and graph density;
- reconcile every binned and unbinned contig with the assembly; an empty `BIN` directory
  is a reportable no-bin result, not permission to relax thresholds until bins appear;
- evaluate bins with `$checkm2`, `$gunc`, taxonomy coherence, and conventional binners;
- perturb Leiden resolution and contact thresholds;
- treat MGE-to-bin contacts as host hypotheses requiring `$arg-mge-host-linkage` gates.

## Recovery and provenance

Intermediate contact matrices may be reused only with unchanged assembly, BAM, taxonomy,
depth, enzyme, and filters. Otherwise start clean. Record HiCBin commit, Python/R/glmmTMB
versions, mapper/samtools/depth versions, library protocol/enzyme, input checksums,
commands, random-seed support/status, effective resolution, and all QC thresholds.

## Interpretation

A Hi-C bin is a proximity-derived genome hypothesis. A contact does not alone establish
intracellular host assignment, infection, or recent transfer; high abundance and
crosslinking artifacts can dominate.

## Source

- https://github.com/dyxstat/HiCBin
- https://doi.org/10.1186/s13059-022-02626-w

## Related skills

`metator` · `viralcc` · `arg-mge-host-linkage` · `checkm2` · `gunc` ·
`metabat2` · `samtools`
