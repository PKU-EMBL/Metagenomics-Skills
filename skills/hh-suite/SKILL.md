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

```bash
set -euo pipefail
DB=${HH_DB_PREFIX:?set HH_DB_PREFIX to a pinned HH-suite database prefix}
[[ -s query.faa && -s "${DB}_a3m.ffdata" && -s "${DB}_a3m.ffindex" ]] || exit 2
mkdir -p temp/hh
hhblits -i query.faa -o temp/hh/query.hhr -oa3m temp/hh/query.a3m \
  -n 1 -d "$DB"
test -s temp/hh/query.hhr && test -s temp/hh/query.a3m
hhsearch -i temp/hh/query.a3m -d "$DB" -o temp/hh/query_hhsearch.hhr
test -s temp/hh/query_hhsearch.hhr
```

## Decision tree

```text
Remote homology without structure?
├─ Profile HMM iterative search → hh-suite (hhblits)
├─ Fast catalogue AA search → mmseqs2
├─ Structure / 3Di → foldseek
└─ Vector DB → erast
```

## Related skills

`homology-search` · `mmseqs2` · `foldseek` · `plass` · `plmsearch` ·
`tool-selection`
