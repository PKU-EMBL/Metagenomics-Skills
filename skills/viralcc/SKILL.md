---
name: viralcc
description: >-
  Bin fragmented viral contigs and inspect exploratory virus–host proximity evidence from
  metagenomic Hi-C data with ViralCC. Use when preparing read-name-sorted Hi-C BAMs,
  integrating viral interaction and host-proximity graphs, fixing random seeds, or auditing
  raw contact links without treating them as calibrated infection or transfer calls.
license: MIT
compatibility: Requires ViralCC 1.1.0 source, Python scientific dependencies, assembly FASTA, one-column viral-contig list, and a filtered read-name-sorted meta-Hi-C BAM.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ViralCC,metaHi-C,virus-binning,virus-host,proximity-ligation"
  metagenomics.upstream: "https://github.com/dyxstat/ViralCC"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.1.0 commit 917fb56977d0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "source bin CLI reviewed; exploratory link module requires independent calibration"
---

# ViralCC

ViralCC clusters fragmented viral contigs using a Hi-C interaction graph plus a
host-proximity graph. Viral candidates must be identified upstream, and resulting bins
still require viral quality assessment.

## Input contract

- assembly FASTA and a headerless one-column list of viral contig IDs;
- viral candidates from `$genomad`/`$virsorter2` under a frozen rule;
- Hi-C BAM filtered for unmapped, secondary, and supplementary alignments and sorted by
  read name;
- library protocol, restriction enzyme, controls, duplicate policy, and mapping filters;
- pinned source commit because the README and current 1.1.0 subcommand names differ.

The reviewed source command is `bin`; older README examples use `pipeline`. Confirm
`python viralcc.py --help` for the pinned commit before execution.

## Bin viral contigs

```bash
set -euo pipefail
root=${VIRALCC_HOME:?set VIRALCC_HOME to pinned source checkout}
assembly=${ASSEMBLY:?set ASSEMBLY}
bam=${HIC_BAM:?set HIC_BAM to read-name-sorted BAM}
viral=${VIRAL_CONTIGS:?set VIRAL_CONTIGS}
out=${OUTDIR:-results/viralcc}
[[ -s "$root/viralcc.py" && -s "$assembly" && -s "$bam" && -s "$viral" ]] || exit 2
for path in "$out" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")"
python "$root/viralcc.py" bin --random-seed 42 -v \
  "$assembly" "$bam" "$viral" "$out" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/cluster_viral_contig.txt" && -s "$out/viral_contig_info.csv" && \
   -s "$out/prokaryotic_contig_info.csv" && -s "$out/viralcc.log" && \
   -d "$out/VIRAL_BIN" ]] || exit 3
```

A valid run can yield few or no multi-contig bins. Do not require a positive biological
call merely to pass execution.

## Host-link module boundary

The pinned source also exposes `raw` and `link`. The reviewed `link` implementation emits
positive raw contact entries between viral and host-bin contigs; it does not itself provide
a calibrated null, abundance/restriction-site normalization, host-bin aggregation, or
false-discovery threshold. Treat it as an exploratory edge extractor unless a complete,
version-specific calibration and fixture test is added. Prefer `$iphop`/`$spacepharer` as
orthogonal evidence and apply `$arg-mge-host-linkage` gates.

## Validation

- reconcile viral-list IDs and all cluster memberships to the assembly;
- inspect accepted/rejected pairs, mapping quality, duplicate handling, graph density,
  `min-k`, and seed stability;
- run `$checkv` on reconstructed viral bins and inspect chimerism/host contamination;
- compare with vOTU clustering and independent viral callers;
- calibrate any host contacts against inter-MAG/background contacts and controls;
- retain unresolved and multi-host candidates.

## Recovery and provenance

Reusing a contact representation is valid only for identical assembly, BAM, viral list,
and filters. Otherwise use a new output. Record source commit, environment, library
protocol/enzyme, mapper/samtools commands, input checksums, viral-caller rule, random seed,
all thresholds, and CheckV results.

## Interpretation

A ViralCC bin is a graph-based viral genome hypothesis. Shared host-proximity patterns do
not prove that every fragment belongs to one virion. Raw Hi-C links do not prove active
infection, host range, ARG carriage, or transfer.

## Source

- https://github.com/dyxstat/ViralCC
- https://doi.org/10.1038/s41467-023-35945-y

## Related skills

`virome-analysis` · `genomad` · `virsorter2` · `checkv` · `iphop` ·
`spacepharer` · `metator` · `hicbin` · `arg-mge-host-linkage`
