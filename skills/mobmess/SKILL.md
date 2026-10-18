---
name: mobmess
description: >-
  Cluster plasmid sequences, infer backbone/compound plasmid systems, and export plasmid
  similarity networks with MobMess. Use for nonredundant plasmid catalogues and architecture
  comparisons when circularity labels, MUMmer thresholds, graph direction, and the difference
  between sequence containment and biological transfer are explicit.
license: MIT
compatibility: Requires Linux, Python 3.7+, PlasX utilities, MUMmer4, plasmid candidate FASTA, and a complete/circular status table.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MobMess,plasmid,network,backbone,compound-plasmid,MUMmer"
  metagenomics.upstream: "https://github.com/michaelkyu/MobMess"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "commit 97c0cfc0f810"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/output contract reviewed against upstream; not executed here"
---

# MobMess

MobMess aligns putative plasmids, clusters near-redundant sequences, and infers
backbone/compound “plasmid systems.” It expects plasmid candidates selected upstream and
uses complete/circular status to define possible backbones.

## Inputs

- nucleotide FASTA containing only the declared plasmid candidate set;
- two-column, headerless table: sequence ID and `True/False` or `1/0` completeness;
- unique IDs matching exactly between FASTA and table;
- a documented circularity method and false-circularity checks;
- predeclared local identity and query-coverage thresholds.

Do not mark a contig complete from an assembler circular label alone; inspect terminal
alignment, read-spanning support, repeats, and length.

## Infer systems

```bash
set -euo pipefail
fasta=${PLASMIDS:?set PLASMIDS to candidate FASTA}
complete=${COMPLETE_TABLE:?set COMPLETE_TABLE}
out=${OUT_PREFIX:-results/mobmess/plasmids}
[[ -s "$fasta" && -s "$complete" ]] || exit 2
for path in "${out}_ani.txt" "${out}_contigs.txt" "${out}_clusters.txt" \
  "${out}_systems.txt" "${out}_contig_graph.graphml" \
  "${out}_cluster_graph.graphml" "${out}.tmp" \
  "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")" "${out}.tmp"
mobmess systems --sequences "$fasta" --complete "$complete" \
  --output "$out" --threads 16 --min-similarity 0.90 --min-coverage 0.90 \
  --tmp "${out}.tmp" >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "${out}_ani.txt" && -s "${out}_contigs.txt" && \
   -s "${out}_clusters.txt" && -s "${out}_systems.txt" && \
   -s "${out}_contig_graph.graphml" && \
   -s "${out}_cluster_graph.graphml" ]] || exit 3
```

The 0.90 identity/coverage values are upstream defaults and reproduce the documented
system concept; they are not universal plasmid species boundaries. Analyze sensitivity
before comparing environments.

## Outputs and validation

- `_ani.txt`: asymmetric alignment coverage plus local/global identity;
- `_contigs.txt`: contig, cluster type, circularity, representative, and system;
- `_clusters.txt` / `_systems.txt`: inferred architecture levels;
- `_cluster_graph.txt`, `_contig_graph.graphml`, and `_cluster_graph.graphml`:
  directed containment/similarity relations.

The pinned source writes `_cluster_graph.graphml`; an older README tutorial refers to a
`_clusters.graphml` example. Gate the source-emitted name for the pinned commit.
Reconcile every FASTA ID, completeness label, cluster, and representative. Inspect
backbones supported by very few sequences and systems driven by fragmented contigs.
Compare candidate status with PlasX/geNomad/MOB-suite and annotate ARG cargo by exact
coordinates, not by system name.

## Recovery and provenance

Pairwise alignment is expensive; a complete `_ani.txt` can be reused with `--ani` only
for the identical FASTA, MUMmer version, and thresholds. Otherwise use a new prefix.
Record MobMess/PlasX commits, MUMmer version, FASTA/checksums, circularity method,
thresholds, command, and graph-export version.

## Interpretation

Graph arrows encode sequence containment/asymmetric alignment, not donor-to-recipient
transfer. A compound/backbone system is an inferred evolutionary architecture, not a
physically closed plasmid in every sample. Network hubs can reflect fragmented assembly,
sequence length, and sampling density.

## Source

- https://github.com/michaelkyu/MobMess
- https://doi.org/10.1038/s41564-024-01610-3

## Related skills

`mobilome-analysis` · `plasx` · `genomad` · `mob-suite` ·
`arg-mge-host-linkage` · `horizontal-gene-transfer` · `transfer-network-analysis`
