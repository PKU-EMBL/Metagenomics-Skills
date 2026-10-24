---
name: motus
description: >
  Marker-gene taxonomic profiling across environments (mOTUs3). Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, marker, profile"
  metagenomics.upstream: "https://github.com/motu-tool/mOTUs"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired-end mOTUs profile CLI checked against upstream usage; not executed here"
---

# mOTUs

Upstream: [mOTUs](https://github.com/motu-tool/mOTUs)

## Citation

Ruscheweyh, H.-J. *et al.* Cultivation-independent genomes greatly expand taxonomic-profiling capabilities of mOTUs across various environments. *Microbiome* **10**, 212 (2022). https://doi.org/10.1186/s40168-022-01410-z

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

mOTUs profiles communities with a curated set of **universal single-copy
phylogenetic marker genes**, updated with cultivation-independent genomes so
environmental / non-human biomes are better covered than early gut-centric
releases.

Compared with MetaPhlAn:

| | mOTUs | MetaPhlAn 4 |
|--|-------|-------------|
| Marker philosophy | Mostly universal SCGs → mOTU clusters | Clade-/SGB-specific marker packs |
| Strength | Cross-environment comparability | Fine SGB resolution incl. unknowns |
| Merge rule | Do not average with Kraken/MetaPhlAn unlabeled |

Pin mOTUs DB version; host-deplete first.

## How to run

Install/download the database in a pinned environment (`motus downloadDB`), then
profile one manifest-defined pair at a time.

```bash
set -Eeuo pipefail
id="${1:?usage: profile-motus.sh SAMPLE_ID R1 R2 OUTPUT_DIR}"
r1="${2:?usage: profile-motus.sh SAMPLE_ID R1 R2 OUTPUT_DIR}"
r2="${3:?usage: profile-motus.sh SAMPLE_ID R1 R2 OUTPUT_DIR}"
out="${4:?usage: profile-motus.sh SAMPLE_ID R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$r1" "$r2"; do test -s "$input" || exit 2; done
gzip -t "$r1" "$r2"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

motus profile -f "$r1" -r "$r2" -t "$threads" \
  -o "$out/${id}.motus.tsv" \
  >"$out/${id}.motus.stdout.log" 2>"$out/${id}.motus.stderr.log"
```

## Key parameters

| Item | Notes |
|------|-------|
| DB | `motus download-db` — pin version |
| `-t` | Threads |
| Downstream | Diversity / ecology tables — not MAG taxonomy (`gtdbtk`) |

## Validation, recovery, and provenance

Require a non-empty profile with the expected mOTUs/database/version headers and
a unique sample identifier. Inspect mapped marker reads, unassigned fraction,
rank/unknown mOTU handling, controls, and abundance/count units. Merge only
profiles generated with the same software/database and compatible options; do
not average mOTUs with MetaPhlAn or k-mer profiles.

Use fresh outputs after changing reads, database, or profiling mode. Record
mOTUs/BWA versions, database version/path/checksum where available, read
checksums, full command, logs, profile checksum, and merge command. Marker-based
relative abundance does not establish absolute load, viability, or absence below
detection.

## Related skills

`metaphlan` · `kraken2` · `sylph` · `metabuli` · `tool-selection` ·
`metagenomics-workflow`
