---
name: tiara
description: >-
  Classify assembled contigs as eukaryotic, prokaryotic, organellar, or unknown with Tiara's deep-learning models. Use to triage metagenomic contigs before microbial-eukaryote binning while retaining probability, length, and unclassified evidence.
license: MIT
compatibility: Requires Tiara 1.0.3 in a compatible Python/PyTorch environment and nucleotide FASTA.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "tiara,eukaryote,contig-classification,mitochondria,plastid,deep-learning"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.0.3"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Tiara

Tiara assigns sequence-domain/organelle classes to nucleotide contigs in two stages. Upstream notes that default classification targets sequences at least 3 kb and does not recommend sequences shorter than 1 kb.

## Setup and input checks

Tiara 1.0.3 has an older Python/PyTorch compatibility envelope; isolate it in a pinned environment or container.

```bash
tiara-test
tiara --version || true
```

Use unique FASTA IDs. Keep the original assembly and a length table; do not silently discard sequences below the model's minimum.

## Run with probabilities and sequence splits

```bash
set -euo pipefail
fna=${1:?usage: tiara.sh contigs.fna output_dir}
out=${2:?usage: tiara.sh contigs.fna output_dir}
[[ -s "$fna" ]] || exit 2
mkdir -p "$out"
(
  cd "$out"
  tiara -i "$(realpath "$fna")" -o tiara.tsv --tf mit pla pro -t 8 \
    -p 0.65 0.60 --probabilities \
    >tiara.stdout.log 2>tiara.stderr.log
)
[[ -s "$out/tiara.tsv" && -s "$out/log_tiara.tsv" ]] || exit 3
```

The command requests mitochondrial, plastid, and prokaryotic FASTA partitions and writes class probabilities. Thresholds shown are the upstream advanced example; justify any study-specific thresholds.

## Validate

- confirm every eligible input ID has one result row and IDs are unique;
- summarize first-stage, second-stage, and final classes by count and total bases;
- stratify calls by contig length, coverage, GC, and probability;
- inspect disagreement with `$whokaryote`, gene homology, or bin context;
- keep `unknown` and short sequences visible rather than forcing classes.

Verify the generated partition FASTAs against the table and ensure their IDs/total length do not imply accidental duplication. Sequence split filenames are option/version dependent, so enumerate and checksum actual outputs.

## Recovery and provenance

Use a clean output directory after a failed `tiara-test` or model/environment change. Capture environment lock, Tiara version/commit, model parameters, command, input checksum, class table, and log summary.

## Analytical thinking

A high-probability eukaryotic label is a model prediction, not taxonomic identification or genome-bin validation. Organelle and horizontally transferred sequences can complicate context. Integrate coverage, genes, bin coherence, and `$eukcc` quality evidence.

## Source

- https://github.com/ibe-uw/tiara
