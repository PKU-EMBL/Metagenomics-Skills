---
name: unicore
description: >
  Unicore — universal structure-based core-gene phylogeny using Foldseek and ProstT5
  (Steinegger lab). Use when: (1) Building phylogenies from proteomes via structural
  core genes, (2) 3Di MSAs for tree inference, (3) Scaling beyond sequence-only marker
  sets. Route via phylogenomics; depends on foldseek (± GPU ProstT5).
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Unicore, Foldseek, ProstT5, phylogeny, core-genes, 3Di"
  metagenomics.upstream: "https://github.com/steineggerlab/unicore"
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "easy-core input/output and GPU interface checked against current upstream README; not executed here"
---

# Unicore

Upstream: [steineggerlab/unicore](https://github.com/steineggerlab/unicore)

## Citation

Kim, D., Park, S. & Steinegger, M. Unicore enables scalable and accurate
phylogenetic reconstruction with structural core genes. *Genome Biol. Evol.*
**17**, evaf109 (2025). https://doi.org/10.1093/gbe/evaf109

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Unicore finds **structural core genes** across proteomes (Foldseek clustering /
ProstT5 3Di) and builds phylogenies — a Steinegger-stack alternative/complement
to sequence-marker workflows (`phylophlan` + `iqtree`).

| vs | Prefer Unicore when |
|----|---------------------|
| `phylophlan` / `iqtree` | Want structure/3Di core genes |
| `gtdbtk` | Custom structural phylogeny, not only GTDB labels |
| `lucaphylo` | Proteome-scale core-gene trees vs single-protein PLM placement |

GPU: `--gpu` requires Foldseek≥10 / ProstT5 and a Turing-or-newer NVIDIA GPU; record model and device.

## How to run

Input must contain only one uniquely named `.fasta` proteome per taxon. Pin and
checksum ProstT5 weights before the run.

```bash
set -Eeuo pipefail
proteomes="${1:?usage: run-unicore.sh PROTEOME_DIR PROSTT5_MODEL OUTPUT_DIR}"
model="${2:?usage: run-unicore.sh PROTEOME_DIR PROSTT5_MODEL OUTPUT_DIR}"
out="${3:?usage: run-unicore.sh PROTEOME_DIR PROSTT5_MODEL OUTPUT_DIR}"
test -d "$proteomes" && test -e "$model" || exit 2
shopt -s nullglob
files=("$proteomes"/*.fasta)
((${#files[@]} >= 4)) || { echo "at least four proteomes are required" >&2; exit 2; }
if find "$proteomes" -maxdepth 1 -type f ! -name '*.fasta' -print -quit | grep -q .; then
  echo "proteome directory must contain only .fasta files" >&2; exit 2
fi
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
gpu_args=()
[[ "${UNICORE_GPU:-0}" = 1 ]] && gpu_args=(--gpu)
unicore easy-core "${gpu_args[@]}" "$proteomes" "$out/results" "$model" \
  "$out/tmp" >"$out/unicore.stdout.log" 2>"$out/unicore.stderr.log"
test -s "$out/results/cluster/clust.tsv"
test -s "$out/results/tree/iqtree.treefile"
```

The default core definition is single-copy presence in 80% of taxa. Any threshold,
Foldseek clustering, IQ-TREE or partition changes must be recorded.

## Decision tree

```text
Phylogeny from many proteomes/MAGs?
├─ GTDB taxonomy only → gtdbtk
├─ Sequence markers → phylophlan → iqtree
├─ Structural core genes / 3Di → unicore
└─ Single divergent protein family → lucaphylo / foldmason + iqtree
```

## Validation, recovery, and provenance

Require proteome parsing, cluster/core profiles, per-core AA/3Di alignments,
IQ-TREE artifacts, final tree, logs and taxon reconciliation. Inspect proteome
quality/size, duplicate IDs, core occupancy/copy number, missing data, structural
cluster sensitivity, alignment quality, gene-tree conflict, model/support,
outgroup/rooting and long branches. Compare pivotal topology with a classical
sequence-marker workflow.

Use fresh output after changing proteomes, model, thresholds, device, software or
options. Record Unicore/Foldseek/IQ-TREE versions, ProstT5 revision/checksum,
hardware, proteome checksums/QC, commands/logs, core tables/MSAs/tree checksums,
seed/model/support and rooting. A structural-core tree is computational evidence,
not taxonomy or a resolved history without diagnostics.

## Related skills

`phylogenomics` · `foldseek` · `foldmason` · `phylophlan` · `iqtree` ·
`gtdbtk` · `tool-selection`
