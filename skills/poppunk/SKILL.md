---
name: poppunk
description: >-
  Cluster bacterial isolate or high-quality genome assemblies for genomic epidemiology
  with PopPUNK core and accessory k-mer distances. Use for assignment to a validated
  species database, stable nomenclature, new model fitting/QC, outbreak-context screening,
  and population stratification before fine-scale phylogeny or recombination analysis.
license: MIT
compatibility: Requires PopPUNK 2.7.8 with pp-sketchlib 2.0.1, one species per analysis, assemblies or supported reads, and preferably a validated species database.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PopPUNK,genomic-epidemiology,clustering,kmer,population-structure"
  metagenomics.upstream: "https://github.com/bacpop/PopPUNK"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.7.8"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/database/output contract reviewed against upstream; not executed here"
---

# PopPUNK

PopPUNK separates within- and between-strain core/accessory distances using variable-length
k-mers. Prefer assignment to a curated species database over fitting a new model.

## Input contract

- one bacterial species/lineage and one assembly/read set per sample;
- unique sample names and a headerless query file: sample ID, then sequence path(s);
- assembly quality, contamination, length, and ambiguous-base gates;
- pinned PopPUNK database/model plus its documentation and checksum;
- predeclared policy for stable labels, novel clusters, and cluster merges.

Mixed metagenomic assemblies are invalid. MAGs require stringent completeness,
contamination, and consensus review because missing accessory sequence biases distance.

## Assign to an existing database

```bash
set -euo pipefail
queries=${QUERY_FILE:?set QUERY_FILE}
db=${POPPUNK_DB:?set POPPUNK_DB}
out=${OUTDIR:-results/poppunk-assignment}
[[ -s "$queries" && -d "$db" ]] || exit 2
for path in "$out" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")"
poppunk_assign --db "$db" --query "$queries" --output "$out" \
  --threads 16 --stable >"${out}.stdout.log" 2>"${out}.stderr.log"
clusters="$out/$(basename "$out")_clusters.csv"
[[ -s "$clusters" && -s "$out/$(basename "$out").h5" ]] || exit 3
```

`--stable` assigns by nearest-neighbor cluster and avoids merging existing labels, but new
samples can be `NA`; it is not mathematically possible to guarantee stable nomenclature
under every database update. Remove `--stable` only under a declared update policy.

## New-species workflow

When no validated database exists: create sketches with `poppunk --create-db`, QC the
reference set, fit a model, inspect core/accessory distance plots and cluster topology, and
refine under frozen criteria. Separate model development from downstream outcome testing.

## Validation

- reconcile every query, warning, QC status, and cluster assignment;
- inspect nearest references, core/accessory distances, novel clusters, and merge warnings;
- compare clusters with a tree and epidemiological/background structure;
- use `$gubbins` only after selecting a recent, low-diversity lineage and constructing a
  whole-genome alignment;
- test cluster stability to assembly QC and database version.

## Recovery and provenance

Query sketches can be reused only with identical input, software/backend, k-mer settings,
and database. Database/model updates require a new output and explicit mapping of old to
new labels. Record PopPUNK/pp-sketchlib versions, database release/checksum, query file,
input checksums, commands, QC, model files, and assignment policy.

## Interpretation

A PopPUNK cluster represents genomic population structure under one fitted database/model.
It is not a direct-transmission cluster, and cluster membership does not establish outbreak
membership, direction, time, or phenotype.

## Source

- https://github.com/bacpop/PopPUNK
- https://doi.org/10.1101/gr.241455.118

## Related skills

`strain-transmission` · `gubbins` · `transphylo` · `iqtree` · `pangenome-analysis` ·
`checkm2` · `gunc`
