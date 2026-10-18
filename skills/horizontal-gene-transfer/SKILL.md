---
name: horizontal-gene-transfer
description: >-
  Design and audit horizontal or lateral gene-transfer analyses from MAGs, genomes,
  metagenomic contigs, pangenomes, and time series. Use to choose MetaCHIP, WAAFLE,
  HGTector, recombination analysis, mobile-context evidence, or donor–recipient networks
  while separating historical candidates from directly observed recent transfer.
license: MIT
compatibility: Requires quality-controlled sequences, taxonomy or rooted species trees where applicable, and read support for assembly-based claims.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "HGT,LGT,gene-transfer,phylogenetic-discordance,recombination,network"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Horizontal gene transfer

First define the timescale and inference target. “HGT” may mean ancient acquisition,
a recent recombination tract, a mobile cargo candidate, or observed transfer during a
longitudinal experiment. These are not interchangeable.

## Routing

| Input/question | Prefer | Main signal |
|---|---|---|
| Community genomes/MAGs plus rooted species tree | `$metachip` | best-match + gene/species phylogeny reconciliation |
| Fragmentary metagenomic contigs | `$waafle` | taxonomic mosaic across neighboring genes |
| One or many genome proteomes | `$hgtector` | homology-hit distribution outliers |
| Recent recombination within one lineage | `$gubbins` | spatial SNP-density tracts on a whole-genome alignment |
| ARG/MGE cargo and hosts | `$arg-mge-host-linkage` | coordinate and physical-link evidence |
| Plasmid architecture/gene sharing | `$mobmess` | sequence containment/similarity network |
| Typed transfer graph | `$transfer-network-analysis` | evidence-preserving edge table |

MetaCHIP and HGTector are poorly suited to asserting real-time transfer; WAAFLE
candidates can be chimeric assemblies. Gubbins detects recombination-like SNP clusters,
not necessarily the mobile vehicle or donor.

## Input contract

- unique sequence/genome/gene IDs and gene-to-contig coordinates;
- CheckM2/GUNC quality and contamination flags for MAGs;
- taxonomy release and the exact grouping ranks used;
- rooted species tree with matching tips for phylogenetic methods;
- assembly and raw-read junction evidence for contig methods;
- sampling time, habitat, subject/contact structure, and batch;
- predeclared sequence similarity, support, multiplicity, and donor-reporting rules.

Do not infer donor direction merely because one sampled genome has the closest match.
The true donor can be unsampled; methods often report the closest sampled donor **group**.

## Workflow

1. Remove or flag contaminated/chimeric genomes and unsupported assembly joins.
2. Run a method matched to the sequence unit and evolutionary timescale.
3. Retain every component score: similarity, topology/support, taxonomic distance,
   synteny, flanks, and read support.
4. Annotate candidate genes and mobile context without selecting only ARGs of interest.
5. Test sensitivity to taxonomy grouping, reference database, and thresholds.
6. Compare candidate frequency with callable/searchable gene background.
7. Construct a typed network; do not merge HGT edges with co-occurrence or Hi-C edges.
8. Validate high-impact candidates with long reads, closed isolates, or experiments.

## Required outputs

```text
event_id,gene_id,recipient_sequence,recipient_group,putative_donor_group,
direction_status,method,similarity,alignment_coverage,tree_support,synteny,
read_junction_support,mge_context,function,sample_id,timepoint,filter_status,
filter_reason,software_version,database_or_tree_id,provenance_id
```

Also report searchable genes/genomes, candidates rejected by QC, no-event samples, and
uncertainty. Network edge weight must state whether it counts genes, sequence length,
posterior support, or normalized opportunity.

## Confounders and falsification

- contamination, conserved genes, paralogy, incomplete lineage sorting, gene loss;
- compositional convergence and uneven reference sampling;
- fragmented or chimeric assemblies;
- recombination/mutation hotspots and alignment errors;
- ecological co-occurrence mistaken for genetic exchange;
- repeated detection of one ancestral event counted as many independent transfers.

A robust candidate should survive stricter sequence/coverage filters and have coherent
flanking, phylogenetic, or mobility evidence. A plausible alternative explanation must
be documented for every headline event.

## Interpretation

Use “candidate HGT/LGT,” “phylogenetic discordance,” or “mosaic contig” unless direct
transfer was observed. A directed chord diagram from a reconciliation algorithm remains
model-based and sample-conditional. Association of HGT frequency with environment is not
proof that ecology caused transfer.

See the
[ARG–MGE–host–strain evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`metachip` · `waafle` · `hgtector` · `gubbins` · `mobmess` ·
`arg-mge-host-linkage` · `mobilome-analysis` · `strain-transmission` ·
`transfer-network-analysis` · `pangenome-analysis` · `iqtree`
