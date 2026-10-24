---
name: iqtree
description: >
  IQ-TREE 2 — fast maximum-likelihood phylogenetic inference with model selection and
  ultrafast bootstrap. Use when: (1) Building publication-grade trees from marker or
  concatenated MSAs, (2) Following PhyloPhlAn / custom alignments for MAG phylogenomics,
  (3) Replacing draft FastTree topologies for final figures.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "IQ-TREE, phylogeny, maximum-likelihood, tree, bootstrap"
  metagenomics.upstream: "https://github.com/iqtree/iqtree2"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "IQ-TREE 2 ModelFinder/UFBoot command template statically reviewed; not executed here"
---

# IQ-TREE 2

Upstream: [iqtree/iqtree2](https://github.com/iqtree/iqtree2)

## Citation

Minh, B. Q. *et al.* IQ-TREE 2: new models and efficient methods for phylogenetic
inference in the genomic era. *Mol. Biol. Evol.* **37**, 1530–1534 (2020).
https://doi.org/10.1093/molbev/msaa015

Nguyen, L.-T., Schmidt, H. A., von Haeseler, A. & Minh, B. Q. IQ-TREE: a fast
and effective stochastic algorithm for estimating maximum-likelihood phylogenies.
*Mol. Biol. Evol.* **32**, 268–274 (2015). https://doi.org/10.1093/molbev/msu300

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Default **ML tree** engine for metagenomic phylogenomics after you have a
clean MSA (from `phylophlan`, marker genes, or curated orthologs). ModelFinder
chooses substitution models; UFBoot gives rapid support values — report both
model and support method.

| vs | Prefer IQ-TREE when |
|----|---------------------|
| `fasttree` | Final / publication trees |
| `gtdbtk` | You need a custom tree, not only GTDB placement |
| `lucaphylo` | MSA-based classical phylogeny is appropriate |

Garbage in → garbage trees: remove poor MAGs, dubious alignments, and
outgroup contamination first.

## How to run

The MSA must be curated before inference. This unpartitioned template fixes a
seed and writes every artifact under a fresh prefix.

```bash
set -Eeuo pipefail
msa="${1:?usage: run-iqtree.sh ALIGNMENT OUTPUT_DIR}"
out="${2:?usage: run-iqtree.sh ALIGNMENT OUTPUT_DIR}"
threads="${THREADS:-AUTO}"
seed="${IQTREE_SEED:-1729}"
test -s "$msa" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

iqtree2 -s "$msa" -m MFP -B 1000 -T "$threads" -seed "$seed" \
  --prefix "$out/run" >"$out/iqtree.stdout.log" \
  2>"$out/iqtree.stderr.log"
test -s "$out/run.treefile"
test -s "$out/run.iqtree"
test -s "$out/run.log"
grep -q 'BEST SCORE FOUND' "$out/run.log"
```

For concatenated markers, supply and archive an explicit partition file and use
the justified partition/merge model rather than treating all sites as one locus.

## Key parameters

| Setting | Notes |
|---------|-------|
| `-m MFP` | ModelFinder Plus — state selected model |
| `-B 1000` | Ultrafast bootstrap replicates |
| `-T` | Threads |
| Partition models | Use when concatenating heterogeneous markers |

## Decision tree

```text
Need a sequence-based tree?
├─ Draft / exploratory large MSA → fasttree
├─ Publication ML tree → iqtree
├─ Genome set workflow → phylophlan (± iqtree backend)
└─ MSA impossible / extreme divergence → lucaphylo
```

## Validation, recovery, and provenance

Require a parseable tree, report/log, selected model, likelihood, support values,
alignment/taxon reconciliation, and convergence/warning review. Inspect marker
occupancy, duplicate IDs, composition/model fit, outgroup, long branches,
partition sensitivity, UFBoot stability, topology conflict, and rooting. Support
does not validate orthology, absence of recombination, or a causal history.

IQ-TREE can checkpoint a byte-identical run; resume only with unchanged input,
prefix, binary and options. Otherwise preserve it and use a fresh directory.
Record IQ-TREE version, MSA/partition checksums and preparation, seed, model
search/support settings, command, all logs/reports/checkpoints, unrooted tree,
rooting/annotation steps, and final checksums.

## Related skills

`phylogenomics` · `fasttree` · `phylophlan` · `gtdbtk` · `lucaphylo` ·
`mag-qc` · `tool-selection`
