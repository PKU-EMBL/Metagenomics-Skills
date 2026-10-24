---
name: quast
description: >
  Assembly quality assessment (contiguity, misassemblies; metaQUAST for metagenomes).
  Use for installation, parameter choice, execution, output interpretation, or
  troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "assembly, qc, quast"
  metagenomics.upstream: "https://github.com/ablab/quast"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "QUAST/metaQUAST CLI template statically reviewed; not executed here"
---

# QUAST / metaQUAST

Upstream: [QUAST / metaQUAST](https://github.com/ablab/quast)

## Citation

Mikheenko, A., Saveliev, V. & Gurevich, A. MetaQUAST: evaluation of metagenome assemblies. *Bioinformatics* **32**, 1088–1090 (2016). https://doi.org/10.1093/bioinformatics/btv697

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Run after assembly **before** heavy binning to catch overly fragmented graphs.
metaQUAST adds reference-based misassembly metrics when suitable genomes exist;
without refs you still get contiguity stats (N50, length histograms).

Contiguity ≠ biological correctness. Do **not** choose assemblers on N50 alone —
combine with mapping rate, bin recovery (`mag-qc`), and compute cost.

## How to run

Use `metaquast.py` when its metagenome/reference logic is needed; use `quast.py`
for reference-free contiguity summaries.

```bash
set -Eeuo pipefail
assembly="${1:?usage: assess-assembly.sh ASSEMBLY_FASTA OUTPUT_DIR}"
out="${2:?usage: assess-assembly.sh ASSEMBLY_FASTA OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$assembly" || exit 2
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$(dirname "$out")" logs

metaquast.py "$assembly" -o "$out" -t "$threads" \
  >"logs/$(basename "$out").metaquast.stdout.log" \
  2>"logs/$(basename "$out").metaquast.stderr.log"
```

For a valid curated reference set, add the release-pinned reference option shown
by the installed version's help and preserve the reference manifest/checksums.

## Key parameters

| Mode | When |
|------|------|
| `metaquast.py` | Metagenomes; optional reference set |
| `quast.py` | Quick contiguity without refs |
| Threads `-t` | Scale with CPU |

## Decision tree

```text
Assembly assessment?
├─ Have references → metaQUAST
├─ No refs → QUAST stats + downstream bin QC
└─ CAMI gold standards → cami / AMBER (not QUAST alone)
```

## Validation, recovery, and provenance

```bash
test -s "$out/report.tsv"
test -s "$out/report.html"
grep -q '^Assembly' "$out/report.tsv"
```

Inspect warnings, total span, contig counts at declared cutoffs, N50/L50 and
largest contig together, ambiguous bases, and reference-based errors only when
the reference set is biologically appropriate. Compare assemblers on downstream
read recruitment and genome/bin recovery, not N50 alone.

QUAST output directories contain intermediate and downloaded material; do not
merge reruns into them. Record QUAST version, mode, thresholds, references and
checksums, input checksum, command, logs, and machine-readable reports.

## Related skills

`megahit` · `metaspades` · `metaflye` · `metamdbg` · `mag-qc` · `cami` ·
`tool-selection`
