---
name: ppanggolin
description: >-
  Build partitioned prokaryotic pangenome graphs with PPanGGOLiN, including persistent/shell/cloud families, regions of genome plasticity, insertion spots, and modules. Use when graph partitioning and genome-plasticity analyses are needed from consistent GFF/GBFF or FASTA inputs.
license: MIT
compatibility: Requires PPanGGOLiN 2.3.2 and prokaryotic genomes/annotations; workflow dependencies and sufficient memory are required.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ppanggolin,pangenome,persistent,shell,cloud,genomic-plasticity"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.3.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# PPanGGOLiN

PPanGGOLiN stores a partitioned pangenome graph and analyses in an HDF5 file. Use taxonomically coherent, quality-gated genomes.

## Build the input list

For annotated input, create a tab-separated file with unique genome name and GFF3/GBFF path. Annotation files must contain sequence or be paired with a matching FASTA list.

```bash
set -euo pipefail
list=genomes.gbff.list
[[ -s "$list" ]] || exit 2
awk -F '\t' 'NF<2 || $1=="" || $2=="" {bad=1} END{exit bad}' "$list"
[[ $(cut -f1 "$list" | sort | uniq -d | wc -l) -eq 0 ]] || {
  echo "duplicate genome IDs" >&2; exit 2;
}
while IFS=$'\t' read -r id path rest; do [[ -s "$path" ]] || exit 2; done < "$list"
ppanggolin --version
```

Use one pinned annotation workflow and preserve a genome QC/ANI manifest.

## Complete workflow

```bash
out=ppanggolin_out
[[ ! -e "$out" ]] || { echo "use a fresh output directory" >&2; exit 2; }
ppanggolin all --anno "$list" --output "$out" --cpu 16 \
  --log "$out.log" --disable_prog_bar
[[ -s "$out/pangenome.h5" ]] || exit 3
ppanggolin info -p "$out/pangenome.h5" --parameters >"$out/parameters.txt"
ppanggolin info -p "$out/pangenome.h5" --content >"$out/content.txt"
ppanggolin write_pangenome -p "$out/pangenome.h5" -o "$out/tables" \
  --stats --Rtab --csv
```

FASTA-only input is supported with `ppanggolin all --fasta genomes.fasta.list`; record kingdom and translation table because PPanGGOLiN will annotate genes.

## Outputs and validation

The workflow HDF5 should contain annotation, gene families, graph, partition, RGPs, spots, and modules. Verify:

- all input genomes occur once;
- per-genome gene/family counts and persistent duplication expose no unexplained outliers;
- persistent/shell/cloud partition totals reconcile with all families;
- RGP, spot, and module outputs are non-empty only when supported, not required by assumption;
- `ppanggolin info --parameters` matches the intended command/configuration.

Generate MSA/phylogeny explicitly if needed:

```bash
ppanggolin msa -p ppanggolin_out/pangenome.h5 --partition persistent --phylo \
  -o ppanggolin_out/msa
```

## Recovery and provenance

The HDF5 file is stateful and later commands add content. Copy/checksum it before mutating analyses, and never combine incompatible runs with `--force`. Keep the input list, annotation checksums, environment, config/command, log, parameter dump, and HDF5 checksum.

## Analytical thinking

Persistent/shell/cloud are PPanGGOLiN model partitions, not universal core/accessory definitions. Sampling, assembly/annotation quality, paralogy, and MAG incompleteness affect them. RGPs and spots indicate genomic-plasticity patterns, not automatically horizontal transfer events or phenotypic effects.

## Source

- https://github.com/labgem/PPanGGOLiN
