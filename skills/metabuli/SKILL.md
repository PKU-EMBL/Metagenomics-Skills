---
name: metabuli
description: >
  Metabuli — metagenomic taxonomic classification via joint DNA + amino-acid (metamer)
  analysis for sensitive homology and specific close-taxon resolution. Use when: (1)
  Choosing a classifier beyond DNA-only (Kraken2) or AA-only (Kaiju), (2) Profiling
  understudied clades where DNA k-mers fail, (3) CAMI- style or plant/environment
  datasets needing both sensitivity and specificity, (4) Writing Methods for joint
  DNA/AA classification. Complementary to metaphlan / kraken2 / kaiju — do not merge
  tables unlabeled.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, Metabuli, DNA, amino-acid, classification"
  metagenomics.upstream: "https://github.com/steineggerlab/Metabuli"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "1.2 interface"
  metagenomics.command-status: "paired-end classify argument order checked against current documentation; not executed here"
---

# Metabuli

Upstream: [steineggerlab/Metabuli](https://github.com/steineggerlab/Metabuli) ·
https://metabuli.steineggerlab.com

## Citation

Kim, J. & Steinegger, M. Metabuli: sensitive and specific metagenomic
classification via joint analysis of amino acid and DNA. *Nat. Methods* **21**,
971–973 (2024). https://doi.org/10.1038/s41592-024-02273-y

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classical dilemma:

| Signal | Strength | Weakness |
|--------|----------|----------|
| DNA k-mers (Kraken-like) | Distinguishes close, well-studied taxa | Misses remote homology |
| AA / 6-frame (Kaiju-like) | Sensitive to understudied clades | Weaker close-species separation |

Metabuli jointly analyzes DNA and AA via **metamers**, aiming to keep both
sensitivity and specificity. In CAMI2 plant-associated benchmarks it recovered
nearly all classifications of strong DNA- and AA-only tools.

Still database-bound: unclassified reads ≠ empty community. Prefer MetaPhlAn
when you need **clade-specific marker** abundances for pathways (HUMAnN); prefer
Metabuli/Kraken/Kaiju when you need read-level classification against large
nucleotide/protein DBs.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| DB | Metabuli database matching software version |
| RAM / disk | Large DBs — plan like Kraken-scale resources |
| Input | Preferably host-depleted FASTQ |

## How to run

Metabuli 1.2 orders positional arguments as input read(s), database directory,
output directory, then job ID.

```bash
set -Eeuo pipefail
id="${1:?usage: classify-metabuli.sh SAMPLE_ID DB_DIR R1 R2 OUTPUT_DIR}"
db="${2:?usage: classify-metabuli.sh SAMPLE_ID DB_DIR R1 R2 OUTPUT_DIR}"
r1="${3:?usage: classify-metabuli.sh SAMPLE_ID DB_DIR R1 R2 OUTPUT_DIR}"
r2="${4:?usage: classify-metabuli.sh SAMPLE_ID DB_DIR R1 R2 OUTPUT_DIR}"
out="${5:?usage: classify-metabuli.sh SAMPLE_ID DB_DIR R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
max_ram="${MAX_RAM_GB:-64}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
test -d "$db" || exit 2
for input in "$r1" "$r2"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

metabuli classify "$r1" "$r2" "$db" "$out/results" "$id" \
  --threads "$threads" --max-ram "$max_ram" \
  >"$out/${id}.metabuli.stdout.log" 2>"$out/${id}.metabuli.stderr.log"
find "$out/results" -type f -size +0c -print -quit | grep -q .
```

## Decision tree

```text
Taxonomic classification goal?
├─ Marker-gene relative abundance → metaphlan / motus
├─ Fast DNA k-mer + Bracken abundance → kraken2 + bracken
├─ Protein-level sensitivity → kaiju
├─ Joint DNA+AA (sensitivity + specificity) → metabuli
└─ Sketch containment / ANI-aware presence → sylph
```

## Methods caveats

- Do not average Metabuli with MetaPhlAn/Kraken without labeling method.
- Pin Metabuli + DB release; report paired-end mode and filters.
- Species labels for novel lineages remain reference-dependent.

## Validation, recovery, and provenance

Reconcile classified plus unclassified reads to the input accounting reported by
the run, inspect rank distributions, close-species ambiguity, score/E-value
filters, controls, and any refined abundance output separately from raw read
assignments. Confirm paired reads remained synchronized. Do not equate a read
classification with organism viability or merge results from different database
releases unlabeled.

Use a fresh output after changing database, sequence mode, RAM strategy, or
thresholds. Record Metabuli version, database/taxonomy release and checksum,
read checksums, paired/single/long-read mode, commands, logs, output schema,
filtering/refinement steps, and result checksums.

## Related skills

`kraken2` · `bracken` · `kaiju` · `metaphlan` · `sylph` · `motus` ·
`tool-selection` · `metagenomics-workflow`
