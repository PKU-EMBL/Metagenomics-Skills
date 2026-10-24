---
name: dastool
description: >
  DAS Tool (Dereplication, Aggregation and Scoring) integrates multiple binning
  predictions into one non-redundant MAG set for a single assembly. Use this skill when
  working with DAS_Tool: preparing contig2bin tables, choosing score thresholds,
  comparing ensemble binning options, or writing Methods. For suite-style MetaBAT/MaxBin
  refinement use metawrap. For recommended multi-assembly refined recovery use basalt.
  For routing, use tool-selection.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MAG, ensemble-binning, DAS_Tool, refinement"
  metagenomics.upstream: "https://github.com/cmks/DAS_Tool"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "DAS Tool and conversion CLI checked against upstream usage; not executed here"
---

# DAS Tool

Upstream: [cmks/DAS_Tool](https://github.com/cmks/DAS_Tool)

## Citation

Sieber, C. M. K. *et al.* Recovery of genomes from metagenomes via a
dereplication, aggregation and scoring strategy. *Nat. Microbiol.* **3**,
836–843 (2018). https://doi.org/10.1038/s41564-018-0171-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

DAS Tool sits in the **ensemble binning** family with MetaWRAP and BASALT:
run several independent binners (MetaBAT2, MaxBin2, CONCOCT, …) on the **same
assembly**, then select an optimized non-redundant set.

DAS Tool scores candidates with **single-copy marker genes** and aggregates
across binning predictions. It does **not** invent new contig membership from
cross-assembly connectivity or deep learning — that is BASALT’s role.

Choose DAS Tool when you already have multiple contig2bin tables and want a
lightweight, classical consensus. Prefer **`basalt`** as the default ensemble
route for related samples / multi-assembly work; use **`metawrap`** when you
want a packaged binning + CheckM-style refinement suite.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Assembly FASTA + ≥2 contig2bin TSVs | MetaBAT2 + MaxBin2 (+ CONCOCT) |
| Search engine | DIAMOND / BLAST+ / USEARCH | DIAMOND (large datasets) |
| Threads | 1 | 8–16 |

## How to run

Use only predictions generated from the same immutable assembly and namespace.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-dastool.sh ASSEMBLY METABAT_BINS MAXBIN_BINS OUTPUT_DIR}"
metabat_bins="${2:?usage: run-dastool.sh ASSEMBLY METABAT_BINS MAXBIN_BINS OUTPUT_DIR}"
maxbin_bins="${3:?usage: run-dastool.sh ASSEMBLY METABAT_BINS MAXBIN_BINS OUTPUT_DIR}"
out="${4:?usage: run-dastool.sh ASSEMBLY METABAT_BINS MAXBIN_BINS OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$assembly" && test -d "$metabat_bins" && test -d "$maxbin_bins" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

Fasta_to_Contigs2Bin.sh -i "$metabat_bins" -e fa \
  >"$out/metabat.contigs2bin.tsv" 2>"$out/metabat.convert.stderr.log"
Fasta_to_Contigs2Bin.sh -i "$maxbin_bins" -e fasta \
  >"$out/maxbin.contigs2bin.tsv" 2>"$out/maxbin.convert.stderr.log"
test -s "$out/metabat.contigs2bin.tsv"
test -s "$out/maxbin.contigs2bin.tsv"

DAS_Tool \
  -i "$out/metabat.contigs2bin.tsv,$out/maxbin.contigs2bin.tsv" \
  -l metabat,maxbin -c "$assembly" -o "$out/run" -t "$threads" \
  --write_bins --write_bin_evals --search_engine diamond \
  >"$out/dastool.stdout.log" 2>"$out/dastool.stderr.log"
```

## Key parameters

| Parameter | Typical | Notes |
|-----------|---------|-------|
| `-i` | comma-separated contig2bin TSVs | Tab: contig_id\<TAB\>bin_id |
| `-l` | labels matching `-i` order | Human-readable binner names |
| `-c` | assembly FASTA | Same contigs used for binning |
| `--score_threshold` | 0.5 default | Higher → fewer, stricter bins |
| `--write_bins` | on for MAG export | Writes FASTA bins |
| `-p` | optional proteins | Skip Prodigal if reused |

## Output

```text
*_DASTool_summary.tsv
*_DASTool_contigs2bin.tsv
DASTool_bins/          # if --write_bins
*_allBins.eval         # if --write_bin_evals
```

## Decision tree

```text
Ensemble MAG recovery?
├─ Recommended default (related samples / multi-assembly) → basalt
├─ Packaged multi-binner + CheckM refinement suite → metawrap
└─ Classical SCG aggregation of existing contig2bin sets → dastool
```


## Literature notes (Nat. Microbiol. 2018)

Sieber *et al.* motivate DAS Tool with observations still true operationally:

- **No single binner wins on all ecosystems**; tools reconstruct different genomes
  at different completeness — combining predictions recovers more near-complete
  genomes than any single method.
- Early work showed manual/curated multi-binner merges help; naive automation can
  reduce contamination **and** completeness — DAS Tool’s SCG scoring aims for an
  optimized non-redundant set from one assembly.
- Input is **contig2bin tables on one assembly**, not cross-assembly DL refinement
  (contrast `basalt`).

Practical rule from the paper’s logic: diversify binners (MetaBAT2 + MaxBin2 +
CONCOCT/SemiBin2/VAMB/COMEBin), then aggregate — do not run DAS Tool on a
single contig2bin table expecting magic.

## Validation, recovery, and provenance

Require non-empty summary, final contig2bin map, bin-evaluation table, and FASTA
bin directory. Verify every assigned contig exists exactly once in the source
assembly, input labels match table order, and duplicate contig assignments within
an input set are resolved before running. Reassess exported bins with `checkm2`
and `gunc`; SCG score is selection evidence, not a publication-quality metric.

Use `--resume` only with the exact prior proteins, inputs, database, and release.
Otherwise keep the old prefix and start a new one. Archive DAS Tool/dependency
versions, SCG database/search-engine version, assembly and table checksums,
commands, logs, score parameters, input evaluations, selected-bin lineage, and
final checksums.

## Related skills

`metawrap` · `basalt` · `megahit` · `metaspades` · `checkm2` · `gunc` · `drep` ·
`mag-qc` · `tool-selection`
