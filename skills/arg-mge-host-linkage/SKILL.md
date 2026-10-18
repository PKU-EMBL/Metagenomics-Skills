---
name: arg-mge-host-linkage
description: >-
  Integrate ARG coordinates, mobile-element boundaries, and microbial host evidence using
  same-contig context, assembly-junction support, long reads, Hi-C, CRISPR, and sequence
  homology. Use when asking which ARG is carried by which MGE and host, or when grading
  linkage strength without converting co-occurrence into physical linkage or transfer.
license: MIT
compatibility: Requires globally unique sequence IDs, coordinate-bearing ARG/MGE calls, read or proximity evidence, and quality-controlled host genomes.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "ARG,MGE,host-linkage,Hi-C,long-read,CRISPR,plasmid,phage"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# ARG–MGE–host linkage

The unit of inference is an explicit chain:

```text
ARG interval → containing sequence/element → host candidate → evidence method
```

Do not create this chain by joining sample names or gene labels alone.

## Linkage ladder

| Tier | Evidence | Permitted wording |
|---|---|---|
| L0 | ARG and MGE/host occur in the same sample | co-detected only |
| L1 | co-abundance or same MAG/bin | candidate association; bin contamination possible |
| L2 | ARG interval lies within an MGE-classified contig/region | assembly-based co-localization |
| L3 | L2 plus supported boundaries/circularity or spanning paired/long reads | physically supported sequence context |
| L4 | L3 plus independent host evidence (integrated flank, normalized Hi-C, CRISPR, or high-specificity homology) | strongly supported computational linkage |
| L5 | isolate closure, targeted PCR, capture/single-cell evidence, or transfer assay | experimentally supported under stated conditions |

No computational score upgrades a result to L5. Integrated prophage/ICE flanks can
support a host but do not demonstrate a recent transfer event.

## Route evidence sources

- ARG calls: `$rgi`, `$amrfinderplus`, `$args-oap`, `$deeparg`, `$resfinder`.
- MGE boundaries/classes: `$genomad`, `$plasx`, `$mob-suite`, `$mobileog`,
  `$integronfinder`, `$isescan`.
- phage hosts: `$iphop` and `$spacepharer`; inspect component evidence separately.
- proximity ligation: `$metator`, `$hicbin`, or `$viralcc`, with experimental controls.
- long-read support: map raw reads with `$minimap2`; require junction-spanning alignments.
- host genome quality/taxonomy: `$checkm2`, `$gunc`, `$gtdbtk`.

## Coordinate-first workflow

1. Create an immutable ID crosswalk before any renaming or sequence extraction.
2. Validate every interval against sequence length and a declared coordinate convention.
3. Derive `contains` relations by interval overlap/containment on the same sequence.
4. Audit assembly junctions with paired-read coverage, long reads, and assembly graphs.
5. Link elements to hosts using each method independently; retain all candidates.
6. Calibrate Hi-C against inter-MAG background, abundance, restriction sites, and controls.
7. Require agreement or explain disagreement among independent host methods.
8. Emit a typed edge table and validate it with `$transfer-network-analysis`.

## Required tables

`features.tsv`:

```text
feature_id,feature_type,sequence_id,start,end,strand,caller,database,score,provenance_id
```

`links.tsv`:

```text
link_id,arg_id,mge_id,host_id,linkage_tier,evidence_method,evidence_unit,
raw_score,calibrated_score,threshold,ambiguity,negative_control_rate,sample_id,
timepoint,direction_status,provenance_id
```

Also retain sequence lengths, element boundaries, all alternative hosts, no-link
records, and the code that generated coordinate intersections.

## Method-specific gates

- **Same contig:** inspect contig length, ends, repeats, chimerism, and local coverage.
- **Long reads:** require unique mapping and reads spanning both ARG/MGE or MGE/host
  junctions with flanking sequence; PCR duplicates do not count as independent support.
- **Hi-C:** use name-sorted, filtered pairs; normalize contacts; inspect cross-sample and
  blank controls; high abundance alone creates contacts.
- **CRISPR:** spacer matches indicate historical exposure and host lineage evidence, not
  necessarily current infection.
- **Binning/co-abundance:** mobile elements violate chromosome-like composition and copy
  number assumptions; treat as weak evidence.

## Interpretation and recovery

A linked ARG may be inactive, disrupted, or below phenotypic relevance. A host link
may represent a broad host lineage rather than the exact cell carrying the element.
A complete chain does not identify transfer direction or timing. If IDs, coordinates,
or library metadata change, regenerate joins in a new output directory rather than
patching old rows.

See the detailed
[evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`resistome-analysis` · `mobilome-analysis` · `horizontal-gene-transfer` ·
`transfer-network-analysis` · `genomad` · `plasx` · `metator` · `hicbin` ·
`viralcc` · `iphop` · `spacepharer` · `minimap2` · `checkm2` · `gunc`
