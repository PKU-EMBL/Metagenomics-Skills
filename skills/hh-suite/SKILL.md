---
name: hh-suite
description: >
  HH-suite3 (HHblits / HHsearch) — remote protein homology via HMM–HMM alignment (Söding
  lab). Use when: (1) Sequence identity is too low for BLAST/MMseqs easy hits, (2)
  Building/searching profile HMMs (BFD, UniClust, Pfam-style DBs), (3) Feeding sensitive
  MSAs into structure prediction Route via homology-search; complements mmseqs2 and
  foldseek.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "HHblits, HHsearch, HH-suite, HMM, remote-homology, search"
  metagenomics.upstream: "https://github.com/soedinglab/hh-suite"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "HHblits/HHsearch database-prefix workflow statically reviewed; not executed here"
---

# HH-suite3

Upstream: [soedinglab/hh-suite](https://github.com/soedinglab/hh-suite)

## Citation

Remmert, M., Biegert, A., Hauser, A. & Söding, J. HHblits: lightning-fast
iterative protein sequence searching by HMM-HMM alignment. *Nat. Methods*
**9**, 173–175 (2012). https://doi.org/10.1038/nmeth.1818

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Profile–profile search (HMM–HMM) recovers remote homologs that single-sequence
tools miss. Still a **sequence/profile** method — pair with `foldseek` when
structures exist. Large DBs (BFD via PLASS catalogues, UniClust) need disk and
careful pinning.

| vs | Prefer HH-suite when |
|----|----------------------|
| `mmseqs2` | Need iterative profile search / MSA for folding |
| `foldseek` | No structures yet; profile MSA / remote homology |
| `plmsearch` | Classical HMM profiles preferred over PLM embeddings |

## How to run

Use a single protein query (or justified input MSA) and a frozen HH-suite database
prefix whose components belong to the same release.

```bash
set -Eeuo pipefail
query="${1:?usage: run-hhsuite.sh QUERY_FASTA OUTPUT_DIR}"
out="${2:?usage: run-hhsuite.sh QUERY_FASTA OUTPUT_DIR}"
db="${HH_DB_PREFIX:?set HH_DB_PREFIX to a pinned database prefix}"
threads="${THREADS:-8}"
iterations="${HHBLITS_ITERATIONS:-3}"
test -s "$query" || exit 2
for component in \
  "${db}_a3m.ffdata" "${db}_a3m.ffindex" \
  "${db}_hhm.ffdata" "${db}_hhm.ffindex" \
  "${db}_cs219.ffdata" "${db}_cs219.ffindex"; do
  test -s "$component" || exit 2
done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
hhblits -i "$query" -d "$db" -n "$iterations" -cpu "$threads" \
  -o "$out/hhblits.hhr" -oa3m "$out/query.a3m" \
  >"$out/hhblits.stdout.log" 2>"$out/hhblits.stderr.log"
test -s "$out/hhblits.hhr" && test -s "$out/query.a3m"
hhsearch -i "$out/query.a3m" -d "$db" -cpu "$threads" \
  -o "$out/hhsearch.hhr" >"$out/hhsearch.stdout.log" \
  2>"$out/hhsearch.stderr.log"
test -s "$out/hhsearch.hhr"
```

Predeclare iteration, inclusion, probability/E-value, coverage, diversity and
maximum-sequence controls; defaults are not interchangeable across databases.

## Decision tree

```text
Remote homology without structure?
├─ Profile HMM iterative search → hh-suite (hhblits)
├─ Fast catalogue AA search → mmseqs2
├─ Structure / 3Di → foldseek
└─ Vector DB → erast
```

## Validation, recovery, and provenance

Require HHR/A3M outputs, logs, query reconciliation, and valid no-hit reports.
Inspect MSA depth/diversity/coverage, low complexity, Neff, probability/E-value,
aligned columns, secondary matches, domain boundaries, consensus drift across
iterations, and agreement with structure/sequence tools. Avoid transfer from
short profile overlaps alone.

Use fresh output after changing query, database, settings, or release. Record
HH-suite version/build, database name/date/component checksums, query checksum,
all options, commands/logs, HHR/A3M checksums, selected-hit rules, and MSA
trimming. Profile probability supports homology, not orthology or a specific
biochemical function without contextual evidence.

## Related skills

`homology-search` · `mmseqs2` · `foldseek` · `plass` · `plmsearch` ·
`tool-selection`
