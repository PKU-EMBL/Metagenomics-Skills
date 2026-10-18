---
name: metator
description: >-
  Process metagenomic Hi-C data into normalized contig-contact networks and proximity-based
  MAGs with MetaTOR. Use when auditing Hi-C mapping, network normalization, repeated
  community detection, recursive bin validation, or downstream MGE–host hypotheses while
  controlling restriction-site, abundance, spurious-contact, and package-interface limits.
license: MIT
compatibility: Requires MetaTOR 1.3.10, Python 3.9–3.11, Bowtie2 or BWA, samtools, Prodigal, HMMER, Java, CheckM resources, assembly FASTA, and paired metaHi-C reads or mapped pairs.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MetaTOR,metaHi-C,proximity-ligation,binning,contact-network,host-linkage"
  metagenomics.upstream: "https://github.com/koszullab/metaTOR"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.3.10"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "pipeline CLI reviewed; MGE-host subcommand requires release-specific fixture validation"
---

# MetaTOR

MetaTOR constructs a normalized metaHi-C contig network, repeatedly partitions it, and can
validate/decontaminate bins. Proximity ligation is experimental contact evidence; contacts
can arise from abundance, restriction-site density, crosslinking, and laboratory noise.

## Input contract

- shotgun assembly with stable contig IDs, preferably assembled from non-Hi-C reads;
- paired metaHi-C reads with known library protocol and restriction enzyme(s), if used;
- negative/technical controls and library-level mapping/contact summaries;
- read-name-sorted BAM pairs or valid 4DN `.pairs` when starting after alignment;
- sufficient memory for CheckM validation and a fresh output directory.

Preserve mate identity. Do not coordinate-sort BAM inputs documented as name-sorted.

## Full pipeline from reads

```bash
set -euo pipefail
assembly=${ASSEMBLY:?set ASSEMBLY}
r1=${HIC_R1:?set HIC_R1}
r2=${HIC_R2:?set HIC_R2}
out=${OUTDIR:-results/metator}
[[ ${HIC_ENZYMES+x} ]] || {
  echo "set HIC_ENZYMES to a comma-separated list, or explicitly to empty" >&2; exit 2;
}
enzymes=$HIC_ENZYMES
[[ -s "$assembly" && -s "$r1" && -s "$r2" ]] || exit 2
for path in "$out" "${out}.tmp" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
enzyme_args=(); [[ -z "$enzymes" ]] || enzyme_args=(--enzyme "$enzymes")
depth_args=()
if [[ -n ${CONTIG_DEPTH:-} ]]; then
  [[ -s "$CONTIG_DEPTH" ]] || exit 2
  depth_args=(--depth "$CONTIG_DEPTH")
fi
mkdir -p "$(dirname "$out")"
metator pipeline -1 "$r1" -2 "$r2" -a "$assembly" -o "$out" --threads 16 \
  --tmpdir "${out}.tmp" "${enzyme_args[@]}" "${depth_args[@]}" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/network.txt" && -s "$out/contig_data_final.txt" && \
   -s "$out/binning.txt" && -s "$out/bin_summary.txt" && \
   -d "$out/final_bin_unscaffold" ]] || exit 3
```

The pinned 1.3.10 `pipeline` source writes `final_bin_unscaffold/`; the standalone
validation command and parts of the README use `final_bin/`. Gate the source-emitted path
for the command actually run. The pinned pipeline accepts `--start bam` or `pair`; use the
separate `partition`/`validation` commands rather than an obsolete `--start network`
example. In every case enforce the release-specific format and sorting contract. If
restriction-site-aware normalization is selected, record exact enzyme names and verify
site counts.

## MGE/host use

The normalized `network.txt`, final `contig_data_final.txt`,
`final_bin_unscaffold/`, and validated MAG assignments can support
MGE–host hypotheses after MGE contigs are identified independently. Calibrate contacts
against intra-/inter-MAG background and require multiple host contigs or orthogonal
support. Do not select the largest raw contact as a host by default.

MetaTOR 1.3.10 source exposes `host`/`mge` command interfaces, but the reviewed packaged
call path is not part of the main documented tutorial and requires a fixture test before
production use. Do not present those subcommands as validated merely because help text
exists; retain the tested command/help and expected output schema if enabling them.

## Validation

- reconcile total, aligned, inter-contig, rejected, and duplicate contact pairs;
- inspect network normalization, component structure, and control/background contacts;
- validate MAG completeness/contamination independently with current `$checkm2` and `$gunc`;
- compare proximity bins with composition/coverage binners;
- test host links across mapping-quality, minimum-contact, and abundance/site corrections;
- inspect contig IDs across assembly, network, bins, and MGE calls.

## Recovery and provenance

Mapping and pair generation can be reused only with identical reads, assembly, mapper,
and filters. Partitioning can be rerun from an immutable normalized network in a new
folder. Record MetaTOR/dependency versions, protocol/enzyme, commands, assembly/read
checksums, mapping/contact QC, normalization, random/repeated-partition settings, and all
bin/host thresholds.

## Interpretation

A Hi-C contact supports physical proximity in the prepared community, not necessarily
intracellular residence, stable host range, infection, or transfer. Cross-sample or
cross-batch recurrence is not independent molecular validation.

## Source

- https://github.com/koszullab/metaTOR
- https://doi.org/10.3389/fgene.2019.00753

## Related skills

`arg-mge-host-linkage` · `hicbin` · `viralcc` · `genomad` · `checkm2` · `gunc` ·
`transfer-network-analysis` · `bowtie2` · `samtools`
