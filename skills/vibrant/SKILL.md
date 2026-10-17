---
name: vibrant
description: >-
  Identify and annotate viruses and proviruses in metagenomic assemblies with VIBRANT, including viral FASTA, GenBank, annotation, and auxiliary-metabolic-gene outputs. Use when VIBRANT-specific viral annotation is required, while cross-checking its older pinned dependency/database stack against current callers.
license: MIT
compatibility: Requires VIBRANT 1.2-era code, Python dependencies, HMMER, Prodigal, and its approximately 11 GB prepared databases.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "vibrant,viruses,provirus,amg,viral-annotation,virome"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.upstream-version: "upstream snapshot a718fba"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# VIBRANT

VIBRANT detects and annotates viral sequences, proviruses, and candidate auxiliary metabolic genes (AMGs). Its upstream stack pins older dependencies; prefer a container/locked environment and compare with actively maintained callers such as `$genomad` or `$virsorter2`.

## Setup gate

From the VIBRANT installation:

```bash
cd /opt/VIBRANT/databases
python3 VIBRANT_setup.py
python3 VIBRANT_setup.py -test
```

The setup uses substantial temporary/final storage. Archive the VIBRANT commit, database setup date/checksums, Python and HMMER versions, and test result. Do not accept a downloaded directory without the setup test.

## Inputs

Prefer nucleotide contigs with unique IDs. The upstream minimum is 1 kb and four ORFs; short fragments have limited evidence. Avoid the word `fragment` in source definition lines because VIBRANT uses that token for excised proviruses. Protein input must use expected Prodigal-style headers and ordering.

## Run

```bash
set -euo pipefail
contigs=${1:?usage: vibrant.sh contigs.fna output_parent}
out=${2:?usage: vibrant.sh contigs.fna output_parent}
[[ -s "$contigs" ]] || exit 2
mkdir -p "$out"
python3 /opt/VIBRANT/VIBRANT_run.py -i "$contigs" -folder "$out" -t 16 \
  >"$out/VIBRANT.stdout.log" 2>"$out/VIBRANT.stderr.log"
base=$(basename "$contigs")
base=${base%.*}
result="$out/VIBRANT_${base}"
[[ -d "$result" ]] || { echo "VIBRANT result directory missing" >&2; exit 3; }
find "$result" -type f -name '*.phages_combined.fna' -size +0c | grep -q . || {
  echo "no non-empty combined viral FASTA; inspect logs and no-hit possibility" >&2; exit 3;
}
```

Use `-virome` only when the input is genuinely virus-enriched and document it. `-l` changes minimum scaffold length; `-o` changes minimum ORFs. Neither should be tuned to obtain a preferred hit count.

## Outputs and verification

Key outputs include `VIBRANT_phages_<input>/<input>.phages_combined.fna`, `.txt`, and `.gbk`, plus result/annotation, HMM tables, figures, and run/annotation logs. Excised proviruses receive `_fragment_#` IDs; maintain a parent-coordinate map.

Verify sequence counts/lengths, no-hit runs, log completion, database/dependency tests, and agreement with another caller on a representative subset. Run `$checkv` independently on accepted viral sequences.

AMG labels require manual inspection of viral context, gene neighborhood, contamination, and metabolic plausibility. A metabolic annotation on a candidate viral contig is not sufficient evidence of an AMG.

## Recovery

VIBRANT may be quiet during normal execution. Diagnose with run and annotation logs, not stdout alone. Use a clean output parent after dependency or database repair to avoid mixing partial HMM tables.

## Analytical thinking

Caller disagreement is expected. Preserve scores/categories from all methods and define a reconciliation rule before ecological testing. VIBRANT prediction does not establish viral activity, host, or function.

## Source

- https://github.com/AnantharamanLab/VIBRANT
