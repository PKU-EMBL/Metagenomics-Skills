---
name: comebin
description: >
  COMEBin — contrastive multi-view representation learning for metagenomic contig
  binning (composition + coverage). Use when: (1) Running COMEBin as a modern single
  binner, (2) Comparing to SemiBin2/VAMB/MetaBAT2, (3) Co- assembly, single-sample, or
  multi-sample binning modes, (4) Feeding bins into ensemble refinement. Prefer ensemble
  (basalt ★ / metawrap / dastool) for catalogues.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, COMEBin, contrastive-learning, MAG"
  metagenomics.upstream: "https://github.com/ziyewang/COMEBin"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot 1b476a4"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# COMEBin

Upstream: [ziyewang/COMEBin](https://github.com/ziyewang/COMEBin)

## Citation

Wang, Z. *et al.* Effective binning of metagenomic contigs using contrastive
multi-view representation learning. *Nat. Commun.* **15**, 585 (2024).
https://doi.org/10.1038/s41467-023-44290-z

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

COMEBin learns contig embeddings with **contrastive multi-view** learning:
data augmentation creates multiple views per contig; a coverage module maps
variable sample counts to fixed-dimensional coverage embeddings. Benchmarks
(CAMI II and real data) show strong near-complete MAG recovery without
SemiBin1-style taxonomic semi-supervision.

Use as a **diverse single-binner** in ensembles (different inductive bias from
MetaBAT2 / MaxBin2 / VAMB). Prefer multi-coverage inputs when related samples
exist (Mattock & Watson 2023 — single-coverage hides contamination).

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Contigs | Assembly FASTA |
| Coverage | Multi-sample BAM/abundance when available |
| QC | `checkm2` after binning |

## How to run

```bash
set -euo pipefail
[[ -s contigs.fa && -d temp/map ]] || exit 2
find temp/map -maxdepth 1 -name '*.bam' -size +0c | grep -q .
command -v run_comebin.sh >/dev/null
run_comebin.sh -a "$(realpath contigs.fa)" \
  -o "$(realpath -m temp/bins/comebin)" \
  -p "$(realpath temp/map)" -d cuda -t 32 \
  >comebin.stdout.log 2>comebin.stderr.log
```

Use `-d cpu` when no compatible CUDA device is available. BAMs must be coordinate-sorted, indexed, and aligned to the exact assembly; inspect `run_comebin.sh -h` in the pinned release before changing modes.

## Decision tree

```text
Single binner choice?
├─ Classical TNF+coverage → metabat2 / concoct / maxbin2
├─ VAE latent → vamb
├─ Self-supervised contrastive → semibin2
├─ Multi-view contrastive → comebin
└─ Catalogue / multi-assembly → basalt ★ (ensemble)
```

## Methods caveats

- Contrastive gains are benchmark-specific; always QC with CheckM2/GUNC.
- Report mode (co-assembly / single / multi-sample) and coverage recipe.
- Combine with ensemble tools rather than publishing one binner’s raw dump.

## Validation, recovery, and provenance

Require completed logs, candidate FASTAs/assignment tables, exact contig membership and no duplicate final assignments. Reconcile all BAM reference headers/lengths to the assembly, summarize binned/unbinned bases, and evaluate bins with CheckM2/GUNC under the same policy used for comparator binners. GPU completion alone is not a quality result.

Use a fresh output after changing assembly, BAM set, device or release. Record COMEBin/PyTorch/CUDA commit and versions, command, assembly/BAM checksums, ordered sample mapping, minimum contig policy, device/seed where exposed, assignments and candidate checksums. Bins remain candidates until independent QC/refinement.

## Related skills

`semibin2` · `vamb` · `metabat2` · `basalt` · `dastool` · `checkm2` ·
`tool-selection` · `metagenomics-workflow`
