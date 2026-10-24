---
name: defensefinder
description: >
  Detect anti-phage defense systems in prokaryotic genomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "defense, CRISPR, genome-mining"
  metagenomics.upstream: "https://github.com/mdmparis/defense-finder"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "run/models-dir CLI checked against current upstream documentation; not executed here"
---

# DefenseFinder

Upstream: [DefenseFinder](https://github.com/mdmparis/defense-finder)

## Citation

Tesson, F. *et al.* Systematic and quantitative view of the antiviral arsenal of prokaryotes. *Nat. Commun.* **13**, 2561 (2022). https://doi.org/10.1038/s41467-022-30269-9

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Mines **defense systems** (CRISPR and beyond). Complements `padloc` (different
system models — often run both for surveys) and viral MGE mining
(`genomad` / `virsorter2`) for host–virus interaction stories.

## How to run

Protein inputs must remain in genomic order because system architecture is part
of the evidence. Freeze the model release rather than running `update` mid-study.

```bash
set -Eeuo pipefail
proteins="${1:?usage: run-defensefinder.sh ORDERED_PROTEINS_FAA OUTPUT_DIR}"
out="${2:?usage: run-defensefinder.sh ORDERED_PROTEINS_FAA OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$proteins" || exit 2
test ! -e "$out" && test ! -e "${out}.stdout.log" && \
  test ! -e "${out}.stderr.log" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")"
model_args=()
if [[ -n "${DEFENSEFINDER_MODELS:-}" ]]; then
  test -d "$DEFENSEFINDER_MODELS" || exit 2
  model_args=(--models-dir "$DEFENSEFINDER_MODELS")
fi

defense-finder run -o "$out" -w "$threads" --preserve-raw \
  "${model_args[@]}" "$proteins" \
  >"${out}.stdout.log" 2>"${out}.stderr.log"
find "$out" -type f -name '*systems*.tsv' -print -quit | grep -q .
find "$out" -type f -name '*genes*.tsv' -print -quit | grep -q .
```

## Key parameters

| input | proteins preferred | From Bakta/Prokka |
| models | installed DB | Pin |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Validation, recovery, and provenance

Require systems, genes, and HMM hit tables plus raw MacSyFinder output when
requested. Reconcile input proteins, system boundaries, complete/incomplete
status, model coverage, duplicate/overlapping systems, and contig-edge effects.
Cross-check survey-level conclusions with PADLOC while keeping model-specific
calls separate.

Use fresh outputs after changing proteins, models, coverage, or release. Record
DefenseFinder/MacSyFinder versions, model repository commit/checksum, ordered
protein and genome annotation checksums, command, logs, raw/system tables, and
result checksums. Predicted systems indicate genomic potential, not measured
phage resistance.

## Related skills

`padloc` · `genomad` · `virsorter2` · `spacedust` · `bakta` · `antismash` ·
`microbial-mining` · `tool-selection` · `metagenomics-workflow`
