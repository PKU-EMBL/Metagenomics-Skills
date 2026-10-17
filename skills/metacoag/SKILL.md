---
name: metacoag
description: >-
  Bin metagenomic contigs with MetaCoAG using composition, multi-sample abundance, single-copy markers, and assembler graph connectivity. Use when a compatible metaSPAdes, MEGAHIT, Flye, or custom GFA graph and matching contigs/path files are available.
license: MIT
compatibility: Requires MetaCoAG 1.3.0, GFA assembly graph, matching contigs, headerless abundance TSV, FragGeneScan, HMMER, and assembler-specific path metadata where required.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "metacoag,binning,assembly-graph,coverage,marker-genes,gfa"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.3.0"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# MetaCoAG

MetaCoAG integrates assembly-graph connectivity, composition, abundance, and single-copy markers. Inputs must originate from the same assembly with unchanged contig IDs.

## Input contract

- metaSPAdes: GFA graph, contigs FASTA, `contigs.paths`, headerless abundance TSV;
- MEGAHIT: matching GFA graph, contigs FASTA, headerless abundance TSV;
- Flye: `assembly_graph.gfa`, `assembly.fasta`, `assembly_info.txt`, abundance TSV (support is less extensively tested upstream);
- custom: inspect current `--help` requirements.

The abundance file has one contig per row followed by coverage columns and **no header**. Generate consistently with `$coverm` and verify contig IDs against FASTA/GFA.

## Preflight

```bash
set -euo pipefail
contigs=final.contigs.fa
graph=final.gfa
abund=abundance.tsv
[[ -s "$contigs" && -s "$graph" && -s "$abund" ]] || exit 2
metacoag --version
python3 - "$contigs" "$abund" <<'PY'
import sys
ids={x[1:].split()[0] for x in open(sys.argv[1]) if x.startswith(">")}
rows=[x.rstrip("\n").split("\t") for x in open(sys.argv[2]) if x.strip()]
assert ids and rows and all(len(r)>=2 for r in rows)
assert rows[0][0] in ids, "abundance may have a header or mismatched contig IDs"
missing=[r[0] for r in rows if r[0] not in ids]
assert not missing, f"unknown abundance contigs: {missing[:10]}"
assert len({r[0] for r in rows})==len(rows), "duplicate abundance contigs"
print("fasta_contigs",len(ids),"abundance_rows",len(rows))
PY
```

Also compare GFA segment IDs and assembler k/graph provenance; FASTG-to-GFA conversion must use the final MEGAHIT k value.

## Run MEGAHIT example

```bash
out=metacoag_out
[[ ! -e "$out" ]] || { echo "use a fresh output directory" >&2; exit 2; }
metacoag --assembler megahit --graph "$graph" --contigs "$contigs" \
  --abundance "$abund" --output "$out" --nthreads 16 \
  >metacoag.stdout.log 2>metacoag.stderr.log
[[ -s "$out/contig_to_bin.tsv" && -d "$out/bins" ]] || exit 3
find "$out/bins" -type f -size +0c | grep -q . || {
  echo "no non-empty bins; inspect low-quality bins and logs" >&2; exit 3;
}
```

For metaSPAdes/Flye add `--paths` with the matching path/info file.

## Validate

- every assigned contig exists in the FASTA and appears in at most one final bin;
- bin FASTA membership agrees with `contig_to_bin.tsv`;
- inspect `bins` and `low_quality_bins` separately;
- assess all bins with `$checkm2`, `$gunc`, taxonomy, size, N50, and coverage coherence;
- compare with composition/coverage-only binners and refine/ensemble rather than accepting graph labels uncritically.

## Recovery and provenance

Version 1.3.0 supports `--continue` from its checkpoint after interruption when inputs and result-affecting options are unchanged; only threads may change. Otherwise use a new output directory. Preserve graph/contig/path/abundance checksums, assembler version/parameters, MetaCoAG command/logs, marker outputs, and quality assessments.

## Analytical thinking

Assembly graph edges can connect repeats, strains, plasmids, and chimeras; connectivity is evidence, not organism identity. Marker-based bin quality within MetaCoAG is only an internal gate. Independent quality/taxonomy and read-coverage validation remain required.

## Source

- https://github.com/metagentools/MetaCoAG
