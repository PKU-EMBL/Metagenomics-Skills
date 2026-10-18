---
name: strain-transmission
description: >-
  Design and audit strain sharing, persistence, acquisition, and transmission analyses
  from shotgun metagenomes or isolate genomes. Use to combine StrainPhlAn, inStrain,
  MIDAS2, StrainGE, StrainFacts, PopPUNK, Gubbins, epidemiological metadata, and
  TransPhylo without equating species co-presence or genomic similarity with direct transmission.
license: MIT
compatibility: Requires longitudinal/contact metadata, consistent references, coverage and callable-site gates, and preferably external background samples.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "strain,transmission,sharing,SNV,genomic-epidemiology,longitudinal"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Strain transmission

Strain similarity is necessary but usually insufficient for direct transmission.
Define whether the target is persistence within a host, sharing between hosts,
acquisition from a source, an outbreak cluster, or a directed transmission tree.

## Routing by data and question

| Need | Prefer |
|---|---|
| Marker-based clade phylogeny across metagenomes | `$strainphlan` |
| Population ANI, microdiversity, shared populations | `$instrain` |
| Cohort SNVs and gene copy number | `$midas2` / `$metasnv` |
| Low-abundance targeted strain search and comparison | `$strainge` |
| Multi-strain deconvolution across samples | `$strainfacts` |
| Isolate/genome population clusters | `$poppunk` |
| Remove recombination from a low-diversity lineage alignment | `$gubbins` |
| Dated-phylogeny transmission posterior | `$transphylo` |
| Community source proportions | `$source-tracking` |

Source tracking addresses mixture compatibility, not strain transmission. Use it as a
separate evidence layer.

## Transmission evidence ladder

| Tier | Evidence | Interpretation |
|---|---|---|
| T0 | same species/taxon | co-presence only |
| T1 | same marker clade or reference cluster | related lineage |
| T2 | low distance over adequate callable genome plus mixture-aware concordance | shared/near-identical strain evidence |
| T3 | T2 plus temporal, spatial/contact, background, and alternative-route support | plausible transmission link |
| T4 | T3 plus a calibrated transmission model or direct epidemiological confirmation | supported transmission hypothesis |

Even T4 may include an unsampled intermediary. Direction requires temporal and model
support; genomic distance alone is symmetric.

## Input and design contract

- immutable sample/person/site/time/contact manifest and sampling intervals;
- raw-read and reference checksums; one mapping/filter policy across comparisons;
- per-sample/reference depth, breadth, callable positions, allele balance, and mixtures;
- negative controls and unrelated/background samples from the same population;
- predeclared distance/callable-site rule calibrated within the organism and timescale;
- recombination handling and molecular-clock/temporal-signal assessment;
- policy for repeated samples, multiple colonies, and unsampled hosts.

Avoid outcome-informed reference selection. High mean depth on conserved loci does not
make genomes comparable.

## Workflow

1. Screen detectability without using case/contact labels.
2. Profile strain mixtures and exclude or model non-callable comparisons.
3. Compute pairwise distance only on jointly callable positions or comparable markers.
4. Quantify uncertainty and test stricter mapping, breadth, depth, and allele thresholds.
5. Place candidate links against unrelated/background diversity.
6. For isolates/consensus genomes, cluster with PopPUNK and remove recombination with
   Gubbins before fine-scale phylogeny where assumptions hold.
7. Overlay time/contact/location only after genomic analysis is frozen.
8. Use TransPhylo only with a dated, recombination-aware tree and defensible generation
   and sampling-time distributions.
9. Export typed edges through `$transfer-network-analysis`.

## Required deliverables

- `detectability.tsv`: sample/reference, depth, breadth, callable sites, mixture flags,
  pass/fail and reason;
- `pairwise_strain_evidence.tsv`: joint callable length, distance definition/value,
  uncertainty, threshold, method, and sensitivity status;
- `candidate_links.tsv`: source/target, direction status, dates, contact/location,
  genomic tier, epidemiological tier, alternative routes, and provenance;
- recombination-aware tree/alignment where applicable;
- background-distance distribution, inclusion flow, and all excluded comparisons;
- software/database/reference versions, commands, seeds, and checksums.

## Failure modes

Reference bias, homologous recombination, within-host diversity, mixed strains, sequencing
error, contamination, low coverage, and unsampled intermediates can all create or obscure
links. A hard universal SNP cutoff is not transferable across species, genome fractions,
or sampling intervals. Household/site enrichment can reflect a shared reservoir rather
than person-to-person transmission.

## Language for reporting

Prefer “shared-strain evidence,” “genomically compatible with recent common ancestry,”
or “posterior transmission link under the stated model.” Reserve “transmitted from A to
B” for evidence that resolves direction and credible alternatives.

See the
[evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`strain-resolved-analysis` · `strainphlan` · `instrain` · `midas2` · `metasnv` ·
`strainge` · `strainfacts` · `poppunk` · `gubbins` · `transphylo` ·
`source-tracking` · `sourcetracker2` · `feast` · `transfer-network-analysis`
