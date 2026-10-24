---
name: fasttree
description: >
  FastTree — approximately-maximum-likelihood trees for large alignments. Use when: (1)
  Draft phylogenies from big MSAs, (2) Quick topology screens before IQ-TREE, (3)
  Resource-limited exploratory MAG trees. For final ML trees prefer iqtree.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "FastTree, phylogeny, approximate-ML, tree"
  metagenomics.upstream: "https://github.com/morgannprice/fasttree"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "protein/nucleotide FastTreeMP command templates statically reviewed; not executed here"
---

# FastTree

Upstream: [morgannprice/fasttree](https://github.com/morgannprice/fasttree) ·
often packaged as `fasttree` / `FastTreeMP` (bioconda)

## Citation

Price, M. N., Dehal, P. S. & Arkin, A. P. FastTree: computing large minimum
evolution trees with profiles instead of a distance matrix. *Mol. Biol. Evol.*
**26**, 1641–1650 (2009). https://doi.org/10.1093/molbev/msp077

Price, M. N., Dehal, P. S. & Arkin, A. P. FastTree 2 — approximately
maximum-likelihood trees for large alignments. *PLoS ONE* **5**, e9490 (2010).
https://doi.org/10.1371/journal.pone.0009490

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FastTree trades some accuracy for **speed on large MSAs** — ideal for
exploratory MAG/marker trees and PhyloPhlAn-scale drafts. For manuscript
figures and formal support values, re-infer with `iqtree`.

| vs | Prefer FastTree when |
|----|----------------------|
| `iqtree` | Huge MSA / quick topology / limited CPU |
| Distance-only trees | You still want approximate ML |

Always state FastTree vs IQ-TREE in Methods if both appear.

## How to run

The input must already be a curated multiple-sequence alignment with unique IDs.
Choose `protein` or `nucleotide` explicitly.

```bash
set -Eeuo pipefail
msa="${1:?usage: run-fasttree.sh ALIGNMENT OUTPUT_DIR}"
out="${2:?usage: run-fasttree.sh ALIGNMENT OUTPUT_DIR}"
datatype="${FASTTREE_DATATYPE:-protein}"
test -s "$msa" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"
case "$datatype" in
  protein) model_args=(-lg) ;;
  nucleotide) model_args=(-gtr -nt) ;;
  *) echo "FASTTREE_DATATYPE must be protein or nucleotide" >&2; exit 2 ;;
esac
FastTreeMP "${model_args[@]}" "$msa" >"$out/tree.nwk" \
  2>"$out/fasttree.stderr.log"
test -s "$out/tree.nwk"
grep -q '[();]' "$out/tree.nwk"
```

The nucleotide template uses GTR; the protein template uses LG. Any gamma,
CAT, pseudocount, constraint, or support changes must be predeclared.

## Decision tree

```text
Tree speed vs rigor?
├─ Screen / huge alignment → fasttree
├─ Final ML + UFBoot → iqtree
└─ Full MAG phylogenomics workflow → phylophlan
```

## Validation, recovery, and provenance

Require a parseable Newick tree, stderr progress log, one leaf per intended
alignment ID, branch lengths, and an inclusion/exclusion audit. Inspect duplicate
IDs, alignment occupancy, outgroup/rooting, extreme branches, unresolved nodes,
model appropriateness, and topology sensitivity to filtering. FastTree support
values are not conventional bootstrap replicates; label them correctly.

Use a fresh output after changing MSA, model, binary, or options. Record FastTree
binary/version (including precision/OpenMP build), alignment checksum and
construction/trimming, datatype/model/options, command, log, unrooted tree
checksum, rooting/annotation script, and final tree checksum. Upgrade key final
claims to IQ-TREE or justify the approximate analysis.

## Related skills

`phylogenomics` · `iqtree` · `phylophlan` · `gtdbtk` · `mag-qc` ·
`tool-selection`
