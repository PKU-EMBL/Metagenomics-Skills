---
name: strain-resolved-analysis
description: >-
  Choose and audit strain-resolved metagenomic analysis using marker phylogenies, reference-based SNVs, within-population diversity, or shared-strain tests. Use when deciding among StrainPhlAn, metaSNV, and inStrain, defining detectability gates, or preventing strain-level claims from species-level profiles.
license: MIT
compatibility: Requires quality-controlled reads plus marker alignments or reference-mapped BAM files.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "strain,microdiversity,snv,strainphlan,metasnv,instrain"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Strain-resolved analysis

Define the biological question before choosing a method. “Strain” has method-dependent resolution.

## Routing

| Question | Skill | Evidence unit |
|---|---|---|
| Phylogeny of a detected MetaPhlAn clade | `$strainphlan` | consensus marker alignment/tree |
| Cohort-wide SNV and population-genetic matrices against references | `$metasnv` | reference positions/SNVs |
| Within-sample nucleotide diversity and pairwise population sharing | `$instrain` | mapped reads on genomes/MAGs |

Species abundance alone cannot establish strain identity. A MAG consensus alone does not measure within-sample microdiversity.

## Input and detectability contract

- sample IDs and longitudinal/subject structure;
- reference/database release and sequence checksums;
- sorted/indexed BAMs where required, generated with a consistent mapper and filters;
- per-reference breadth, depth, mapped reads, and mapping-quality summaries;
- read-group or sample provenance;
- a predeclared minimum evidence rule.

Use breadth and depth jointly. High mean depth over a small conserved region is not strain-resolved coverage. Exclude samples/references failing the gate before comparative tests.

## Workflow

1. Screen taxa and estimate whether enough samples meet coverage requirements.
2. Choose clade markers or references without using outcome labels.
3. Map/process every sample identically; retain unmapped and filtered-read statistics.
4. Run the selected method and preserve callable-site masks.
5. Validate sample/reference coverage and inspect mixed-population indicators.
6. Build trees/distances only over comparable marker sets or callable positions.
7. Test biological hypotheses with subject, batch, geography, and time represented correctly.
8. Repeat key comparisons under stricter mapping and coverage thresholds.

## Required outputs

- `detectability.tsv`: sample, taxon/reference, mapped reads, mean depth, breadth, callable sites, pass/fail reason;
- method-native variants, consensus markers, distances, and trees;
- sample/reference inclusion lists;
- database release, mapper options, filters, software versions, and logs;
- threshold-sensitivity results.

## Quality gates

Check reference ambiguity, multi-mapping, recombination, contamination, mixed-strain signals, temporal plausibility, and tree support. For transmission-like claims, require epidemiological context and an explicit null/background diversity comparison.

## Analytical thinking

Similarity can reflect common ancestry, limited marker resolution, reference bias, or unsampled intermediates. Strain sharing is not direct transmission. Consensus approaches suppress within-host mixtures; SNV approaches inherit reference ascertainment. Report “marker-level clustering,” “low population distance,” or “shared population evidence” unless stronger validation exists.
