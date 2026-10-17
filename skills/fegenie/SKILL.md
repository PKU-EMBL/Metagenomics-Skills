---
name: fegenie
description: >
  FeGenie — HMM-based identification of iron-related genes and neighborhoods in
  genomes/metagenome assemblies (acquisition, siderophores, Fe redox, storage,
  magnetosome). Use for Fe cycling potential on contigs or MAGs. Broader C/N/S →
  metabolic; S scores → mebs.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "FeGenie, iron, Fe, siderophore, biogeochemistry, element-cycling"
  metagenomics.upstream: "https://github.com/Arkadiy-Garber/FeGenie"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot 8efc74c"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# FeGenie

Upstream: [Arkadiy-Garber/FeGenie](https://github.com/Arkadiy-Garber/FeGenie)

## Citation

Garber, A. I. *et al.* FeGenie: A Comprehensive Tool for the Identification of
Iron Genes and Iron Gene Neighborhoods in Genome and Metagenome Assemblies.
*Front. Microbiol.* **11**, 37 (2020).
https://doi.org/10.3389/fmicb.2020.00037

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

FeGenie targets **iron**: transport/acquisition, **siderophores**, oxidation /
dissimilatory reduction, storage, magnetosome-related genes, and neighborhoods.
Complements generic KO annotation that often misses Fe redox markers.

| vs | Prefer FeGenie when |
|----|---------------------|
| `metabolic` / `dram` | Fe-specific gene families and operon context |
| `mebs` | Explicit Fe gene calls vs cycle entropy scores |
| `antismash` | Siderophore BGC context vs FeGenie HMM categories |

Hits ≠ demonstrated Fe flux or siderophore production.

## Inputs and run

Input is a directory of nucleotide assemblies/genomes sharing one extension, or predicted proteins with `--orfs`. IDs must be unique and bins should carry quality metadata.

```bash
set -euo pipefail
[[ -d bins ]] || exit 2
find bins -maxdepth 1 -name '*.fna' -size +0c | grep -q .
: "${iron_hmms:?set iron_hmms to the pinned FeGenie HMM directory}"
: "${rscripts:?set rscripts to the pinned FeGenie R scripts directory}"
FeGenie.py -h >/dev/null
FeGenie.py -bin_dir bins -bin_ext fna -out result/fegenie -t 16 \
  >fegenie.stdout.log 2>fegenie.stderr.log
```

For existing proteins, use a separate output and `-bin_ext faa --orfs`; add `-ref REF.faa` only for the documented cross-validation route.

## Decision tree

```text
Iron / siderophore genetic potential?
├─ Yes → fegenie
├─ Multi-element C/N/S diagrams → metabolic
├─ S/N/CH₄/Fe scores → mebs
└─ Broad distillate → dram
```

## Validation, recovery, and provenance

Require non-empty `FeGenie-geneSummary-clusters.csv`, completed logs and per-input accounting. Reconcile each hit to genome, contig, protein coordinates, HMM/category and neighborhood; inspect cutoffs, ambiguous redox families, short/truncated genes and conflicting generic annotations. Normalize community summaries only with a declared denominator and keep gene-level tables.

Use a fresh output after changing gene calls, HMMs or reference. Record FeGenie commit, HMM-directory hash, Prodigal/HMMER/DIAMOND versions, command, input/checksum manifest, MAG quality, result checksum and filters. Gene/neighborhood evidence indicates iron-related potential, not reaction direction, expression or flux.

## Related skills

`element-cycling` · `metabolic` · `mebs` · `dram` · `antismash` ·
`microbial-mining` · `tool-selection`
