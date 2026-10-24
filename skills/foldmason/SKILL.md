---
name: foldmason
description: >
  FoldMason — multiple protein structure alignment at scale (Steinegger lab). Use when:
  (1) Building structural MSAs from AFDB / predicted models, (2) Comparing folds across
  MAG protein families after Foldseek clustering, (3) Preparing structure-aware
  alignments for phylogeny or motif work.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "FoldMason, structure-MSA, Foldseek, alignment"
  metagenomics.upstream: "https://github.com/steineggerlab/foldmason"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "easy-msa outputs and report mode checked against current upstream README; not executed here"
---

# FoldMason

Upstream: [steineggerlab/foldmason](https://github.com/steineggerlab/foldmason) ·
Web: https://search.foldseek.com/foldmason

## Citation

Gilchrist, C. L. M., Mirdita, M. & Steinegger, M. Multiple protein structure
alignment at scale with FoldMason. *Science* **391**, 485–488 (2026).
https://doi.org/10.1126/science.ads6733

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Foldseek finds pairwise structural neighbors; **FoldMason** builds scalable
**multiple** structure alignments (FASTA + HTML reports). Useful after
clustering dark proteins or AFDB hits into families.

| vs | Prefer FoldMason when |
|----|------------------------|
| `foldseek` | Need MSA of many structures, not just hit table |
| Sequence MSA (MAFFT/…) | Structures available / twilight zone |
| `folddisco` | Global structural MSA vs local motif |

## How to run

Use a curated directory of homologous PDB/mmCIF structures with unique IDs; avoid
an unordered shell glob that can omit compressed files or exceed argument limits.

```bash
set -Eeuo pipefail
structures="${1:?usage: run-foldmason.sh STRUCTURE_DIR OUTPUT_DIR}"
out="${2:?usage: run-foldmason.sh STRUCTURE_DIR OUTPUT_DIR}"
threads="${THREADS:-8}"
test -d "$structures" || exit 2
find "$structures" -maxdepth 1 -type f \( -name '*.pdb' -o -name '*.cif' -o \
  -name '*.pdb.gz' -o -name '*.cif.gz' \) -print -quit | grep -q . || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
foldmason easy-msa "$structures" "$out/result" "$out/tmp" \
  --report-mode 1 --threads "$threads" \
  >"$out/foldmason.stdout.log" 2>"$out/foldmason.stderr.log"
test -s "$out/result_aa.fa"
test -s "$out/result_3di.fa"
test -s "$out/result.nw"
test -s "$out/result.html"
```

For large sets, evaluate `--precluster`; for refined alignments, record
`--refine-iters`. These choices change which structures and columns drive the MSA.

## Decision tree

```text
Have a set of related structures?
├─ Pairwise search only → foldseek
├─ Multiple structure alignment → foldmason
├─ Short motif → folddisco
└─ Sequence MSA → hh-suite / classical aligners
```

## Validation, recovery, and provenance

Require AA/3Di MSAs, guide tree, HTML report, logs, and one reconciled row per
input structure. Inspect exclusions, duplicate IDs, chain choice, sequence/3Di
lengths, gap/occupancy patterns, LDDT, outliers, preclustering/refinement effects,
and low-confidence coordinates. The guide tree is an alignment aid unless
independently justified as phylogeny.

Use fresh output after changing structures, options, or binary. Record FoldMason
and Foldseek versions/builds, structure sources/checksums and confidence policy,
input manifest, command/logs, settings, MSA/tree checksums, and exclusions.
Structural alignment supports shared geometry, not identical function or history.

## Related skills

`foldseek` · `folddisco` · `foldcomp` · `unicore` · `homology-search` ·
`phylogenomics` · `tool-selection`
