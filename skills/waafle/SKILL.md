---
name: waafle
description: >-
  Find candidate lateral gene-transfer events on assembled metagenomic contigs with WAAFLE
  by combining nucleotide homology, gene order, taxonomic mosaics, and read-supported
  junction QC. Use for fragmentary multi-gene contigs when database/taxonomy formatting,
  misassembly filters, and inferred direction must be audited.
license: MIT
compatibility: Requires WAAFLE 1.5.0, BLAST+, Bowtie2 for junction QC, contigs of roughly 1–20 kb, a WAAFLE nucleotide database, and matching taxonomy.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "WAAFLE,LGT,HGT,metagenome,contig,junction-QC"
  metagenomics.upstream: "https://github.com/biobakery/waafle"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.5.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/database/output contract reviewed; not executed here"
---

# WAAFLE

WAAFLE identifies taxonomic mosaics across neighboring genes on metagenomic contigs. It is
optimized for fragmentary contigs spanning a few to tens of genes, not closed genomes or
hundreds-of-kilobase scaffolds.

## Inputs

- assembled nucleotide contigs with unique BLAST-compatible IDs;
- WAAFLE-formatted nucleotide gene database and matching child-parent taxonomy;
- optional GFF from a consistent gene caller, otherwise WAAFLE gene calling;
- original paired reads for junction support;
- database release/checksum and taxonomic level used for reference genes.

The current upstream ChocoPhlAn WAAFLE database is large; preserve its exact
`v202210_202403`-style release rather than referring to “latest.”

## Search, score, and junction QC

Run in a new staging directory so WAAFLE’s derived filenames remain isolated.

```bash
set -euo pipefail
contigs=${CONTIGS:?set CONTIGS}
db=${WAAFLE_DB:?set WAAFLE_DB prefix}
tax=${WAAFLE_TAXONOMY:?set WAAFLE_TAXONOMY}
r1=${READ1:?set READ1}
r2=${READ2:?set READ2}
out=${OUTDIR:-results/waafle}
[[ -s "$contigs" && -s "$tax" && -s "$r1" && -s "$r2" ]] || exit 2
[[ -e "$db" || -e "${db}.nin" || -e "${db}.ndb" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
cp "$contigs" "$out/contigs.fna"
{
  waafle_search "$out/contigs.fna" "$db" --threads 16 \
    --out "$out/contigs.blastout"
  waafle_genecaller "$out/contigs.blastout" --gff "$out/contigs.gff"
  waafle_orgscorer "$out/contigs.fna" "$out/contigs.blastout" \
    "$out/contigs.gff" "$tax" --outdir "$out" --basename contigs
  waafle_junctions "$out/contigs.fna" "$out/contigs.gff" \
    --reads1 "$r1" --reads2 "$r2" --tmpdir "$out/tmp" \
    --outdir "$out" --basename contigs
  waafle_qc "$out/contigs.lgt.tsv" "$out/contigs.junctions.tsv"
} >"$out/waafle.stdout.log" 2>"$out/waafle.stderr.log"
[[ -s "$out/contigs.lgt.tsv" && -s "$out/contigs.no_lgt.tsv" && \
   -s "$out/contigs.unclassified.tsv" && -s "$out/contigs.junctions.tsv" && \
   -e "$out/contigs.lgt.tsv.qc_pass" ]] || exit 3
```

A zero-row `qc_pass` file is a valid result if the header/file exists. BLAST index suffixes
vary; the preflight accepts a database path or a `.nin`/`.ndb` marker, but archive
`blastdbcmd -info -db "$db"` as the stronger production check.

## Validation

- reconcile all contigs among LGT, no-LGT, and unclassified outputs;
- inspect clades A/B, synteny, score, LCA, direction, and gene coordinates;
- require read support around the inferred LGT junctions and examine local coverage;
- compare candidates against assembly-graph ambiguities and independent assemblies;
- test stringent junction-hit/coverage-ratio settings and contig length strata;
- retain all failed-QC candidates with explicit reasons.

Direction is inferred from gene order and flanking clade assignments. It can remain `A?B`
and does not identify an unsampled donor.

## Recovery and provenance

The BLAST search is rate-limiting and may be reused only for the identical contig FASTA,
database, BLAST version, and search options. Use a new output directory after changing
gene calls, taxonomy, database, or QC thresholds. Record WAAFLE/BLAST/Bowtie2 versions,
database/taxonomy checksums, assembly and read checksums, commands, and filters.

## Interpretation

A passing mosaic contig is a candidate LGT event, not directly observed transfer. Chimeric
assembly, conserved genes, missing reference taxa, and gene loss remain alternatives.

## Source

- https://github.com/biobakery/waafle
- https://doi.org/10.1038/s41564-024-01881-w

## Related skills

`horizontal-gene-transfer` · `metachip` · `hgtector` · `megahit` · `bowtie2` ·
`arg-mge-host-linkage` · `transfer-network-analysis`
