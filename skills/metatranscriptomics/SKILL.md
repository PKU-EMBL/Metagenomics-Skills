---
name: metatranscriptomics
description: >-
  Design and execute microbial metatranscriptomic analysis from RNA controls and rRNA depletion through QC, host/rRNA removal, gene/pathway quantification, matched-metagenome normalization, and differential analysis. Use when measuring community RNA while keeping activity, abundance, compositionality, and protocol bias distinct.
license: MIT
compatibility: Requires RNA-seq FASTQ, sample metadata, rRNA references, and selected QC/alignment/quantification/statistics tools.
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "metatranscriptomics,rna-seq,rrna-depletion,sortmerna,expression,activity"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "not-applicable"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow guidance; tool execution is delegated"
---

# Metatranscriptomics

Microbial RNA profiles combine organism abundance, transcription, RNA stability, extraction, depletion, and library effects. “More RNA” is not automatically “more active.”

## Experimental contract

Record preservation time/temperature, extraction protocol, DNase treatment, rRNA-depletion kit/probes, strandedness, library type, read layout/length, spike-ins, batch, and matched DNA availability. Include extraction/library blanks and positive controls. Randomize conditions across batches.

Distinguish total RNA, mRNA-enriched, and metatranscriptome protocols. Depletion efficiencies and taxonomic biases differ and should not be pooled uncritically.

## Workflow

1. **Raw QC** — `$fastqc`/`$fastp`; inspect quality, adapters, duplication, insert length, and overrepresented sequences.
2. **Host removal** — `$hostile`/`$bowtie2` against a pinned host reference; preserve removed fractions.
3. **rRNA depletion** — `$sortmerna`; report rRNA/non-rRNA pairs and database release.
4. **Residual DNA check** — inspect intergenic/strand patterns and negative controls; computational filtering cannot replace DNase controls.
5. **Reference strategy** — map to a matched sample/cohort gene catalogue when available, or use a documented public catalogue/database.
6. **Quantification** — gene counts/transcript abundance with `$salmon`, Bowtie2-based counting, or `$humann`; state multi-mapping policy.
7. **Functional aggregation** — preserve gene-to-family/pathway mappings and unmapped/unclassified fractions.
8. **Statistics** — use raw counts and a design-aware RNA-seq model or compositional method as appropriate; include batch and repeated measures.
9. **Matched DNA comparison** — compute RNA/DNA ratios only after harmonizing feature definitions, detection limits, and normalization.

## Stage gates

For each sample report raw pairs, post-QC pairs, host fraction, rRNA fraction, non-rRNA pairs, mapped/assigned fraction, library complexity, strand consistency, and feature totals. Investigate samples with extreme depletion, low non-rRNA yield, or control signal before group testing.

Require exact sample-ID alignment and an explicit handling rule for zeros/non-detects. Do not divide tiny RNA or DNA values without censoring/sensitivity analysis.

## Deliverables

- immutable raw and filtered FASTQ checksums;
- per-stage retention table and MultiQC report;
- pinned rRNA/host/gene databases and checksums;
- gene/family/pathway count and normalized tables with mapping provenance;
- statistical design, contrasts, effect sizes, uncertainty, and sensitivity analyses;
- command/environment logs and observed failures/no-hit samples.

## Analytical thinking

RNA abundance supports transcriptional potential at sampling time, not protein abundance, metabolic flux, or organism growth. RNA/DNA ratios can partly account for organism abundance but amplify uncertainty and inherit both assays' biases. Use “transcript abundance” or “relative transcriptional allocation” unless direct activity validation exists.
