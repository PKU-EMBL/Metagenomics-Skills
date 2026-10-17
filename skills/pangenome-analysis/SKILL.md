---
name: pangenome-analysis
description: >-
  Design bacterial or archaeal pangenome analyses from consistently annotated isolate genomes or MAGs, including sample selection, dereplication, gene-family inference, core/accessory partitions, phylogeny, and phenotype association. Use when choosing Panaroo or PPanGGOLiN and controlling annotation, quality, population structure, and MAG missingness.
license: MIT
compatibility: Requires multiple related genomes and consistent FASTA/GFF/GBFF annotations.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "pangenome,core-genome,accessory-genome,panaroo,ppanggolin,mag"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Pangenome analysis

Pangenomes are sensitive to genome sampling, assembly quality, contamination, and annotation consistency. Resolve these before interpreting gene gain/loss.

## Routing

- Use `$panaroo` for graph-based bacterial pangenomes with explicit annotation-error correction and Roary-compatible presence/absence outputs.
- Use `$ppanggolin` for persistent/shell/cloud partitioning plus regions of genome plasticity, insertion spots, and modules.
- Use `$drep`/`$skani` before analysis when oversampled clonal genomes would dominate results.
- Use `$bakta` or another single pinned annotator for all genomes; do not mix heterogeneous public annotations uncritically.

## Input contract

Create `genomes.tsv` containing genome ID, path, species/lineage, source, quality, completeness, contamination, assembly size, contig count, annotation version, and inclusion reason. IDs must be unique and phenotype labels must not be encoded inconsistently.

For MAGs, predeclare stricter missingness logic. Apparent accessory-gene absence can be assembly incompleteness; fragmented genes can inflate families.

## Workflow

1. Confirm genomes represent a coherent taxonomic scope using ANI and taxonomy.
2. Remove contamination, poor-quality genomes, and unwanted replicate/clonal imbalance using documented rules.
3. Reannotate all genomes consistently.
4. Run `$panaroo` or `$ppanggolin` with pinned versions and parameters.
5. Inspect family-size, core-size, singleton, and per-genome gene-count distributions.
6. Build a recombination-aware core phylogeny when evolutionary inference is needed.
7. Test phenotype associations with population structure, geography, and sampling represented.
8. Repeat key findings under alternate quality, core, and paralogue thresholds.

## Quality gates

- all expected genomes appear exactly once in the presence/absence matrix;
- gene counts and core proportion do not reveal unexamined outliers;
- annotations use the same caller/database/configuration;
- paralogues and fragmented genes are not silently collapsed;
- phylogenetic support and recombination treatment are reported;
- associations include effect sizes and corrected uncertainty, not only p-values.

## Deliverables

- frozen genome/annotation manifest and checksums;
- gene-family membership and binary presence/absence matrix;
- core alignment and tree where applicable;
- persistent/core, shell/accessory, cloud/singleton summaries using tool-specific terminology;
- exclusion log, commands, environment, and sensitivity analysis.

## Analytical thinking

A pangenome is a property of the sampled genomes and clustering definition, not a fixed species constant. Gene-family presence does not guarantee expression or function, and MAG absence is especially uncertain. Do not compare core/accessory counts across tools or parameter sets as though definitions were identical.
