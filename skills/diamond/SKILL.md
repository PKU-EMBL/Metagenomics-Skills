---
name: diamond
description: >
  Ultra-fast protein alignment (BLASTP/X alternative) for functional/taxonomic searches.
  Use for installation, parameter choice, execution, output interpretation, or
  troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, protein, blast"
  metagenomics.upstream: "https://github.com/bbuchfink/diamond"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "DIAMOND database/search template statically reviewed; not executed here"
---

# DIAMOND

Upstream: [DIAMOND](https://github.com/bbuchfink/diamond)

## Citation

Buchfink, B., Reuter, K. & Drost, H.-G. Sensitive protein alignments at tree-of-life scale using DIAMOND. *Nat. Methods* **18**, 366–368 (2021). https://doi.org/10.1038/s41592-021-01101-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

DIAMOND provides sensitive protein alignments at proteome/tree-of-life scale
(Buchfink *et al.*, 2021) — the workhorse behind many functional and taxonomic
protein searches (eggNOG-mapper, DAS Tool protein search, custom NR/UniRef).

- Use `blastx`/`blastp` for genes/proteins; not a substitute for nucleotide
  coverage mappers (`strobealign` / `bowtie2`) needed for binning.
- Sensitivity modes (`--fast` → `--ultra-sensitive`) trade speed for remote
  homolog recall — state the mode in Methods.
- Tabular `-f 6` is pipeline-friendly; keep DB version pinned.


## How to run

Build an immutable database from a release-pinned reference, then search under a
fresh result directory.

```bash
set -Eeuo pipefail
reference="${1:?usage: diamond-search.sh REFERENCE_FAA QUERY_FAA OUTPUT_DIR}"
query="${2:?usage: diamond-search.sh REFERENCE_FAA QUERY_FAA OUTPUT_DIR}"
out="${3:?usage: diamond-search.sh REFERENCE_FAA QUERY_FAA OUTPUT_DIR}"
threads="${THREADS:-16}"
for input in "$reference" "$query"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

diamond makedb --in "$reference" --db "$out/reference" \
  >"$out/makedb.stdout.log" 2>"$out/makedb.stderr.log"
diamond blastp --query "$query" --db "$out/reference" \
  --out "$out/hits.tsv" --threads "$threads" --sensitive \
  --outfmt 6 qseqid sseqid pident length evalue bitscore qcovhsp scovhsp \
  >"$out/search.stdout.log" 2>"$out/search.stderr.log"
```

## Key parameters

| `blastp/blastx` | mode | |
| `-f 6` | tabular | BLAST-like |

## Validation, recovery, and provenance

A zero-row hit table can be valid, but the file and completed logs must exist.
When non-empty, require eight tab-separated fields, valid numeric ranges, and
query IDs that join back to the input. Apply identity, coverage, E-value, and
best-hit/orthology rules explicitly; a local match is not automatically a
functional assignment.

Archive DIAMOND version, sensitivity mode, output fields, reference release and
checksum, query checksum, database build/search commands, logs, and result
checksum. Keep the unfiltered hit table before downstream thresholds.

## Related skills

`eggnog-mapper` · `mmseqs2` · `homology-search` · `tool-selection` ·
`metagenomics-workflow`
