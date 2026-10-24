---
name: antismash
description: >
  Detect and annotate biosynthetic gene clusters (BGCs) on genomes and MAGs. Use for
  natural-product genome mining, choosing genefinding, interpreting region HTML/JSON,
  and stating validation limits.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "BGC, secondary-metabolite, genome-mining"
  metagenomics.upstream: "https://github.com/antismash/antismash"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "per-genome antiSMASH CLI template statically reviewed; not executed here"
---

# antiSMASH

Upstream: [antismash/antismash](https://github.com/antismash/antismash)

## Citation

Blin, K. *et al.* antiSMASH 7.0: new and improved predictions for detection,
regulation, chemical structures and visualisation. *Nucleic Acids Res.* **51**,
W46–W50 (2023). https://doi.org/10.1093/nar/gkad344

## Analytical thinking

antiSMASH finds **BGC regions** (PKS, NRPS, RiPP, terpene, …). It does **not**
prove a compound is produced. Fragmented MAGs truncate clusters — prefer
near-complete bins (`checkm2` / `mag-qc`) and note contig breaks inside regions.

Run on **per-genome FASTA** (or GenBank from `bakta`/`prokka`), not mixed
community contigs, unless you explicitly want contig-level screens and will
not assign clusters to species without binning.

Record antiSMASH version **and** database download date. For comparative BGC
families across MAGs, follow with BiG-SCAPE (`bigscape`).

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Genome/MAG FASTA | Completeness ≥50–70% for claims |
| DBs | `download-antismash-databases` | Shared read-only path |
| CPU | 8 | 16+ |
| Gene finding | prodigal (meta/MAGs) | Or use Bakta GenBank |

## How to run

Install databases in a pinned environment before the study. This example is for
one bacterial MAG FASTA; use a separate output per genome.

```bash
set -Eeuo pipefail
id="${1:?usage: run-antismash.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
genome="${2:?usage: run-antismash.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
out="${3:?usage: run-antismash.sh GENOME_ID GENOME_FASTA OUTPUT_DIR}"
threads="${THREADS:-16}"
taxon="${ANTISMASH_TAXON:-bacteria}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
case "$taxon" in bacteria|fungi) ;; *) exit 2 ;; esac
test -s "$genome" || exit 2
log_dir="${out}.logs"
test ! -e "$out" && test ! -e "$log_dir" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$log_dir"

antismash "$genome" --output-dir "$out" --html-title "$id" \
  --cpus "$threads" --genefinding-tool prodigal --taxon "$taxon" \
  >"$log_dir/antismash.stdout.log" 2>"$log_dir/antismash.stderr.log"
test -s "$out/index.html"
find "$out" -maxdepth 1 -type f -name '*.json' -print -quit | grep -q .
```

For Bakta/Prokka GenBank input, omit or verify gene-finding options so existing
annotations are handled as intended. Do not mix outputs from different module or
database configurations in one comparative set.

## Key parameters

| Option | Guidance |
|--------|----------|
| `--genefinding-tool prodigal` | Default for MAG FASTA |
| `--taxon bacteria/fungi` | Affects rules; match organism |
| `--cb-knownclusters` / MiBIG opts | Enable when comparing to known BGCs (version-dependent) |
| `--minimal` | Faster, fewer analyses — for screens only |

## Outputs to archive

| Path | Meaning |
|------|---------|
| `index.html` | Interactive regions |
| `*.json` / region GenBanks | Machine-readable clusters |
| stdout cluster counts | Summary for tables |

## Decision tree

```text
BGC mining goal?
├─ Single HQ MAG → bakta/prokka → antismash → (optional) bigscape
├─ Many MAGs catalogue → filter by checkm2 first, then batch antismash
└─ Need AMP smORFs not BGCs → macrel (different claim)
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| DB missing errors | Re-run `download-antismash-databases` |
| Zero clusters on huge MAG | Check prodigal ran; try GenBank input |
| Huge runtime | Use `--minimal` for pilot; full mode for finals |

## Validation, recovery, and provenance

Require HTML, JSON, annotated GenBank and region files, completed logs, unique
record IDs, and an input-to-region audit including zero-region genomes. Inspect
cluster boundaries, contig-edge truncation, product/class confidence, gene
finding, known-cluster similarity, and MAG quality. Cross-genome family analysis
must use compatible antiSMASH/module/database versions.

Use a fresh directory after changing genome, database, modules, or release.
Record antiSMASH and dependency versions, database/MIBiG snapshot and checksums,
input/annotation checksums, taxon/gene-finding/module flags, commands, logs,
region manifest, and output checksums. BGC predictions indicate biosynthetic
potential, not expression or compound production.

## Related skills

`microbial-mining` · `bakta` · `prokka` · `bigscape` · `dram` · `checkm2` ·
`mag-qc`
