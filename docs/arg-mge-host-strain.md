# ARG–MGE–host–strain evidence and transfer networks

This guide separates four questions that are often collapsed into one claim:

1. **What resistance determinant was detected and how much was present?**
2. **Is that determinant physically carried by a defined mobile element?**
3. **Which organism or strain carries that element?**
4. **Does the study support horizontal transfer, source contribution, strain sharing, or
   direct transmission?**

A strong result can answer one question and remain unresolved for the next. Agreement among
algorithms that reuse the same reference sequences or reads is not independent evidence.

## Start from a frozen design

Before running tools, freeze:

- sample, subject, site, time, extraction batch, library, control, and read-pair manifests;
- assembly unit, long-read/Hi-C linkage unit, and the biological unit that may be connected;
- software versions, database/model releases, immutable checksums, and native namespaces;
- primary thresholds, negative controls, background/reference populations, and sensitivity
  analyses;
- whether each conclusion concerns detection, abundance, physical linkage, host assignment,
  evolutionary history, source mixture, strain sharing, or direct transmission.

Preserve nucleotide/protein/contig/MAG/element/sample/subject IDs with explicit crosswalks.
Never infer coordinate-level linkage after clustering has destroyed the original mapping.

## Resistome evidence layers

| Layer | Typical evidence | Valid statement | Not established |
|---|---|---|---|
| R0 | classifier/alignment hit | sequence is ARG-like under one model/database | phenotype or expression |
| R1 | curated family plus identity/coverage/domain gates | curated genotype detected | resistance in its current host |
| R2 | read mapping or feature counts with a denominator | computational abundance estimate | absolute copies without calibration |
| R3 | coordinate-preserving assembly/long-read support | ARG occupies a defined sequence context | complete mobile element or host |
| R4 | isolate genome plus species-specific mutation rules | genotype predicts a phenotype under a validated scope | measured MIC/susceptibility |
| R5 | culture, MIC or functional assay | experimental phenotype/function under tested conditions | environmental activity in every sample |

Use `resistome-analysis` to choose among RGI/CARD, AMRFinderPlus, ResFinder,
ARGs-OAP/SARG, DeepARG, PathoFact and related methods. Retain each caller's native
accession, class, hierarchy, version, thresholds and uncertainty; crosswalks are explicit
many-to-many tables, never silent renaming.

## ARG–MGE–host linkage ladder

| Level | Evidence | Reporting language |
|---|---|---|
| L0 | same sample | co-detected only; no physical linkage |
| L1 | co-abundance or same MAG/bin | candidate association; bin contamination remains possible |
| L2 | same assembled contig/region with valid ARG and MGE coordinates | assembly-based co-localization |
| L3 | supported boundaries/circularity or paired/long reads spanning relevant junctions | physically supported sequence context |
| L4 | L3 plus normalized Hi-C, CRISPR, integration-site or concordant independent host evidence | strongly supported computational host linkage |
| L5 | isolate closure, targeted capture/PCR/single-cell evidence, or transfer assay | experimentally supported carriage/transfer under tested conditions |

Apply the ladder in `arg-mge-host-linkage`. Short contigs and repeat-mediated paths can
produce false co-location. An assembler circular label is not sufficient: inspect terminal
alignment, read-spanning support, coverage and repeats. Hi-C contacts require abundance,
restriction-site and negative-control calibration. CRISPR spacers support host lineage or
historical exposure, not current productive infection.

## Horizontal gene transfer: choose the timescale

| Question | Suitable route | Main limitation |
|---|---|---|
| taxonomically discordant genes among genomes/MAGs | MetaCHIP2, HGTector2, gene trees | historical candidate; donor sampling and contamination |
| multi-gene taxonomic mosaic on a metagenomic contig | WAAFLE plus junction reads | misassembly and incomplete reference taxa |
| recombinant blocks within a recent bacterial lineage | Gubbins | does not identify a physical donor or vehicle |
| plasmid sequence architecture and containment | PlasX plus MobMess | similarity/containment arrows are not transfer arrows |
| current ARG–MGE–host molecule | long reads, validated assembly paths, isolate assays | requires coordinate and junction evidence |

Report method-specific candidates. A best database match is not a demonstrated donor; a
recombination block is not an observed transfer; a phylogenetic incongruence does not date
the event. Preserve ambiguous directions instead of forcing arrows.

## Strain sharing and transmission ladder

| Level | Evidence | Reporting language |
|---|---|---|
| T0 | same species/profile | taxon co-detection |
| T1 | close reference, cluster or consensus profile | related population candidate |
| T2 | high similarity over a sufficiently large jointly callable genome | shared/closely related strain |
| T3 | T2 plus mixture-aware analysis, background calibration, time/location/contact support | transmission-compatible link |
| T4 | dated recombination-aware phylogeny plus converged transmission model and sampling uncertainty | posterior transmission hypothesis |

Use MIDAS2/inStrain/metaSNV for population SNVs, StrainGST/StrainGR for low-abundance
reference-guided comparison, StrainFacts for mixtures, StrainPhlAn for marker phylogenies,
PopPUNK for population structure, Gubbins for recent recombination and TransPhylo only for
an adequately dated tree. Always report jointly callable length/fraction, depth, allele
balance, mixed-strain status, unrelated/background distances, temporal ordering, and
possible unsampled intermediates. Low SNP distance alone does not prove direct
transmission.

## Source tracking is a separate question

SourceTracker2 and FEAST estimate compositional compatibility between a sink and declared
source categories. They do not track individual cells, strains, plasmids or transfer
direction. Keep `source_contribution` separate from `strain_sharing` and
`transmission_posterior`; validate held-out known sources, unknown-source controls,
negative controls, fold leakage and batch effects.

## Evidence-typed network contract

Do not reduce all relationships to an unlabeled source–target–weight table. The canonical
TSV required by `transfer-network-analysis` contains:

`edge_id`, `source_id`, `target_id`, `source_type`, `target_type`, `edge_type`,
`direction_status`, `weight`, `weight_scale`, `evidence_method`, `evidence_unit`,
`sample_id`, `direction_basis`, `uncertainty`, `thresholds`, `provenance_id`.

Supported `edge_type` values and their semantics are:

| Edge type | Default direction | Meaning |
|---|---|---|
| `contains` | directed | sequence/element contains a coordinate-defined feature |
| `host_link` | directed | element/virus has method-specific host evidence |
| `hic_contact` | undirected | normalized proximity-ligation contact |
| `sequence_similarity` | undirected | pairwise sequence similarity under a declared denominator |
| `gene_sharing` | undirected | shared-gene/protein-cluster relationship |
| `cooccurrence` | undirected | sample-level association only |
| `strain_sharing` | undirected | callable-genome relatedness under a fixed rule |
| `source_contribution` | directed | model-estimated source-to-sink mixture contribution |
| `hgt_candidate` | directed or ambiguous | method-specific evolutionary transfer hypothesis |
| `transmission_posterior` | directed | model posterior that one case infected another |

Weights from ANI, contact counts, correlations, mixture fractions and posterior
probabilities are not commensurate. Analyze layers separately by default. If a multiplex
graph is built, preserve edge type, scale, direction basis, uncertainty, method, thresholds
and provenance; never add or average unrelated weights without a prespecified model.

Validate a prepared table with the bundled script:

```bash
set -euo pipefail
input=${EDGE_TABLE:?set EDGE_TABLE}
out=${OUTDIR:-results/network-validation}
[[ -s "$input" && ! -e "$out" ]] || exit 2
mkdir -p "$out"
python3 "skills/transfer-network-analysis/scripts/validate_edges.py" \
  "$input" "$out/edges.normalized.tsv" "$out/edges.summary.json" \
  >"$out/validate.stdout.log" 2>"$out/validate.stderr.log"
[[ -s "$out/edges.normalized.tsv" && -s "$out/edges.summary.json" ]] || exit 3
```

The validator checks schema, controlled edge/direction semantics, finite weights, duplicate
IDs/relations and self-loops, then canonicalizes undirected endpoint order. Passing this
check establishes structural validity only, not biological correctness.

## Nulls, controls and sensitivity

Match each layer to an appropriate null:

- ARG detection: decoys, negative controls, truncated proteins and close non-resistance
  homologues;
- co-location: shuffled coordinates, contig-length/coverage strata and assembly alternatives;
- Hi-C: inter-bin background, restriction-site/abundance corrections and library controls;
- CRISPR: reversed/control targets and contamination screens;
- HGT: taxonomy/reference perturbations, contamination filters and gene-tree alternatives;
- strain sharing: unrelated same-population pairs, callable-genome matching and mixture
  perturbations;
- source tracking: held-out sources, omitted-source tests and batch-blocked folds;
- network topology: degree-preserving, temporal and sampling-aware nulls within each layer.

Report whether headline links persist under stricter and looser defensible thresholds. A
stable artifact remains an artifact if all sensitivity analyses reuse the same biased input.

## Minimum reporting package

Archive:

1. immutable sample/ID/crosswalk manifests and input checksums;
2. software, database, taxonomy and model versions/checksums;
3. commands/configuration, random seeds, logs and explicit failure states;
4. complete native outputs, no-hit/no-call states and exclusion ledgers;
5. coordinate evidence, jointly callable masks, contact/background summaries and controls;
6. typed node/edge tables plus `provenance_id`-addressable records;
7. primary and sensitivity results, uncertainty, and unresolved conflicting evidence;
8. a claim table mapping every conclusion to R/L/T level and experimental versus
   computational support.

Primary literature and tool papers are listed in the repository's
[reference catalogue](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).
