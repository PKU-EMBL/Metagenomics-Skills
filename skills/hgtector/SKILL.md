---
name: hgtector
description: >-
  Detect putative horizontally acquired genes from genome or MAG proteomes with HGTector2
  using taxonomically partitioned homology-hit distributions. Use for database building,
  search/analyze execution, self/close/distal group review, donor hypotheses, and sensitivity
  analysis without treating statistical outliers as observed transfer events.
license: MIT
compatibility: Requires HGTector2 2.0b3, Python 3, DIAMOND, a pinned reference sequence/taxonomy database, and one protein FASTA per genome.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "HGTector,HGT,homology,taxonomy,outlier,donor"
  metagenomics.upstream: "https://github.com/qiyunlab/HGTector"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0b3 commit ea9fa7222fb3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/database/output contract reviewed; not executed here"
---

# HGTector2

HGTector scores each protein by homology hits in self, close, and distal taxonomic groups,
then identifies outliers as putative horizontally acquired genes. Results depend strongly
on taxonomy, reference sampling, and group definitions.

## Input contract

- one whole-proteome FASTA per isolate/genome/MAG, with unique sample/protein IDs;
- quality and contamination flags for partial MAGs;
- pinned sequence database plus NCBI taxonomy dump;
- explicit input taxon IDs where auto-inference is unreliable;
- predeclared self/close groups or a documented auto-inference policy.

Build a database with `hgtector database -o db_dir --default` only as a controlled setup
step; archive its date, source accessions, taxonomy dump, and checksums.

## Search and analyze

```bash
set -euo pipefail
proteomes=${PROTEOMES:?set PROTEOMES to a file or directory of FAA files}
db=${HGTECTOR_DB:?set HGTECTOR_DB}
out=${OUTDIR:-results/hgtector}
[[ -e "$proteomes" && -s "$db/diamond/db.dmnd" && \
   -s "$db/taxdump/nodes.dmp" && -s "$db/taxdump/names.dmp" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
hgtector search -i "$proteomes" -o "$out/search" -m diamond -p 16 \
  -d "$db/diamond/db" -t "$db/taxdump" \
  >"$out/search.stdout.log" 2>"$out/search.stderr.log"
hgtector analyze -i "$out/search" -o "$out/analyze" -t "$db/taxdump" \
  >"$out/analyze.stdout.log" 2>"$out/analyze.stderr.log"
[[ -s "$out/analyze/scores.tsv" ]] || exit 3
awk -F '\t' 'NR==1 {for (i=1;i<=NF;i++) if ($i=="hgt") found=1; exit !found}' \
  "$out/analyze/scores.tsv"
```

For production, provide `--input-tax`, `--self-tax`, and `--close-tax` or document why
auto-inference is trustworthy. Sensitivity-test KDE/bandwidth, filtering, and donor-rank
settings rather than tuning to desired candidates.

## Validation

- account for every input proteome and protein in search/no-hit/score states; a missing
  `hgts/` directory is a valid no-candidate state when `scores.tsv` and logs confirm zero;
- inspect self/close/distal scores, silhouette score, hit count, best distal match, and
  inferred group taxonomy;
- review reference density across candidate donor groups;
- screen candidates for contamination, conserved domains, paralogy, and truncated genes;
- compare high-priority calls with gene trees, synteny/MGE context, and `$metachip`;
- retain failures of KDE clustering and any fixed-threshold fallback.

## Recovery and provenance

`analyze` may be rerun from an unchanged search directory. Database, taxonomy, proteome,
or search-filter changes require new search and analysis directories. Record HGTector,
DIAMOND, database build/accessions/checksums, taxdump date, group definitions, all
parameters, input checksums, and result filters.

## Interpretation

The reported donor is an LCA/best match among distal database hits, not a demonstrated
physical donor. Homology-distribution outliers support putative historical acquisition;
they do not date the event, identify a vehicle, or show ongoing transfer.

## Source

- https://github.com/qiyunlab/HGTector
- https://doi.org/10.1186/1471-2164-15-717

## Related skills

`horizontal-gene-transfer` · `metachip` · `waafle` · `iqtree` ·
`mobilome-analysis` · `arg-mge-host-linkage`
