---
name: spacepharer
description: >-
  Predict prokaryote–phage host pairs from CRISPR spacers with SpacePHARER using sensitive
  translated search, aggregated spacer hits, a reversed/control target set, and an explicit
  false-discovery rate. Use for independent phage-host evidence, custom spacer/phage
  databases, taxonomy-aware output, and multi-hit validation.
license: MIT
compatibility: Requires SpacePHARER build 5.c2e680a or pinned source, a 64-bit system, host spacer files/arrays, phage nucleotide genomes, and writable temporary storage.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "SpacePHARER,CRISPR,spacer,phage-host,virus-host,FDR"
  metagenomics.upstream: "https://github.com/soedinglab/spacepharer"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "5.c2e680a; source commit d1e94c04025b"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/database/output contract reviewed; not executed here"
---

# SpacePHARER

SpacePHARER aggregates CRISPR spacer evidence to predict phage–host pairs and estimates a
cutoff against a control target set. Spacer matches support historical host exposure;
they do not establish current infection.

## Inputs

- one nucleotide spacer FASTA per host genome and a newline-delimited file manifest;
- one phage nucleotide genome per FASTA and a newline-delimited file manifest,
  preferably quality-gated with `$checkv`;
- exact host and phage file-to-ID/taxonomy crosswalks;
- target and reversed/control databases built from the same phage set;
- predeclared FDR and output format.

Screen host genomes/MAGs for viral contamination before extracting spacers. A viral contig
mis-binned into a host can create circular evidence.

## Build target/control sets and predict

```bash
set -euo pipefail
phage_manifest=${PHAGE_MANIFEST:?set PHAGE_MANIFEST}
spacer_manifest=${SPACER_MANIFEST:?set SPACER_MANIFEST}
out=${OUTDIR:-results/spacepharer}
[[ -s "$phage_manifest" && -s "$spacer_manifest" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
phage_files=(); spacer_files=()
while IFS= read -r path || [[ -n "$path" ]]; do
  [[ -s "$path" ]] || { echo "missing phage FASTA: $path" >&2; exit 2; }
  phage_files+=("$path")
done < "$phage_manifest"
while IFS= read -r path || [[ -n "$path" ]]; do
  [[ -s "$path" ]] || { echo "missing spacer FASTA: $path" >&2; exit 2; }
  spacer_files+=("$path")
done < "$spacer_manifest"
((${#phage_files[@]} > 0 && ${#spacer_files[@]} > 0)) || exit 2
mkdir -p "$out/tmp"
{
  spacepharer createsetdb "${spacer_files[@]}" "$out/spacerDB" "$out/tmp" \
    --extractorf-spacer 1
  spacepharer createsetdb "${phage_files[@]}" "$out/phageDB" "$out/tmp"
  spacepharer createsetdb "${phage_files[@]}" "$out/phageDB_rev" "$out/tmp" \
    --reverse-fragments 1
  spacepharer predictmatch "$out/spacerDB" "$out/phageDB" "$out/phageDB_rev" \
    "$out/predictions.tsv" "$out/tmp" --fdr 0.05 --fmt 1
} >"$out/spacepharer.stdout.log" 2>"$out/spacepharer.stderr.log"
[[ -s "$out/spacerDB" && -s "$out/phageDB" && -e "$out/predictions.tsv" ]] || exit 3
```

Blank manifest lines are invalid; generate sorted manifests without comments and checksum
them. Supported CRT/MinCED/PILER-CR/CRISPRDetect files can instead be parsed with
`parsespacer` or passed through `easy-predict` according to the pinned release. Include
`--tax-mapping-file` during database creation when taxonomy-aware LCA output is required.

## Validation

- reconcile every host/spacer and phage ID to its source genome;
- inspect combined score, number of independent spacer hits, per-hit best-hit probability,
  coordinates, PAM context, and FDR;
- collapse duplicate arrays/spacers without counting them as independent evidence;
- screen exact matches for host/phage contamination and shared repeats;
- retain no-prediction phages and multiple host candidates;
- compare with `$iphop`, nucleotide homology, and Hi-C evidence without double-counting
  SpacePHARER if it contributed to an integrated predictor.

## Recovery and provenance

Databases can be reused only for the identical sequence set, taxonomy map, SpacePHARER
version, and control-generation options. Otherwise rebuild in a new directory. Record
software/source version, commands, sequence and database checksums, host/phage taxonomy,
FDR, format, temporary-file policy, and all post-filters.

## Interpretation

CRISPR evidence can reflect past exposure, prophage-derived spacers, broad taxonomic host
assignment, or strain-specific immunity. It does not by itself show productive infection,
current co-residence, direction, or host range.

## Source

- https://github.com/soedinglab/spacepharer
- https://doi.org/10.1093/bioinformatics/btab222

## Related skills

`arg-mge-host-linkage` · `iphop` · `virome-analysis` · `checkv` · `viralcc` ·
`metator` · `transfer-network-analysis`
