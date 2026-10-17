---
name: eukaryotic-metagenomics
description: >-
  Plan microbial-eukaryote recovery from metagenomes, including contig-domain classification, eukaryotic gene prediction, binning, EukCC quality/taxonomy, and contamination-aware interpretation. Use for fungi, protists, or other microbial eukaryotes that prokaryote-focused MAG workflows and marker sets handle poorly.
license: MIT
compatibility: Requires assembled contigs and substantial compute; tool/database requirements vary by eukaryotic lineage.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "microbial-eukaryotes,protists,fungi,tiara,eukcc,whokaryote,metaeuk"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Eukaryotic metagenomics

Do not apply bacterial gene callers, tetranucleotide expectations, or CheckM/CheckM2 marker models to microbial eukaryotes without justification.

## Routing

| Task | Preferred skill | Boundary |
|---|---|---|
| Eukaryote/prokaryote/organelle contig triage | `$tiara` | sequence classifier; minimum length matters |
| Feature-based eukaryotic contig classification | `$whokaryote` | contigs below 5 kb or with fewer than two genes may be unclassified |
| Homology-based eukaryotic gene prediction | `$metaeuk` | depends on protein reference coverage |
| Bin completeness, contamination, taxonomy | `$eukcc` | eukaryote-specific marker sets and database |
| General conserved orthologue completeness | `$busco` | lineage dataset must match target |

Use concordance between classifiers rather than treating one prediction as truth. Keep mitochondrial/plastid sequences distinguishable from nuclear contigs.

## Inputs

- QC reads, assemblies, graph/coverage files, and sample manifest;
- contig lengths and multi-sample coverage;
- candidate eukaryotic contigs with original IDs retained;
- gene predictions suited to intron-rich genomes when needed;
- pinned Tiara, EukCC, BUSCO, and protein-reference versions.

Long-read or hybrid assemblies can improve repeat resolution and phasing, but polishing errors can disrupt genes. Short-read-only assemblies may fragment low-abundance and repeat-rich genomes.

## Workflow

1. Run `$tiara` and optionally `$whokaryote`; retain probability/class columns.
2. Separate nuclear candidates, organelles, prokaryotic contigs, and unclassified contigs without discarding the latter prematurely.
3. Bin using coverage, composition, linkage, and lineage-aware evidence; manually inspect discordant contigs.
4. Predict genes with eukaryote-aware methods and screen prokaryotic contamination.
5. Evaluate bins with `$eukcc` and an appropriate `$busco` lineage where useful.
6. Assign taxonomy from multiple genes/reference placement; report unresolved bins.
7. Quantify with mappings to a dereplicated catalogue and explicit ambiguous-read handling.

## Verification and deliverables

For every bin, report size, contig count, N50, GC, coverage, classifier composition, EukCC completeness/contamination/lineage, BUSCO lineage/results if used, organelle content, and taxonomic evidence. Verify that sequence IDs survive every split and that total lengths reconcile between source and partitions.

Flag bins with conflicting contig classes, extreme coverage/GC, duplicated markers, or lineage placement supported by few markers. Re-run quality estimates after decontamination rather than editing only summary tables.

## Analytical thinking

Eukaryotic completeness models are lineage- and database-dependent. A predicted eukaryotic contig is not a recovered eukaryotic genome; a “complete” marker set does not establish correct phasing, ploidy, or absence of prokaryotic contamination. Preserve unknowns and report tool disagreement.
