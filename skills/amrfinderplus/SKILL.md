---
name: amrfinderplus
description: >-
  Detect acquired antimicrobial-resistance genes, curated resistance mutations, stress or
  biocide genes, and selected virulence factors with NCBI AMRFinderPlus. Use for assembled
  isolate genomes, high-quality MAGs, or metagenomic proteins when software/database
  versions, organism-specific scope, and genotype-to-phenotype limits must be explicit.
license: MIT
compatibility: Requires AMRFinderPlus 4.2.7, its matching NCBI database, assembled nucleotide and/or protein FASTA, and compatible GFF for combined mode.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "AMRFinderPlus,AMR,ARG,mutation,virulence,NCBI"
  metagenomics.upstream: "https://github.com/ncbi/amr"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "4.2.7"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and database contract reviewed against upstream; not executed here"
---

# AMRFinderPlus

AMRFinderPlus combines curated protein/nucleotide models. The optional `--plus`
scope adds stress, heat, biocide, and selected virulence genes; it does not turn
all output rows into AMR determinants.

## Inputs and scope

- protein FASTA, assembly FASTA, and GFF must use mutually consistent IDs;
- freeze the AMRFinderPlus database before cohort analysis and record its release;
- use `-O/--organism` only for a supported, defensibly assigned isolate/genome;
- do not run organism-specific mutation interpretation on an unresolved mixed metagenome.

Protein plus GFF plus nucleotide input gives the most context for an annotated
isolate or MAG. Nucleotide-only mode is available for unannotated assemblies.

## Run combined mode

```bash
set -euo pipefail
sample=${SAMPLE_ID:?set SAMPLE_ID}
proteins=${PROTEINS:?set PROTEINS to protein FASTA}
gff=${GFF:?set GFF to compatible CDS GFF}
contigs=${CONTIGS:?set CONTIGS to assembly FASTA}
out=${OUTDIR:-results/amrfinderplus/$sample}
[[ -s "$proteins" && -s "$gff" && -s "$contigs" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
amrfinder --version >"$out/software-version.txt" 2>&1
amrfinder --database_version >"$out/database-version.txt" 2>&1
amrfinder -p "$proteins" -g "$gff" -n "$contigs" --plus \
  --threads 16 --name "$sample" >"$out/amrfinder.tsv" 2>"$out/amrfinder.log"
[[ -s "$out/amrfinder.tsv" ]] || exit 3
awk -F '\t' 'NR==1 { if (NF < 10) exit 1 }' "$out/amrfinder.tsv"
```

For nucleotide-only screening, replace the combined input flags with `-n
assembly.fna`. Update the database in a controlled setup step with `amrfinder -u`,
then freeze and checksum it; never update halfway through a cohort.

## Organism-specific mutations

A curated organism option enables supported point-mutation logic. Record the exact
organism string and also retain `--mutation_all FILE` when auditing callable genotype
states. Absence of a reported mutation can mean no gene, no callable locus, an unknown
mutation, or a susceptible genotype; distinguish these states.

## Validation

- reconcile all output sequence/protein identifiers to the input and GFF;
- inspect `Method`, `Scope`, subclass, identity, coverage, partial/end flags, and hierarchy;
- separate `CORE` AMR rows from `PLUS` stress/virulence rows;
- retain header-only no-hit outputs as valid no-call results;
- examine fragmented MAG/contig-end hits and paralogous housekeeping genes;
- compare critical calls with `$rgi` or `$resfinder` without merging accessions blindly.

## Recovery and provenance

A software/database mismatch, malformed GFF, or interrupted run requires a fresh output
folder after correction. Record software version, database version and checksum, command,
input checksums, organism option, scope, and post-filter code. Database updates require a
new result release.

## Interpretation

AMRFinderPlus reports curated genotype evidence, not expression, clinical susceptibility,
MIC, host identity, or mobility. Link rows to MGE boundaries and hosts through
`$arg-mge-host-linkage`; sample-level co-detection is insufficient.

## Sources

- https://github.com/ncbi/amr/wiki
- https://doi.org/10.1038/s41598-021-91456-0

## Related skills

`resistome-analysis` · `rgi` · `resfinder` · `pointfinder` · `staramr` ·
`arg-mge-host-linkage` · `pathofact`
