---
name: lexicmap
description: >
  LexicMap — efficient nucleotide alignment of moderate-length queries (genes, plasmids,
  long reads; typically >250 bp) against up to millions of prokaryotic genomes. Use
  when: (1) Searching genes/plasmids vs huge genome databases, (2) Scaling beyond
  BLAST/minimap2 for AllTheBacteria / GTDB-scale refs, (3) Epidemiology/ecology queries
  needing fast genome hits. Not a substitute for short-read→contig coverage mappers
  (strobealign/bowtie2) used in binning.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "alignment, search, LexicMap, genomes, BLAST"
  metagenomics.upstream: "https://github.com/shenwei356/LexicMap"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "index/search CLI checked against current upstream quick start; not executed here"
---

# LexicMap

Upstream: [shenwei356/LexicMap](https://github.com/shenwei356/LexicMap)

## Citation

Shen, W., Lees, J. A. & Iqbal, Z. Efficient sequence alignment against millions
of prokaryotic genomes with LexicMap. *Nat. Biotechnol.* (2025).
https://doi.org/10.1038/s41587-025-02812-8

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Problem: BLAST-style search against **millions** of bacterial genomes.
LexicMap indexes probe/seed structure for fast, lower-memory alignment of
moderate-length queries. Use for gene/plasmid/long-read queries against large
genome warehouses (`progenomes`, AllTheBacteria, GTDB reps).

| Task | Prefer |
|------|--------|
| Illumina reads → contigs (binning coverage) | `strobealign` / `bowtie2` |
| Gene/plasmid vs million genomes | `lexicmap` |
| Phylogeny-compressed 661k on a laptop | `phylign` |
| Protein remote homology | `diamond` / `mmseqs2` / `erast` |
| Species ANI between MAGs | `skani` / `fastani` |

## How to run

Build one immutable index from a genome directory (`-I`) or an explicit file list
(`-S -X`), then query that index repeatedly.

```bash
set -Eeuo pipefail
genomes="${1:?usage: lexicmap-index.sh GENOME_DIR OUTPUT_DIR}"
out="${2:?usage: lexicmap-index.sh GENOME_DIR OUTPUT_DIR}"
test -d "$genomes" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
lexicmap index -I "$genomes" -O "$out/reference.lmi" \
  >"$out/index.stdout.log" 2>"$out/index.stderr.log"
test -d "$out/reference.lmi"
```

```bash
set -Eeuo pipefail
index="${1:?usage: lexicmap-search.sh INDEX QUERY_FASTA OUTPUT_DIR}"
query="${2:?usage: lexicmap-search.sh INDEX QUERY_FASTA OUTPUT_DIR}"
out="${3:?usage: lexicmap-search.sh INDEX QUERY_FASTA OUTPUT_DIR}"
test -d "$index" && test -s "$query" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
lexicmap search -d "$index" "$query" -o "$out/hits.tsv" \
  --align-min-match-pident 80 --min-qcov-per-hsp 70 \
  --min-qcov-per-genome 70 --top-n-genomes 10000 \
  >"$out/search.stdout.log" 2>"$out/search.stderr.log"
test -e "$out/hits.tsv"
```

For plasmids or other long/circular queries, use a separately justified coverage,
minimum-match-length, and top-N policy; do not reuse gene defaults blindly.

## Validation, recovery, and provenance

Verify index completion, genome count, stable genome IDs, input manifest
coverage, and index checksum/size. For searches, inspect the header and validate
`qcovGnm`, `qcovHSP`, identity, aligned length, E-value, and hit multiplicity
against the biological question. Zero hits can be valid; truncated logs or a
missing header are not. LexicMap is not intended as a short-read coverage mapper.

Record LexicMap version, index options, genome manifest/releases/checksums, query
checksum, thresholds, top-N policy, commands, logs, and result checksum. Rebuild
under a new path when the genome collection or incompatible software changes.

## Related skills

`homology-search` · `phylign` · `minimap2` · `diamond` · `mmseqs2` · `erast` ·
`progenomes` · `gtdb` · `plasmaag` · `tool-selection`
