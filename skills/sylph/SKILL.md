---
name: sylph
description: >
  Rapid species-level metagenome profiling and containment estimation. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, sketch, profile"
  metagenomics.upstream: "https://github.com/bluenote-1577/sylph"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "current sylph profile v2 database interface checked against upstream docs; not executed here"
---

# sylph

Upstream: [sylph](https://github.com/bluenote-1577/sylph)

## Citation

Shaw, J. & Yu, Y. W. Rapid species-level metagenome profiling and containment estimation with sylph. *Nat. Biotechnol.* **43**, 1348–1359 (2025). https://doi.org/10.1038/s41587-024-02412-y

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Containment ANI between a reference genome and a metagenome is **biased at low
coverage** (missing k-mers look like divergence). Sylph models k-mer coverage
with a **zero-inflated Poisson**, estimates effective coverage λ, and reports
**coverage-adjusted ANI** plus abundances — two orthogonal outputs.

Why it matters:

- Very fast sketch-based profiling for large cohorts / large genome databases.
- Better presence/ANI calls for low-coverage genomes than naive containment.
- Complementary to MetaPhlAn (markers) and Kraken (LCA k-mers); cite sketch DB.
- User coverage thresholds still matter; assembly incompleteness ≠ low coverage.

## How to run

Current prebuilt databases use the v2 `.syl2db` interface. Keep mate lists
explicit and identically ordered for multi-sample runs.

```bash
set -Eeuo pipefail
id="${1:?usage: profile-sylph.sh SAMPLE_ID DATABASE.syl2db R1 R2 OUTPUT_DIR}"
db="${2:?usage: profile-sylph.sh SAMPLE_ID DATABASE.syl2db R1 R2 OUTPUT_DIR}"
r1="${3:?usage: profile-sylph.sh SAMPLE_ID DATABASE.syl2db R1 R2 OUTPUT_DIR}"
r2="${4:?usage: profile-sylph.sh SAMPLE_ID DATABASE.syl2db R1 R2 OUTPUT_DIR}"
out="${5:?usage: profile-sylph.sh SAMPLE_ID DATABASE.syl2db R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$db" "$r1" "$r2"; do test -s "$input" || exit 2; done
gzip -t "$r1" "$r2"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

sylph profile -d "$db" -1 "$r1" -2 "$r2" -t "$threads" \
  >"$out/${id}.profile.tsv" 2>"$out/${id}.sylph.stderr.log"
test -s "$out/${id}.profile.tsv"
```

Use `sylph-tax` when taxonomic aggregation is required; base `sylph profile`
reports database-genome matches. Custom database construction and `query`
semantics should follow the pinned release documentation.

## Key parameters

| Parameter | Notes |
|-----------|-------|
| `-c` | Subsampling rate (default 200 in paper examples) |
| sketch DB | Prebuilt (e.g. GTDB-based) or custom — pin version |
| coverage threshold | Presence gate; report in Methods |
| `profile` vs `query` | Abundance profiling vs genome containment ANI |

## Decision notes

- Stage: **taxonomy** / genome presence
- Prefer for large-scale genome-resolved containment + profiling speed
- Do not merge with MetaPhlAn/Kraken unlabeled

## Validation, recovery, and provenance

Check database-genome IDs, estimated coverage, coverage-adjusted ANI, abundance,
containment/presence filters, duplicate references, and negative controls. Retain
zero/no-hit samples and distinguish low biological abundance from low reference
coverage or incomplete references. Do not merge genome-level sylph results with
marker/k-mer taxonomic tables without an explicit harmonization layer.

Use fresh outputs after database or threshold changes. Record sylph and database
format versions, database source/release/checksum, read checksums, commands,
threads, logs, output schema, filtering rules, and result checksum. Presence and
ANI remain reference-conditioned estimates.

## Related skills

`metaphlan` · `kraken2` · `motus` · `metabuli` · `skani` · `coverm` ·
`tool-selection` · `metagenomics-workflow`
