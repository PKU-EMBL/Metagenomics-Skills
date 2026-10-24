---
name: qsap
description: >
  QSAP — quorum-sensing (QS) related gene annotation pipeline against the QSP database
  (DIAMOND and/or HMMER). Use when mining autoinducer / QS circuitry (AHL, AIP,
  AI-2-related families as covered by QSP) from proteins or assemblies. Related
  secondary metabolites → antismash; Fe siderophores → fegenie.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "QSAP, quorum-sensing, QS, autoinducer, signaling, genome-mining"
  metagenomics.upstream: "https://github.com/chunxiao-dcx/QSAP"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "QSAP.pl list/strategy interface checked against upstream README; not executed here"
---

# QSAP (quorum sensing)

Upstream: [chunxiao-dcx/QSAP](https://github.com/chunxiao-dcx/QSAP) ·
QSP database: https://github.com/chunxiao-dcx/QSP

## Citation

Pipeline/DB: Dai, C. QSAP / QSP — quorum-sensing protein resources
(https://github.com/chunxiao-dcx/QSAP). Cite the upstream repository and QSP
release used; add peer-reviewed QSP/QSAP citation when available in Methods.

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

**Quorum sensing (群体感应)** coordinates population behaviors via signal
synthases/receptors/transporters. QSAP classifies QS-related sequences from
the QSP collection. Treat hits as genetic potential — not measured autoinducer
concentrations.

| Related claim | Prefer |
|---------------|--------|
| QS genes | `qsap` |
| Specialized metabolite / AHL-adjacent BGCs | `antismash` |
| Siderophores (Fe acquisition signals/competition) | `fegenie` |
| Broad metabolism | `dram` / `element-cycling` |

## How to run

Use an absolute-path input list containing one FASTA path per line. Do not mix
nucleotide and protein query types. Pin the QSAP checkout and bundled QSP data.

```bash
set -Eeuo pipefail
home="${QSAP_HOME:?set QSAP_HOME to a pinned checkout}"
input_list="${1:?usage: run-qsap.sh ABS_INPUT_LIST ABS_OUTPUT_DIR}"
out="${2:?usage: run-qsap.sh ABS_INPUT_LIST ABS_OUTPUT_DIR}"
threads="${THREADS:-8}"
strategy="${QSAP_STRATEGY:-sub}"
[[ "$input_list" = /* && "$out" = /* ]] || exit 2
case "$strategy" in sub|union|hmmscan|diamond) ;; *) exit 2 ;; esac
test -s "$home/QSAP.pl" && test -s "$input_list" || exit 2
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
while IFS= read -r query; do
  [[ -z "$query" ]] && continue
  [[ "$query" = /* ]] && test -s "$query" || exit 2
done <"$input_list"
mkdir -p "$(dirname "$out")" "${out}.logs"

(
  cd "$home"
  perl ./QSAP.pl -i "$input_list" -o "$out" -s "$strategy" -n "$threads"
) >"${out}.logs/qsap.stdout.log" 2>"${out}.logs/qsap.stderr.log"
test -d "$out/outputs"
find "$out/outputs" -type f -size +0c -print -quit | grep -q .
```

## Decision tree

```text
Cell–cell signaling / QS?
├─ QS gene annotation → qsap
├─ BGC / natural products → antismash
├─ Siderophores → fegenie
└─ Plasmid-borne QS context → genomad / mob-suite ∩ qsap
```

## Validation, recovery, and provenance

Require per-sample raw alignment outputs, an input/sample reconciliation, logs,
and abundance merge only when read or abundance-table mode was requested.
Inspect sequence type, IDs, HMM/DIAMOND support, identity/coverage thresholds,
`sub` versus `union` integration, conflicting functional labels, paralogs, and
fragmented hits. Retain no-hit samples and coordinates where available.

Use fresh outputs after changing QSP, strategy, query type, or thresholds. Record
QSAP/QSP commits and checksums, DIAMOND/HMMER/Salmon versions as applicable,
input/read/abundance checksums, command, logs, raw and merged outputs, and all
filters. QS-gene similarity supports potential, not signaling, expression, or
measured autoinducer production.

## Related skills

`antismash` · `fegenie` · `dram` · `genomad` · `mob-suite` ·
`microbial-mining` · `tool-selection`
