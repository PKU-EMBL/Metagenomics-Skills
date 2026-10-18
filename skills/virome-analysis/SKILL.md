---
name: virome-analysis
description: >-
  Design and execute metagenomic virome analysis from viral-particle-enriched or bulk metagenomes through viral sequence calling, CheckV quality assessment, vOTU dereplication, annotation, abundance, taxonomy, and host prediction. Use when integrating geNomad, VirSorter2, VIBRANT, CheckV, vConTACT, iPHoP, SpacePHARER, or ViralCC with defensible viral quality and host-evidence gates.
license: MIT
compatibility: Requires assembled contigs and container/Conda-capable compute for selected viral tools.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "virome,viruses,phages,votu,checkv,genomad,iphop,spacepharer,viralcc"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Virome analysis

Keep sample preparation, sequence identification, genome quality, species clustering, abundance, taxonomy, and host prediction as separate evidence layers.

## Inputs and design

Record whether data came from bulk metagenomes, virus-like-particle enrichment, size filtration, nuclease treatment, multiple-displacement amplification, or RNA-virus protocols. These choices alter the recoverable community and prohibit naive comparisons across protocols.

Require:

- sample manifest and controls;
- quality-controlled reads and per-sample/coassembly policy;
- contigs with unique, whitespace-safe IDs;
- read mappings for abundance;
- pinned viral caller, CheckV, taxonomy, and host databases.

## Recommended graph

1. **QC and host depletion** — preserve read/base retention and reference identity.
2. **Assembly** — retain assembly graph/logs and inspect minimum viral-candidate length.
3. **Candidate calling** — run `$genomad` and/or `$virsorter2`; use `$vibrant` when its annotation/AMG outputs are specifically needed.
4. **Boundary and quality** — run `$checkv`; separate proviral regions and record completeness/contamination.
5. **Species-level catalogue** — run `$votu-workflow` with an explicit MIUViG-compatible ANI/coverage rule.
6. **Abundance** — map each sample to the non-redundant catalogue; specify identity, aligned fraction, and multi-mapping policy.
7. **Taxonomy/network** — use reference similarity or `$vcontact`; preserve unclassified vOTUs.
8. **Host evidence** — use `$iphop`, `$spacepharer`, provirus boundaries, or calibrated Hi-C (`$viralcc`/`$metator`) and grade each method with `$arg-mge-host-linkage`.
9. **Function/AMGs** — require viral context and manual neighborhood review; metabolic-gene hits alone do not establish AMGs.

## Candidate reconciliation

Create a table with one row per sequence and columns for caller, score/category, coordinates, length, topology, CheckV quality, contamination, vOTU, abundance, taxonomy, host method, host score, and database release. Do not collapse discordant calls into a binary truth value.

A useful acceptance hierarchy is study-specific, but should distinguish:

- high-confidence complete/high-quality genomes;
- medium-quality genomes usable for many ecological analyses;
- low-quality fragments retained only for explicitly supported analyses;
- rejected cellular or low-information sequences.

## Verification gates

- every accepted viral ID exists exactly once in the sequence catalogue;
- CheckV processed the same sequences passed to clustering;
- representative selection is deterministic and documented;
- per-sample mapped viral abundance excludes ambiguous mappings according to a stated policy;
- controls are present in abundance diagnostics;
- host predictions expose method-level evidence and scores;
- circularity, completeness, taxonomy, and host labels are not inferred from filename conventions.

## Deliverables

- `viral_candidates.tsv`, `viral_quality.tsv`, `votu_membership.tsv`;
- representative vOTU FASTA and sequence checksums;
- sample-by-vOTU count/coverage table;
- taxonomy and host-evidence tables with database releases;
- commands, versions, logs, exclusion reasons, and sensitivity results.

## Analytical thinking

A viral caller predicts sequence identity; CheckV estimates genome quality; ANI clustering defines operational populations; host tools infer method-specific links. CRISPR can reflect historical exposure and Hi-C can reflect nonspecific proximity. None experimentally validates infection, activity, or metabolic function. Viral enrichment and amplification can strongly distort relative abundance. Phrase findings as sequence-, catalogue-, or prediction-level evidence.

## Related skills

`genomad` · `virsorter2` · `vibrant` · `checkv` · `votu-workflow` · `vcontact` ·
`iphop` · `spacepharer` · `viralcc` · `metator` · `arg-mge-host-linkage`

## References

- MIUViG: https://doi.org/10.1038/nbt.4306
- geNomad: https://doi.org/10.1038/s41587-023-01953-y
- CheckV: https://doi.org/10.1038/s41587-020-00774-7
