---
name: folddisco
description: >
  Folddisco — fast discontinuous structural motif search across the protein universe
  (Steinegger lab). Use when: (1) Searching catalytic triads / zinc fingers / other
  short motifs in AFDB/PDB/ESM30, (2) Motif-level annotation after Foldseek fold hits,
  (3) Mining conserved geometry in MAG protein structures. Route via homology-search /
  metagenomics-llm; complement foldseek (full-chain) and mmseqs2 (sequence).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Folddisco, motif, structure-search, AFDB, Foldseek"
  metagenomics.upstream: "https://github.com/steineggerlab/folddisco"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "current motif query/output options checked against upstream README; not executed here"
---

# Folddisco

Upstream: [steineggerlab/folddisco](https://github.com/steineggerlab/folddisco) ·
Web: https://search.foldseek.com/folddisco

## Citation

Kim, H., Kim, R. S., Mirdita, M., Yoon, J. & Steinegger, M. Structural motif
search across the protein universe with Folddisco. *Nat. Biotechnol.* (2026).
https://doi.org/10.1038/s41587-026-03162-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Foldseek finds similar **folds / chains**; many functions depend on a small
**discontinuous motif** (catalytic residues, metal sites). Folddisco indexes
geometric hashes so motif queries scale to AFDB50 / ESM30 / PDB. In the
Steinegger “levels of conservation” framing: sequence/fold (`mmseqs2` /
`foldseek`) → multimer (`foldseek` multimer) → **motif (`folddisco`)**.

| vs | Prefer Folddisco when |
|----|------------------------|
| `foldseek` | Motif / active-site geometry, not global fold TM |
| `mmseqs2` | Residues are discontinuous or sequence-divergent |
| HMM / PROSITE | Have a 3D motif definition from a structure |

Caveats: motif length limits (long selections fail on the web UI); hits need
manual residue chemistry checks; pin index version (v2 `*.tar.lz4` vs legacy).

## How to run

Define motif residues from a named structure before searching a pinned index.
Default output includes partial matches, so retain coverage/RMSD fields.

```bash
set -Eeuo pipefail
index="${1:?usage: query-folddisco.sh INDEX QUERY_STRUCTURE RESIDUES OUTPUT_DIR}"
query="${2:?usage: query-folddisco.sh INDEX QUERY_STRUCTURE RESIDUES OUTPUT_DIR}"
residues="${3:?usage: query-folddisco.sh INDEX QUERY_STRUCTURE RESIDUES OUTPUT_DIR}"
out="${4:?usage: query-folddisco.sh INDEX QUERY_STRUCTURE RESIDUES OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$query" || exit 2
if [[ ! -e "$index" ]] && ! compgen -G "${index}*" >/dev/null; then exit 2; fi
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
folddisco query -i "$index" -p "$query" -q "$residues" -t "$threads" \
  --header --per-structure >"$out/hits.tsv" 2>"$out/folddisco.stderr.log"
test -s "$out/hits.tsv"
head -n 1 "$out/hits.tsv" | grep -q 'tid'
```

For whole-structure sampling, omit `-q` and predeclare `--sampling-ratio` and
`--skip-match`; this is a different evidence mode. Prebuilt indexes are at
https://opendata.mmseqs.org/folddisco/. Web: https://search.foldseek.com/folddisco

## Key parameters

| Setting | Notes |
|---------|-------|
| `-p` / `-q` | Query PDB/mmCIF and residue list (`B57,B102,C195`) |
| `-i` | Precomputed Folddisco index — pin release |
| `-d` / `-a` | Distance (Å) / angle (°) prefilter sensitivity |
| `--skip-match` | Geometric search without AA identity constraints |
| `--sampling-ratio` | Speed/sensitivity trade-off for long queries |

## Decision tree

```text
Structure-aware annotation need?
├─ Global fold / chain → foldseek
├─ Complex / interface → foldseek easy-multimersearch
├─ Short discontinuous motif → folddisco
├─ Sequence only → mmseqs2 / plmsearch
└─ Gene neighborhood modules → spacedust
```

## Validation, recovery, and provenance

Require header-preserving raw hits and explicit no-hit queries. Inspect residue
numbering/chain IDs, missing atoms, motif chemistry, node coverage, IDF, RMSD,
partial/confident status, database redundancy, structure confidence, and
sensitivity to distance/angle/substitution settings. Confirm shortlisted hits by
coordinate visualization and independent alignment or biochemical context.

Use fresh output after changing motif, structure, index, thresholds, or release.
Record Folddisco version/commit, index release/checksum, source structure and
residue definition, command/log, output fields, filters, and reviewed coordinates.
Geometric similarity is a candidate motif, not measured catalysis or binding.

## Related skills

`foldseek` · `metagenomics-llm` · `mmseqs2` · `spacedust` · `plmsearch` ·
`deepblast` · `microbial-mining` · `tool-selection`
