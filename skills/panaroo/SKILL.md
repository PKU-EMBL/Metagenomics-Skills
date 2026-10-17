---
name: panaroo
description: >-
  Construct graph-based bacterial pangenomes with Panaroo from consistently annotated GFF3 genomes, correcting annotation artifacts and producing gene presence/absence, graph, and core-alignment outputs. Use for within-species isolate or carefully quality-gated MAG collections.
license: MIT
compatibility: Requires Panaroo 1.8.0 and GFF3 annotations with compatible embedded genome sequence; MAFFT/Clustal is needed for alignment modes.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "panaroo,pangenome,core-genome,accessory-genome,gff,graph"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.8.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Panaroo

Panaroo builds and cleans a pangenome graph from prokaryotic annotations. Use one species/ANI-coherent collection and one annotation pipeline.

## Inputs and preflight

- one unique sample per GFF3;
- consistently generated CDS identifiers and translation table;
- genome QC, taxonomy/ANI, source, phenotype, and inclusion metadata;
- GFF3 files containing or linked to the correct nucleotide sequence.

```bash
set -euo pipefail
shopt -s nullglob
gffs=(annotations/*.gff)
((${#gffs[@]} >= 3)) || { echo "need at least three GFFs" >&2; exit 2; }
printf '%s\n' "${gffs[@]}" | sort > panaroo_inputs.txt
[[ $(sort panaroo_inputs.txt | uniq | wc -l) -eq ${#gffs[@]} ]] || exit 2
panaroo --version
```

## Run strict cleaning and core alignment

```bash
out=panaroo_out
[[ ! -e "$out" ]] || { echo "use a fresh output directory" >&2; exit 2; }
panaroo -i "${gffs[@]}" -o "$out" --clean-mode strict \
  --remove-invalid-genes -a core --core_threshold 0.95 -t 16 \
  >panaroo.stdout.log 2>panaroo.stderr.log
for f in gene_presence_absence.csv gene_presence_absence.Rtab final_graph.gml \
         gene_data.csv combined_DNA_CDS.fasta combined_protein_CDS.fasta; do
  [[ -s "$out/$f" ]] || { echo "missing $f" >&2; exit 3; }
done
```

`--remove-invalid-genes` is useful for annotations that violate expected CDS assumptions, but review how many genes/genomes it affects. Use `--clean-mode sensitive` only when rare plasmids/accessory genes justify accepting more contamination/artifacts, and present it as sensitivity analysis.

## Validate

- confirm each input genome appears once in `gene_presence_absence.Rtab`;
- inspect per-genome gene counts, family sizes, core fraction, singletons, and refound/fragmented genes;
- review outlier genomes before biological inference;
- use `core_gene_alignment_filtered.aln` for phylogeny when generated and document recombination treatment;
- compare strict/sensitive or core-threshold choices for key conclusions.

`gene_presence_absence.csv` stores gene membership, while `.Rtab` is binary. `final_graph.gml` captures graph structure. Keep `gene_data.csv` to map internal IDs back to annotations.

## Recovery and provenance

Do not reuse a partially populated output directory after changing input or parameters. Archive the sorted input manifest/checksums, annotation versions, Panaroo environment, command/logs, outputs, and excluded-genome reasons.

## Analytical thinking

Apparent gene absence can be incomplete assembly or annotation failure, especially in MAGs. Gene-family presence does not prove function/expression. Core size is conditional on sample composition, cleaning mode, clustering, and core threshold.

## Source

- https://github.com/gtonkinhill/panaroo
