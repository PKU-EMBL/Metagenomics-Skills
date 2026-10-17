---
name: sourmash
description: >-
  Sketch, compare, search, and decompose genomes, reads, and metagenomes with sourmash FracMinHash signatures. Use for lightweight sequence similarity, containment, contamination screening, database search, or gather-based metagenome composition when k-mer size and scaled parameters are compatible.
license: MIT
compatibility: Requires sourmash 4.9.x and FASTA/FASTQ or compatible signature/database files.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "sourmash,fracminhash,kmer,containment,gather,sketch"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "4.9.x"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# sourmash

sourmash uses MinHash/FracMinHash sketches for rapid similarity and containment. A sketch is a lossy summary; parameters define what can be compared.

## Input and parameter contract

Record molecule type, `k`, `scaled` (or `num`), abundance tracking, and database release. Query and database sketches must have compatible molecule type and k-mer size; sourmash can downsample compatible scaled sketches but cannot recover discarded hashes.

Typical DNA choices include k=31 for genome/metagenome comparisons and `scaled=1000` or a database-matched value. Choose parameters before cohort processing.

## Sketch paired reads as one sample

```bash
set -euo pipefail
r1=${1:?usage: sourmash-gather.sh R1.fastq.gz R2.fastq.gz database.zip sample}
r2=${2:?usage: sourmash-gather.sh R1.fastq.gz R2.fastq.gz database.zip sample}
db=${3:?usage: sourmash-gather.sh R1.fastq.gz R2.fastq.gz database.zip sample}
sample=${4:?usage: sourmash-gather.sh R1.fastq.gz R2.fastq.gz database.zip sample}
[[ -s "$r1" && -s "$r2" && -s "$db" ]] || exit 2
sourmash sketch dna -p k=31,scaled=1000,abund --merge "$sample" \
  -o "${sample}.sig.zip" "$r1" "$r2" \
  >"${sample}.sketch.stdout.log" 2>"${sample}.sketch.stderr.log"
sourmash sig describe "${sample}.sig.zip" >"${sample}.signature.txt"
sourmash gather "${sample}.sig.zip" "$db" -k 31 --threshold-bp 10000 \
  -o "${sample}.gather.csv" --save-matches "${sample}.matches.zip" \
  >"${sample}.gather.txt" 2>"${sample}.gather.stderr.log"
[[ -s "${sample}.gather.csv" ]] || exit 3
```

Use `abund` only when abundance-weighted gather estimates are wanted. For genome dereplication/similarity, abundance tracking is usually unnecessary.

## Other supported workflows

```bash
# Pairwise similarity matrix among compatible signatures
sourmash compare -k 31 --csv distances.csv genomes/*.sig.zip

# Best matches or query containment
sourmash search query.sig.zip database.sbt.zip -k 31 -n 20
sourmash search query.sig.zip database.sbt.zip -k 31 --containment -n 20

# Build a current RocksDB search index
sourmash index -F rocksdb refs.k31.rocksdb reference-signatures.zip
```

`search` returns independent matches; `gather` iteratively subtracts assigned hashes to produce a minimum metagenome cover. They answer different questions.

## Validation

- inspect `sourmash sig describe` for k, scaled, molecule, abundance, name, and hash count;
- verify gather CSV columns, non-empty query hashes, and fraction unexplained;
- compare signatures only under compatible parameters;
- include negative and known-mixture controls where detection claims matter;
- repeat low-level matches at lower `scaled` (higher resolution) if practical.

Large ANI estimates from tiny matched regions or low hash counts are unstable. `gather` can choose arbitrarily among near-identical references sharing the same hashes; do not interpret a selected genome as strain proof.

## Recovery and provenance

Keep original signatures, database checksum/release, complete stdout/stderr, `sourmash --version`, and command. A database filename is not a release record. If a run reports incompatible sketches, regenerate/downsample deliberately rather than bypassing checks.

## Analytical thinking

Containment is directional and differs from Jaccard similarity. Reference completeness bounds detection, and unassigned hashes are not automatically novel organisms. Treat gather abundance as a sketch-derived estimate, not an experimentally calibrated cell fraction.

## Source

- https://github.com/sourmash-bio/sourmash
