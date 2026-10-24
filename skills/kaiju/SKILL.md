---
name: kaiju
description: >
  Fast sensitive taxonomic classification via protein-level matches. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, protein, classification"
  metagenomics.upstream: "https://github.com/bioinformatics-centre/kaiju"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired-end kaiju and kaiju2table CLI checked against upstream usage; not executed here"
---

# Kaiju

Upstream: [Kaiju](https://github.com/bioinformatics-centre/kaiju)

## Citation

Menzel, P., Ng, K. L. & Krogh, A. Fast and sensitive taxonomic classification for metagenomics with Kaiju. *Nat. Commun.* **7**, 11257 (2016). https://doi.org/10.1038/ncomms11257

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Kaiju classifies reads by **six-frame translated** matches against a protein DB
(LCA of hits). Strength: remote homology / understudied clades where DNA k-mers
fail. Weakness: weaker close-species separation than good DNA classifiers.

| Tool | Signal | Prefer when |
|------|--------|-------------|
| `kaiju` | AA / protein | Novel / divergent lineages |
| `kraken2` | DNA k-mers | Speed, custom DNA DBs |
| `metabuli` | Joint DNA+AA | Want both sensitivity and specificity |
| `metaphlan` / `singlem` | Markers | Clade/SGB or unknown-species marker profiles |

Database choice dominates results. Do not merge Kaiju tables with MetaPhlAn
unlabeled.

## How to run

```bash
set -Eeuo pipefail
id="${1:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
db="${2:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
nodes="${3:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
names="${4:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
r1="${5:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
r2="${6:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
out="${7:?usage: classify-kaiju.sh SAMPLE_ID DB_FMI NODES NAMES R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$db" "$nodes" "$names" "$r1" "$r2"; do test -s "$input" || exit 2; done
gzip -t "$r1" "$r2"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

kaiju -t "$nodes" -f "$db" -i "$r1" -j "$r2" -z "$threads" \
  -o "$out/${id}.kaiju.out" \
  >"$out/${id}.kaiju.stdout.log" 2>"$out/${id}.kaiju.stderr.log"
kaiju2table -t "$nodes" -n "$names" -r species \
  -o "$out/${id}.species.tsv" "$out/${id}.kaiju.out" \
  >"$out/${id}.table.stdout.log" 2>"$out/${id}.table.stderr.log"
```

## Key parameters

| Item | Notes |
|------|-------|
| DB | RefSeq / nr / proGenomes-derived builds — pin release |
| `-z` | Threads |
| `-a` / greedy modes | Predeclare the mode and record its sensitivity/speed settings |
| Rank in `kaiju2table` | Species/genus — state in Methods |

## Decision tree

```text
Protein-aware read taxonomy?
├─ Yes, AA sensitivity primary → kaiju
├─ Joint DNA+AA → metabuli
├─ Marker composition → metaphlan / singlem
└─ Fast DNA k-mer → kraken2 (+ bracken)
```

## Methods caveats

- Hits depend on protein DB completeness; unclassified ≠ empty community
- Pin Kaiju + NCBI taxonomy dump versions used to build the DB

## Validation, recovery, and provenance

Require one Kaiju record per read or read pair and reconcile classified plus
unclassified counts to input pairs. Check paired-name mismatch errors, mode
(greedy/MEM), SEG policy, score/E-value thresholds, rank aggregation, controls,
and taxonomy IDs absent from the pinned dump. Retain raw assignments before
`kaiju2table` filtering.

Use fresh outputs after changing database, taxonomy, mode, or thresholds. Record
Kaiju version, database recipe/source/release/checksum, NCBI taxonomy date and
checksums, read checksums, command, logs, raw/table checksums, and summary rules.
Protein matches are reference-conditioned taxonomic evidence, not phenotype or
absolute abundance.

## Related skills

`metabuli` · `kraken2` · `diamond` · `metaphlan` · `singlem` · `tool-selection`
