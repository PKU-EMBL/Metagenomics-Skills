---
name: whokaryote
description: >-
  Classify metagenomic contigs as eukaryotic or prokaryotic with Whokaryote using gene-density, intergenic, and optional Tiara-integrated features. Use for long-contig microbial-eukaryote triage when contigs, gene predictions, minimum-length limits, and unclassified sequences are tracked explicitly.
license: MIT
compatibility: Requires Whokaryote 1.1.2, Python environment, Tiara for model T, and Prodigal or compatible GFF/gene coordinates.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "whokaryote,eukaryote,prokaryote,contigs,classification,tiara"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.1.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Whokaryote

Whokaryote classifies sufficiently long, gene-containing contigs as eukaryotic or prokaryotic. Model `T` integrates Tiara and is the upstream-recommended default; model `S` is standalone.

## Input contract

- nucleotide multi-FASTA with unique contig IDs;
- optionally a matching gene-prediction GFF (`--gff`) to avoid recomputation;
- chosen model and minimum length (default 5 kb);
- enough disk for intermediate FASTA/features.

Contigs shorter than the minimum or with fewer than two predicted genes are not classified and must remain in an explicit unclassified ledger.

## Run

```bash
set -euo pipefail
contigs=${1:?usage: whokaryote.sh contigs.fasta output_dir}
out=${2:?usage: whokaryote.sh contigs.fasta output_dir}
[[ -s "$contigs" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a fresh output directory" >&2; exit 2; }
whokaryote.py --contigs "$contigs" --outdir "$out" --model T \
  --minsize 5000 --threads 8 --f \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
find "$out" -name 'whokaryote_predictions_*.tsv' -size +0c | grep -q . || exit 3
```

If consistent gene calls already exist, add `--gff predictions.gff`; verify the GFF sequence IDs exactly match the FASTA. The older hidden `--prodigal_file` option appears in some examples, but use the documented `--gff` interface for new workflows.

## Outputs and validation

Expect eukaryote/prokaryote header lists, length-filtered contigs, gene coordinates/features, Tiara predictions for model T, detailed feature/prediction tables, and `whokaryote_predictions_<model>.tsv`. With `--f`, expect class-specific FASTAs.

Verify:

- classified, below-length, low-gene-count, and otherwise unclassified IDs reconcile to input IDs;
- split FASTA IDs agree with the prediction table;
- class composition is examined by length, coverage, GC, and gene count;
- model T and `$tiara` evidence are not treated as independent votes;
- suspicious contigs are checked in bin and gene-homology context.

## Recovery and provenance

Partial directories can contain stale feature tables; rerun into a clean path after failure. Capture version/commit, Python environment, Tiara/Prodigal versions, model, minimum length, command, logs, and input/output checksums.

## Analytical thinking

Long-contig selection creates a strong detectability bias. A eukaryotic prediction does not establish taxonomy or genome membership, while an unclassified short contig is not prokaryotic. Integrate with coverage/binning and `$eukcc` rather than deleting discordant sequences automatically.

## Source

- https://github.com/LottePronk/whokaryote
