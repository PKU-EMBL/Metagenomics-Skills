---
name: maxbin2
description: >
  Automated multi-metagenome contig binning. Use for installation, parameter choice,
  execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, maxbin"
  metagenomics.upstream: "https://sourceforge.net/projects/maxbin2/"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "MaxBin 2 CLI template statically reviewed; not executed here"
---

# MaxBin 2

Upstream: [MaxBin 2](https://sourceforge.net/projects/maxbin2/)

## Citation

Wu, Y.-W., Simmons, B. A. & Singer, S. W. MaxBin 2.0: an automated binning algorithm to recover genomes from multiple metagenomic datasets. *Bioinformatics* **32**, 605–607 (2016). https://doi.org/10.1093/bioinformatics/btv638

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MaxBin 2 uses **nucleotide composition + differential abundance** across samples
(expectation-maximization). It is a classical workhorse and a valuable
**ensemble member** because it often recovers different genomes than MetaBAT2.

| vs MetaBAT2 | Notes |
|-------------|-------|
| Strength | Multi-sample abundance model; widely packaged in MetaWRAP |
| Weakness | Slower / heavier on huge contig sets; fewer adaptive TNF tricks |

Prefer multi-coverage abundance tables. Always QC with CheckM2; for catalogues
feed into `basalt` ★ / `metawrap` / `dastool`.

## How to run

The abundance file must use contig IDs matching the assembly exactly. Repeat
`-abund` only for validated, consistently ordered sample-specific tables.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-maxbin.sh ASSEMBLY ABUNDANCE OUTPUT_DIR}"
abundance="${2:?usage: run-maxbin.sh ASSEMBLY ABUNDANCE OUTPUT_DIR}"
out="${3:?usage: run-maxbin.sh ASSEMBLY ABUNDANCE OUTPUT_DIR}"
threads="${THREADS:-16}"
for input in "$assembly" "$abundance"; do test -s "$input" || exit 2; done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

run_MaxBin.pl -contig "$assembly" -abund "$abundance" \
  -out "$out/maxbin" -thread "$threads" \
  >"$out/maxbin.stdout.log" 2>"$out/maxbin.stderr.log"
```

## Key parameters

| Flag | Notes |
|------|-------|
| `-abund` | Coverage table(s); IDs must match contig headers |
| `-thread` | Threads |
| min contig length | Record the installed default and justify any override |

## Decision tree

```text
Single classical binner?
├─ Adaptive TNF+coverage → metabat2
├─ EM abundance+composition → maxbin2
├─ GMM composition+coverage → concoct
└─ Catalogue / multi-assembly → basalt ★
```

## Validation, recovery, and provenance

Require a completed summary/log and non-empty bin FASTAs with unique contig
membership. Reconcile assembly IDs against the abundance table, quantify binned
and unbinned bases, inspect marker summaries, and run `checkm2` plus `gunc` on
exported bins. Compare MaxBin2 as one ensemble member; do not select it solely by
raw bin count.

Rerun changed inputs or abundance sets under a new prefix. Record MaxBin2 and
marker/database versions, assembly/abundance checksums, sample order, command,
logs, minimum-contig settings, contig2bin table, QC results, and bin checksums.

## Related skills

`metabat2` · `concoct` · `dastool` · `metawrap` · `basalt` · `checkm2` · `gunc` ·
`tool-selection`
