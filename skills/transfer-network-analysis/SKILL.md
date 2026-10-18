---
name: transfer-network-analysis
description: >-
  Build and audit evidence-typed networks for ARG–MGE containment, MGE–host links,
  gene sharing, HGT candidates, source contributions, strain sharing, and transmission
  posteriors. Use when integrating propagation or migration edges while preventing
  co-occurrence, Hi-C contact, sequence similarity, and direct transmission from being conflated.
license: MIT
compatibility: Requires a tab-delimited edge table with stable node IDs, explicit edge semantics, method provenance, and uncertainty.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "network,transmission,HGT,source-sink,host-linkage,evidence-graph"
  metagenomics.stage: "report"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "bundled validator smoke-tested with synthetic fixtures; biological analyses not executed"
---

# Transfer and migration network analysis

A graph is only as meaningful as its edge definition. Keep different evidence layers
separate, even when they share nodes.

## Do not merge these edge types

| Edge type | Meaning | Direction |
|---|---|---|
| `contains` | coordinate containment (for example ARG in MGE) | directed |
| `host_link` | element-to-host evidence | directed |
| `hic_contact` | normalized proximity-ligation contact | undirected |
| `sequence_similarity` | sequence-level similarity | undirected |
| `gene_sharing` | shared gene-content relation | undirected |
| `cooccurrence` | statistical sample association | undirected |
| `strain_sharing` | genomic similarity under callability gates | undirected |
| `source_contribution` | modeled source-to-sink fraction | directed |
| `hgt_candidate` | inferred transfer; direction can be ambiguous | directed/ambiguous |
| `transmission_posterior` | posterior who-infected-whom probability | directed |

An association network from `$netcomi` is not a transfer network. A MobMess graph is
not a host network. A Hi-C edge is not direct transmission.

## Required edge schema

Use one TSV with these columns:

```text
edge_id,source_id,target_id,source_type,target_type,edge_type,direction_status,
weight,weight_scale,evidence_method,evidence_unit,sample_id,direction_basis,
uncertainty,thresholds,provenance_id
```

Use `NA` for inapplicable fields, not an empty string. Controlled node types are `arg`,
`gene`, `feature`, `mge`, `plasmid`, `virus`, `integron`, `transposon`, `ice`, `ime`,
`contig`, `mag`, `genome`, `strain`, `host`, `taxon`, `sample`, `source`, `sink`,
`person`, `site`, and `unknown`; one node ID must retain one type. `weight_scale` must
define the number (for example posterior probability, normalized contact, ANI,
contribution, correlation, or event count). Directed/ambiguous edges require a non-NA
`direction_basis`. Keep raw evidence in method-native tables.

## Validate the edge contract

Bundled script `scripts/validate_edges.py` checks required columns, IDs, node-type
consistency, finite/range-valid weights, direction semantics, duplicate
directed/undirected edges, and emits a normalized table, checksums, and layer summary. It
does not judge biological validity.

```bash
set -euo pipefail
input=${1:?usage: validate-network.sh edges.tsv out_dir}
out=${2:?usage: validate-network.sh edges.tsv out_dir}
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
python3 skills/transfer-network-analysis/scripts/validate_edges.py \
  "$input" "$out/edges.validated.tsv" "$out/edge-summary.json" \
  >"$out/validate.stdout.log" 2>"$out/validate.stderr.log"
[[ -s "$out/edges.validated.tsv" && -s "$out/edge-summary.json" ]] || exit 3
```

When a copied skill is installed outside this repository, resolve the script relative
to that skill directory rather than the repository root.

## Analysis workflow

1. Freeze node identity and edge semantics before computing graph statistics.
2. Validate each evidence layer independently and retain rejected edges with reasons.
3. Calibrate thresholds against controls/nulls appropriate to the method.
4. Analyze layers separately; use a multiplex graph only when every layer remains labeled.
5. Report component size, degree, centrality, communities, and robustness by edge type.
6. Bootstrap samples/reads or perturb thresholds to assess edge and hub stability.
7. Restrict label permutations to exchangeable biological units and correct multiplicity.
8. Overlay time and direction only when supported; never orient undirected similarity.

## Network-specific controls

- correct degree/centrality for sampling and database opportunity where possible;
- avoid counting many genes on one element as independent transfer events;
- collapse exact duplicate evidence without collapsing independent methods;
- test whether hubs are driven by sequence length, abundance, assembly quality, or
  reference representation;
- preserve negative/no-link evidence and unsampled/unknown nodes;
- report how multi-host, multi-source, and ambiguous edges were handled.

## Interpretation

Centrality is not biological importance, transmissibility, or causal influence. A dense
component can arise from shared ancestry, broad host range, high abundance, incomplete
sampling, or database bias. Directed edges remain conditional on the inference model and
sampled candidates.

See the
[ARG–MGE–host–strain evidence guide](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/arg-mge-host-strain.md).

## Related skills

`arg-mge-host-linkage` · `horizontal-gene-transfer` · `strain-transmission` ·
`source-tracking` · `sourcetracker2` · `feast` · `mobmess` · `metachip` ·
`transphylo` · `netcomi`
