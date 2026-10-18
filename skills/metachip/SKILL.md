---
name: metachip
description: >-
  Detect candidate horizontal gene transfers among community genomes or MAGs with
  MetaCHIP2 using best-match and phylogenetic reconciliation. Use when preparing GenBank
  inputs, taxonomy groups, a rooted species tree, multi-rank detection, inferred gene-flow
  summaries, or donor-direction interpretation with unsampled-donor caveats.
license: MIT
compatibility: Requires MetaCHIP2 2.3.25, annotated GenBank genomes, matching taxonomy/grouping, a rooted species tree, Ranger-DTL2, BLAST or MMseqs2, MAFFT, and FastTree.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MetaCHIP2,HGT,LGT,phylogeny,gene-flow,MAG"
  metagenomics.upstream: "https://github.com/songweizhi/MetaCHIP2"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.3.25"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/output contract reviewed against upstream; not executed here"
---

# MetaCHIP2

MetaCHIP2 combines best-match evidence with gene/species phylogenetic reconciliation to
identify candidate HGTs among the supplied genomes. Its donor is the closest sampled gene
in an inferred donor **group**, not necessarily the organism that physically transferred
the gene.

## Input contract

- one consistently annotated GenBank file per genome/MAG; file stem matches all metadata;
- short contig IDs compatible with the annotation workflow;
- CheckM2/GUNC quality flags and explicit exclusion policy;
- two-column GTDB taxonomy or custom grouping file;
- rooted species tree with the same genome tips;
- predeclared taxonomic ranks and BLAST-versus-MMseqs2 search mode.

Use `MetaCHIP2 prokka` for batch annotation only when Prokka is scientifically suitable,
and `MetaCHIP2 tree` when its GTDB-Tk workflow and database release are pinned.

## Detect candidate transfers

```bash
set -euo pipefail
gbk=${GBK_DIR:?set GBK_DIR}
groups=${GROUPS:?set GROUPS to taxonomy/grouping TSV}
tree=${ROOTED_TREE:?set ROOTED_TREE}
out=${OUTDIR:-results/metachip2}
[[ -d "$gbk" && -s "$groups" && -s "$tree" ]] || exit 2
for path in "$out" "${out}.stdout.log" "${out}.stderr.log"; do
  [[ ! -e "$path" ]] || { echo "refusing to overwrite: $path" >&2; exit 2; }
done
mkdir -p "$(dirname "$out")"
MetaCHIP2 detect -i "$gbk" -x gbk -c "$groups" -s "$tree" \
  -t 16 -f -o "$out" -r pcofg -m \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
hits=$(find "$out" -type f -name 'detected_HGTs.txt' -print -quit)
[[ -n "$hits" && -s "$hits" ]] || exit 3
awk -F '\t' 'NR==1 {if (NF < 5) exit 1}' "$hits"
```

`-m` selects MMseqs2/Linclust acceleration. Remove it only when deliberately using the
all-versus-all BLASTN path. `-r pcofg` analyzes phylum through genus; choose ranks before
examining results and ensure enough genomes per group.

## Validate outputs

Inspect `detected_HGTs.txt`, sequence FASTAs, flanking-region plots, grouping files, and
gene-flow visualization. For every event:

- confirm both genes/genomes and tree tips exist and taxonomy is correct;
- inspect identity, full-length/end-match flags, flanks, gene-tree support, and rank recurrence;
- map reads across relevant assembly junctions and screen both genomes for contamination;
- collapse one ancestral event observed in descendants when appropriate;
- retain candidate events with uncertain or conflicting direction.

Subset functional categories only after the full event set is frozen. A Circos band width
counts detected events under this pipeline; it is not a transfer rate.

## Recovery and provenance

All-vs-all search results may be supplied with `-b` only for the identical genome set,
annotation, search software, and parameters. Otherwise start a new directory. Record
MetaCHIP2, GTDB-Tk/database, Ranger-DTL, MMseqs2/BLAST, MAFFT/FastTree versions, rooted
tree, grouping file, commands, input checksums, and filters.

## Interpretation

Report “MetaCHIP2 candidate HGT” and “putative donor/recipient group.” Low identity can
reflect an unsampled true donor; high identity can reflect contamination or conserved
sequence. Direction and timing remain model-dependent and do not demonstrate active
transfer.

## Source

- https://github.com/songweizhi/MetaCHIP2
- https://doi.org/10.1186/s40168-019-0649-y

## Related skills

`horizontal-gene-transfer` · `hgtector` · `waafle` · `gubbins` · `gtdbtk` ·
`checkm2` · `gunc` · `transfer-network-analysis`
