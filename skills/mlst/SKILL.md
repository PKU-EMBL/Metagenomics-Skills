---
name: mlst
description: >
  mlst — chromosomal multilocus sequence typing of assemblies against PubMLST schemes
  (Torsten Seemann wrapper). Use for isolate / HQ-MAG species ST calling. Route via
  cge-finders / microbial-mining for isolate packages; plasmid ST → pmlst (different
  schemes).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MLST, PubMLST, typing, isolate, ST, epidemiology"
  metagenomics.upstream: "https://github.com/tseemann/mlst"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "full/scheme/info interface checked against current upstream README; not executed here"
---

# mlst

Upstream: [tseemann/mlst](https://github.com/tseemann/mlst) · schemes from
[PubMLST](https://pubmlst.org/)

## Citation

Seemann, T. mlst: scan contig files against PubMLST typing schemes.
https://github.com/tseemann/mlst

Jolley, K. A., Bray, J. E. & Maiden, M. C. J. Open-access bacterial population
genomics: BIGSdb software, the PubMLST.org website and their applications.
*Wellcome Open Res.* **3**, 124 (2018).
https://doi.org/10.12688/wellcomeopenres.14826.1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `pmlst`.

## Analytical thinking

Chromosomal **MLST** assigns a species-scheme sequence type from seven (or
scheme-defined) housekeeping loci. Auto-scheme detection can mis-assign on
novel/environmental genomes — verify species/`--scheme`. Novel alleles yield
incomplete STs.

**Not** plasmid typing (`pmlst`) and **not** ANI taxonomy (`gtdbtk` / `skani`).
Use with CGE Finders for One-Health isolate reports: species ST + resistome +
plasmids.

## How to run

Prefer an independently justified explicit scheme. If auto-detection is used,
retain the detected scheme and verify it against taxonomy.

```bash
set -Eeuo pipefail
assembly="${1:?usage: run-mlst.sh ASSEMBLY_FASTA OUTPUT_DIR}"
out="${2:?usage: run-mlst.sh ASSEMBLY_FASTA OUTPUT_DIR}"
test -s "$assembly" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
mlst --info >"$out/scheme-manifest.tsv"
scheme_args=()
if [[ -n "${MLST_SCHEME:-}" ]]; then
  scheme_args=(--scheme "$MLST_SCHEME")
fi
mlst --full "${scheme_args[@]}" "$assembly" >"$out/mlst.tsv" \
  2>"$out/mlst.stderr.log"
test -s "$out/mlst.tsv"
test -s "$out/scheme-manifest.tsv"
```

Freeze the `mlst` package and bundled PubMLST snapshot; do not update schemes
between cohort samples.

## Decision tree

```text
Sequence type needed?
├─ Chromosomal PubMLST ST → mlst
├─ Plasmid scheme ST → pmlst
├─ Species/taxonomy for MAGs → gtdbtk
└─ AMR / plasmids / virulence → cge-finders / abricate / rgi
```

## Validation, recovery, and provenance

Require full-format output, scheme manifest, logs, and one reconciled status per
assembly. Inspect forced/detected scheme, ST status, exact/approximate/missing or
multiple alleles, assembly fragmentation, locus coverage, contamination and
species consistency. Preserve novel allele sequences for review where needed;
do not convert incomplete/novel profiles into known STs.

Use fresh outputs after changing assemblies, schemes, databases, or release.
Record mlst/BLAST versions, scheme name/date and database checksums, assembly
checksum, command, raw output, logs, and interpretation rules. MLST is a typing
result for the selected scheme, not a general phylogeny or plasmid ST.

## Related skills

`pmlst` · `cge-finders` · `abricate` · `staramr` · `plasmidfinder` ·
`gtdbtk` · `microbial-mining` · `tool-selection`
