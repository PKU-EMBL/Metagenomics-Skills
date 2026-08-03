# End-to-end shotgun pathway

Integrates Modules A–G. Prefer **Module F (BASALT)** for refined multi-assembly
MAG recovery; prefer **Modules C–E** for profiling, gene catalogues, and
classical MAG catalogues.

## Canonical stage order

```text
raw reads + metadata
  → Module B: quality control and host depletion
  → Module C: read-based taxonomy and function (optional)
  → Module D: assembly and gene catalogue (optional)
  → Module E or F: MAG recovery
  → quality assessment (CheckM2 preferred)
  → dereplication when building a non-redundant genome set
  → taxonomy (GTDB-Tk) and genome abundance (CoverM)
  → Module G: statistics and figures
```

Every composition or MAG claim requires documented reads, databases, parameters,
and quality-control resources.

## Shared preprocessing defaults

- Prefer **fastp** for paired-end QC; retain JSON/HTML summaries.
- Prefer **KneadData** with `--reorder` for host depletion; record host genome ID.
- Keep checksums of retained reads; prefer dehosted deposition for human data.
- Mate concordance is required for salmon, MetaWRAP, and BASALT connectivity.

## Coverage rules for genome modules

- Coverage must derive from reads designated as evidence for that assembly.
- Multi-sample depth is informative only within biologically related strata.
- Contig identifiers must match when importing external binsets into BASALT.

## Quality and catalogue construction

1. Prefer **CheckM2** for bacterial/archaeal estimates; record database identity.
2. Publication filters are often stricter than BASALT refinement entry gates.
3. Dereplicate with an explicit ANI threshold and tool version.
4. Treat GTDB-Tk taxonomy as a separate claim layer from binner labels.
5. Annotate the final dereplicated MAG set unless analysing discarded candidates.

## PKU-EMBL context

For extreme environments, host-associated systems, or AI-method studies:

- Preserve strata that define the scientific contrast.
- Marker-based completeness can be conservative for unusual lineages.
- Separate learned models, classical binning, and manual curation in reporting.

## Deliverables checklist

- Design / metadata manifest
- Dehosted reads or regenerable host-depletion command + host DB ID
- Profiling tables with method and database release (if claimed)
- Assembly FASTA + assembler command
- Gene NR FASTA + quantification + annotation (if claimed)
- MAG set + CheckM2/CheckM + dRep + GTDB (+ CoverM)
- Software versions and checksums for inputs, databases, and BASALT models
- BASALT citation when Module F is used
