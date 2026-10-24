---
name: foldcomp
description: >
  Foldcomp — compress and index large protein structure sets (Steinegger lab) for
  efficient storage and random access before Foldseek-scale searches. Use when: (1)
  Archiving AFDB-scale PDB collections, (2) Reducing disk for structure search
  pipelines, (3) Extracting sequences/pLDDT from Foldcomp DBs. Route via homology-search
  with foldseek.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Foldcomp, structure, compression, AFDB, Foldseek"
  metagenomics.upstream: "https://github.com/steineggerlab/foldcomp"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "compress/check/extract CLI checked against current upstream README; not executed here"
---

# Foldcomp

Upstream: [steineggerlab/foldcomp](https://github.com/steineggerlab/foldcomp)

## Citation

Kim, H., Mirdita, M. & Steinegger, M. Foldcomp: a library and format for
compressing and indexing large protein structure sets. *Bioinformatics* **39**,
btad153 (2023). https://doi.org/10.1093/bioinformatics/btad153

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Structure search needs structures on disk. Foldcomp provides a compact
**format + index** for large PDB/mmCIF collections used with Foldseek-family
tools. Infrastructure skill — not a homology algorithm itself.

## How to run

Create a Foldcomp database from a structure directory and verify it by checking
the archive and extracting amino-acid sequences.

```bash
set -Eeuo pipefail
structures="${1:?usage: compress-foldcomp.sh STRUCTURE_DIR OUTPUT_DIR}"
out="${2:?usage: compress-foldcomp.sh STRUCTURE_DIR OUTPUT_DIR}"
threads="${THREADS:-8}"
test -d "$structures" || exit 2
find "$structures" -type f \( -name '*.pdb' -o -name '*.cif' -o \
  -name '*.pdb.gz' -o -name '*.cif.gz' \) -print -quit | grep -q . || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
foldcomp compress -t "$threads" -r --db "$structures" "$out/structures" \
  >"$out/compress.stdout.log" 2>"$out/compress.stderr.log"
foldcomp check -t "$threads" "$out/structures" \
  >"$out/check.stdout.log" 2>"$out/check.stderr.log"
foldcomp extract --amino-acid -t "$threads" "$out/structures" \
  "$out/sequences.fasta" >"$out/extract.stdout.log" \
  2>"$out/extract.stderr.log"
test -s "$out/sequences.fasta"
find "$out" -maxdepth 1 -type f -name 'structures*' -size +0c -print -quit | grep -q .
```

Subset decompression requires a frozen ID list and a fresh destination. Do not
use `--overwrite` in a production archive.

## Decision tree

```text
Many protein structures to store/search?
├─ Compress/index archive → foldcomp
├─ Search → foldseek / folddisco / foldmason
└─ Sequence-only path → foldseek + ProstT5
```

## Validation, recovery, and provenance

Reconcile input structures and extracted IDs; inspect failed/skipped discontinuous
structures, duplicate IDs, chain/model policy, pLDDT retention, check output,
compression ratio, and random subset decompression/RMSD. A sequence extract alone
does not prove coordinates round-trip correctly.

Use fresh output after changing inputs, options, binary, or format. Record
Foldcomp version/build, input manifest/checksums and structure source, commands,
logs, database component checksums, check report, subset round-trip metrics, and
extracted sequence checksum. Compression is infrastructure, not a homology or
quality result.

## Related skills

`foldseek` · `foldmason` · `folddisco` · `homology-search` · `tool-selection`
