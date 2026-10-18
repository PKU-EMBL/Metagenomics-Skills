---
name: gubbins
description: >-
  Detect recombination-enriched regions and infer a recombination-aware phylogeny from a
  whole-genome alignment of closely related bacterial isolates with Gubbins. Use before
  SNP-distance or transmission analyses when sample relatedness, alignment provenance,
  reference gaps, tree convergence, and masked versus unmasked variation must be explicit.
license: MIT
compatibility: Requires Gubbins 3.4.3, a whole-genome multi-FASTA alignment of one low-diversity lineage, an installed tree builder, and adequate CPU/RAM.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Gubbins,recombination,phylogeny,SNP,outbreak,bacteria"
  metagenomics.upstream: "https://github.com/nickjcroucher/gubbins"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "3.4.3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/output contract reviewed against upstream manual; not executed here"
---

# Gubbins

Gubbins iteratively identifies clusters of substitutions consistent with recombination and
reconstructs a clonal phylogeny. It is intended for closely related bacterial isolates,
not diverse species-wide or mixed-metagenome alignments.

## Input contract

- one lineage selected without reference to the outcome being tested;
- one row per isolate in a whole-genome alignment with stable unique IDs;
- alignment from the same reference and masking policy for all samples;
- removal of duplicate sample IDs and audit of near-identical technical replicates;
- assembly/mapping contamination and mixed-strain QC;
- rootedness/clock and temporal analyses handled downstream, not assumed by Gubbins.

Reference-mapping alignments must preserve invariant/core sites and callable masks where
needed; a SNP-only alignment can distort branch lengths and recombination inference.

## Run

```bash
set -euo pipefail
aln=${ALIGNMENT:?set ALIGNMENT to whole-genome FASTA alignment}
out=${OUT_PREFIX:-results/gubbins/lineage}
[[ -s "$aln" ]] || exit 2
for path in "${out}.final_tree.tre" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "use a new output prefix: $out" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")"
run_gubbins.py --prefix "$out" --threads 16 --tree-builder iqtree \
  --first-tree-builder fasttree --iterations 5 --converge-method weighted_robinson_foulds \
  "$aln" >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "${out}.final_tree.tre" && -s "${out}.filtered_polymorphic_sites.fasta" && \
   -s "${out}.per_branch_statistics.csv" && -s "${out}.recombination_predictions.gff" && \
   -s "${out}.node_labelled.final_tree.tre" ]] || exit 3
```

Tree builders and models are configurable. Record the exact implementation and executable
versions; do not silently switch because one dependency is unavailable.

## Validation

- verify all alignment samples occur exactly once in every output tree;
- inspect run logs, iteration convergence, branch support, and per-branch statistics;
- examine predicted blocks in genome coordinates and sensitivity to iterations/tree model;
- compare masked and unmasked SNP distances and tree topology;
- audit isolates with high recombination, long branches, low callability, or contamination;
- use dated tips and clock diagnostics before `$transphylo`.

Recombination predictions are statistical regions enriched for clustered substitutions;
phage, repeats, mapping artifacts, selection, and structural variation are alternatives.

## Recovery and provenance

Do not append new genomes to old results. Rebuild the alignment and rerun with a new prefix.
Record Gubbins and tree-builder versions, input alignment/checksum, reference and alignment
workflow, masking/callability rules, commands, iterations, convergence metric, seed if
available, and all excluded samples.

## Interpretation

A recombination-masked tree approximates clonal ancestry under the model. It does not by
itself yield donor/recipient events, direct transmission, infection dates, or a molecular
clock. Overmasking can remove epidemiologically useful mutations; undermasking can inflate
distance.

## Source

- https://github.com/nickjcroucher/gubbins
- https://doi.org/10.1093/nar/gku1196

## Related skills

`strain-transmission` · `transphylo` · `poppunk` · `iqtree` · `fasttree` ·
`horizontal-gene-transfer` · `bwa` · `samtools`
