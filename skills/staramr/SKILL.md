---
name: staramr
description: >
  staramr — scan assemblies against ResFinder, PointFinder, and PlasmidFinder databases
  in one report (PHAC-NML). Use for isolate AMR + plasmid replicon summaries when you
  want CGE DBs without running each Finder separately. Route via cge-finders /
  microbial-mining; CARD catalogues still via rgi.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "staramr, CGE, ResFinder, PointFinder, PlasmidFinder, AMR, plasmid"
  metagenomics.upstream: "https://github.com/phac-nml/staramr"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "search/db-info/PointFinder interface checked against current upstream README; not executed here"
---

# staramr

Upstream: [phac-nml/staramr](https://github.com/phac-nml/staramr)

## Citation

Bharat, A. *et al.* Correlation between Phenotypic and In Silico Detection of
Antimicrobial Resistance in *Salmonella enterica* in Canada Using Staramr.
*Microorganisms* **10**, 292 (2022).
https://doi.org/10.3390/microorganisms10020292

Uses CGE databases — also cite ResFinder / PointFinder / PlasmidFinder papers
(see `resfinder`, `pointfinder`, `plasmidfinder`).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

staramr is a **convenience scanner** over CGE ResFinder + PointFinder +
PlasmidFinder DBs with summary TSVs. Ideal for isolate batches and One-Health
surveillance pipelines. Still genotype-level — phenotype concordance is
organism/drug dependent.

Does **not** replace VirulenceFinder or MobileElementFinder. Does **not** use
CARD; keep `rgi` separate. For PointFinder, set the correct
`--pointfinder-organism`.

## How to run

Use the database bundled with a pinned staramr release or update once and freeze
it before the cohort. PointFinder must be enabled only with a supported,
independently established organism.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-staramr.sh ASSEMBLY_FASTA OUTPUT_DIR}"
out="${2:?usage: run-staramr.sh ASSEMBLY_FASTA OUTPUT_DIR}"
threads="${THREADS:-8}"
test -s "$assembly" || exit 2
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "${out}.logs"
point_args=()
if [[ -n "${POINTFINDER_ORGANISM:-}" ]]; then
  point_args=(--pointfinder-organism "$POINTFINDER_ORGANISM")
fi
staramr db info >"${out}.logs/database-info.txt"
staramr search -n "$threads" -o "$out" "${point_args[@]}" "$assembly" \
  >"${out}.logs/staramr.stdout.log" 2>"${out}.logs/staramr.stderr.log"
test -s "$out/summary.tsv"
test -s "$out/detailed_summary.tsv"
test -s "$out/settings.txt"
```

## Decision tree

```text
Need Res + Point + Plasmid in one pass?
├─ Yes (isolates) → staramr
├─ Only acquired AMR CLI → resfinder
├─ Only replicons → plasmidfinder
├─ Virulence / named MGEs → virulencefinder / mobileelementfinder
└─ CARD meta catalogue → rgi
```

## Validation, recovery, and provenance

Require summary, detailed, ResFinder, PointFinder, PlasmidFinder, MLST,
settings, hit FASTAs, logs, and database info; retain negative isolates. Inspect
quality-module assumptions, identity/overlap, fragmented/duplicate genes,
mutation support and organism validity, replicon context, novel/partial STs, and
cross-database conflicts. Do not silently exclude genes or negatives.

Use fresh outputs after changing assembly, databases, thresholds, organism, or
release. Record staramr/BLAST/mlst versions, all CGE commits and gene-drug table
versions, assembly checksum, command, settings/logs, result checksums, and
interpretation rules. Report predicted microbiological resistance separately
from clinical resistance and laboratory AST.

## Related skills

`cge-finders` · `resfinder` · `pointfinder` · `plasmidfinder` ·
`virulencefinder` · `mobileelementfinder` · `rgi` · `mob-suite` · `genomad` ·
`microbial-mining` · `tool-selection`
