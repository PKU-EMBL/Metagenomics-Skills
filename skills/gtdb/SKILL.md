---
name: gtdb
description: >
  Use the Genome Taxonomy Database (GTDB) public releases — taxonomy tables, trees,
  metadata, and representative genomes. Use this skill when: (1) Choosing or citing a
  GTDB release, (2) Downloading bac120/ar53 taxonomy or reps, (3) Distinguishing GTDB
  data files from the GTDB-Tk runtime package, (4) Preparing reference sets for MAG
  comparison. For classifying your MAGs, use gtdbtk. For biome catalogues, use mgnify.
  For routing, use public-databases.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, GTDB, taxonomy, genomes"
  metagenomics.upstream: "https://gtdb.ecogenomic.org/"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "release 232 file layout and checksum workflow verified against the live archive; no large files downloaded"
---

# GTDB (Genome Taxonomy Database)

Portal: https://gtdb.ecogenomic.org/ ·
Downloads: https://gtdb.ecogenomic.org/downloads ·
Data: https://data.gtdb.ecogenomic.org/releases/ ·
Toolkit: [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk)

## Citation

Parks, D. H. *et al.* A complete domain-to-species taxonomy for Bacteria and Archaea. *Nat. Biotechnol.* **38**, 1079–1086 (2020). https://doi.org/10.1038/s41587-020-0501-8

Parks, D. H. *et al.* GTDB release 10: a complete and systematic taxonomy for 715 230 bacterial and 17 245 archaeal genomes. *Nucleic Acids Res.* **54**, D743–D754 (2026). https://doi.org/10.1093/nar/gkaf1040

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

GTDB provides a **rank-normalized prokaryotic taxonomy**. Your MAG labels from
binning are **not** taxonomy — GTDB assignment is a separate claim layer.

Distinguish three packages people confuse:

| Package | What it is | Typical use |
|---------|------------|-------------|
| GTDB release files (`bac120_taxonomy.tsv`, trees, metadata, genome reps) | Public taxonomy/genome release | Cite taxonomy; build custom refs |
| `GTDBTK_DATA_PATH` / `gtdbtk_data.tar.gz` | Runtime DB for GTDB-Tk | Classify genomes with `gtdbtk` |
| MGnify biome catalogues | Biome MAG catalogues (often GTDB-annotated) | Novelty / habitat context (`mgnify`) |

Always pin the **GTDB release ID** (e.g. R10-RS226 from `VERSION.txt` / release notes) next to GTDB-Tk software version.

## Release notes

Parks *et al.* describe **R10-RS226** (~715k bacterial and ~17k archaeal
genomes) in the 2026 database paper. The live archive currently exposes
**R11-RS232** under `release232/232.0/`; its release notes report 901,341 genomes
in 199,923 species clusters. Treat these as distinct snapshots.

- Major new deep lineages are rarer each release, but species discovery continues;
  do not claim that GTDB is complete.
- Website, representatives, taxonomy, and ANI methods can change by release.
- Match GTDB-Tk data packages to the release used for classification.
- Resolve `latest/VERSION.txt` only for discovery, then freeze the explicit
  `releaseNNN/NNN.0/` URL and checksums before analysis.

## Prerequisites

| Need | Resource |
|------|----------|
| Taxonomy tables / trees | `https://data.gtdb.ecogenomic.org/releases/latest/` |
| Representative genomes | `genomic_files_reps/` (very large) |
| Classify MAGs | GTDB-Tk data package → `gtdbtk` skill |

## How to fetch release metadata

This pinned example downloads only metadata/taxonomy tables, not representative
genome bundles.

```bash
set -Eeuo pipefail
release="${GTDB_RELEASE_PATH:-release232/232.0}"
[[ "$release" =~ ^release[0-9]+/[0-9]+[.]0$ ]] || exit 2
number="${release#release}"
number="${number%%/*}"
out="db/gtdb/r${number}"
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
base="https://data.gtdb.ecogenomic.org/releases/${release}"
for file in VERSION.txt RELEASE_NOTES.txt FILE_DESCRIPTIONS.txt MD5SUM.txt \
  "bac120_taxonomy_r${number}.tsv.gz" "ar53_taxonomy_r${number}.tsv.gz"; do
  curl --fail --location --retry 3 "$base/$file" -o "$out/$file" \
    2>>"$out/download.stderr.log"
done
(
  cd "$out"
  grep -E '(^|/)(bac120|ar53)_taxonomy_.*[.]tsv[.]gz$' MD5SUM.txt \
    | md5sum --check -
) >"$out/checksums.log"
```

Mirror choice is documented at https://gtdb.ecogenomic.org/downloads. For
GTDB-Tk classification, install its complete release-coupled reference bundle,
not an ad hoc genome tarball, and apply the checks in `$gtdbtk`.

For GTDB-Tk classification, install its complete release-coupled reference bundle—not an ad-hoc genome tarball—and apply the checks in `$gtdbtk`.

## Key files (thinking)

| File | Use |
|------|-----|
| `bac120_taxonomy.tsv` / `ar53_taxonomy.tsv` | Map genome → GTDB lineage |
| `*_metadata.tsv.gz` | Quality / NCBI cross-refs / stats |
| `bac120.tree` / `ar53.tree` | Reference phylogeny |
| `genomic_files_reps/` | Species-rep FASTA/proteins (huge) |

## Decision tree

```text
GTDB-related task?
├─ Classify my MAGs → gtdbtk (needs GTDB-Tk data package)
├─ Cite / parse taxonomy release tables → gtdb (this skill)
├─ Compare to human-gut species catalogue → mgnify (UHGG) ± gtdb labels
└─ Read-based species tables only → metaphlan / kraken2 (not GTDB placement)
```

## Validation, recovery, and provenance

Verify archive checksums, `VERSION.txt`, release notes, expected table headers,
unique genome accessions, lineage rank syntax, and bacterial/archaeal separation.
Do not combine taxonomy or metadata rows from different releases without an
explicit crosswalk. Download representative genomes only after estimating
storage and preserving their manifest.

Archive the explicit release URL, download date, mirror, `MD5SUM.txt`, local
checksums, file sizes, parsing code, and any accession/taxonomy crosswalk. GTDB
labels are release-specific taxonomic assignments, not read-level presence or
formal nomenclatural validation.

## Related skills

`gtdbtk` · `public-databases` · `mgnify` · `progenomes` · `cami` · `checkm2` ·
`drep` · `mag-qc` · `visualization`
