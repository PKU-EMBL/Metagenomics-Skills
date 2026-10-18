---
name: plasx
description: >-
  Classify metagenomic contigs as plasmid-like with PlasX using COG14, Pfam 32, and
  de novo gene-family architecture. Use when preparing compatible anvi'o annotations,
  running the pinned model, choosing score thresholds, or comparing plasmid calls while
  retaining contig-level uncertainty and training-domain limits.
license: MIT
compatibility: Requires Linux, Python 3.7+, anvi'o-compatible COG14/Pfam 32 annotations, MMseqs2 10.6d92c, the PlasX model assets, and substantial RAM.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PlasX,plasmid,metagenome,classifier,gene-architecture"
  metagenomics.upstream: "https://github.com/michaelkyu/PlasX"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "commit 5c9acfd00a59"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI/model contract reviewed against upstream; not executed here"
---

# PlasX

PlasX predicts plasmid-like contigs from gene architecture. It requires the annotation
versions used for training: COG 2014, Pfam 32, and its de novo family model. Current anvi'o
default databases are not interchangeable.

## Input contract

For one unchanged contig FASTA, prepare:

- anvi'o/Prodigal gene calls exported as `gene-calls.txt`;
- COG14 and Pfam 32 function export as `cogs-and-pfams.txt`;
- globally unique contig and gene IDs;
- PlasX model files from Zenodo record 5819401 with checksums;
- MMseqs2 10.6d92c and a declared number of database splits.

The de novo family search can require about 60 GB RAM without splitting. Increase
`--splits` under limited memory and record it.

## Model setup and prediction

Run `plasx setup` once in a frozen environment with the upstream Zenodo URLs, then archive
checksums of the downloaded family profiles and coefficients. Given compatible annotation
files:

```bash
set -euo pipefail
prefix=${PREFIX:?set PREFIX to an output prefix}
genes=${GENE_CALLS:?set GENE_CALLS}
functions=${COG_PFAM:?set COG_PFAM}
out=${OUTDIR:-results/plasx}
[[ -s "$genes" && -s "$functions" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
plasx search_de_novo_families -g "$genes" \
  -o "$out/${prefix}-de-novo-families.txt" --threads 16 --splits 32 --overwrite \
  >"$out/search.stdout.log" 2>"$out/search.stderr.log"
plasx predict -a "$functions" "$out/${prefix}-de-novo-families.txt" \
  -g "$genes" -o "$out/${prefix}-scores.txt" --overwrite \
  >"$out/predict.stdout.log" 2>"$out/predict.stderr.log"
[[ -s "$out/${prefix}-scores.txt" ]] || exit 3
awk -F '\t' 'NR==1 {exit !($1=="contig" && $2=="score")}' \
  "$out/${prefix}-scores.txt"
```

Upstream suggests scores above 0.5 for candidate plasmids and higher thresholds such as
0.9 for stricter sets. These are starting points, not universal truth; predeclare and
sensitivity-test the cutoff by contig length and study domain.

## Validation

- every input contig should have one score unless an exclusion is explained;
- verify gene IDs agree across both annotation tables and gene calls;
- audit COG/Pfam/model versions and model checksums;
- compare calls with `$genomad`, `$mob-suite`, circularity, and mobility genes;
- inspect chromosome/plasmid conflicts and short or repeat-rich contigs;
- retain all scores, not only thresholded positives.

## Recovery and provenance

Model/setup changes or incompatible annotation versions require a fresh environment and
output directory. Record PlasX commit, MMseqs2/anvi'o/Prodigal versions, COG/Pfam releases,
model URLs/checksums, split count, command, input checksums, and cutoff.

## Interpretation

A high score supports plasmid-like genetic architecture. It does not prove a complete,
circular, autonomous, conjugative, host-assigned, or actively transferring plasmid. Use
`$mobmess` for plasmid systems and `$arg-mge-host-linkage` for cargo/host evidence.

## Source

- https://github.com/michaelkyu/PlasX
- https://doi.org/10.1038/s41564-024-01610-3

## Related skills

`mobilome-analysis` · `genomad` · `mob-suite` · `mobmess` · `anvio` ·
`arg-mge-host-linkage` · `rgi`
