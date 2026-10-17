---
name: lorbin
description: >
  LorBin — unsupervised long-read metagenome binning with multiscale adaptive clustering
  (DBSCAN + BIRCH) and single-copy-gene evaluation. Use when: (1) Binning long-read /
  HiFi metagenome assemblies, (2) Recovering MAGs from species-rich or
  abundance-imbalanced communities, (3) Comparing LorBin to SemiBin2/VAMB long-read
  modes, (4) Feeding LorBin bins into ensemble refinement (BASALT `-e l` needs the
  PKU-EMBL LorBin fork). For ensemble recovery use basalt. For short-read defaults use
  metabat2 / semibin2 / vamb.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, long-read, LorBin, MAG, DBSCAN"
  metagenomics.upstream: "https://github.com/LorMeBioAI/LorBin"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot ee10232"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# LorBin

Upstream: [LorMeBioAI/LorBin](https://github.com/LorMeBioAI/LorBin)

## Citation

Xue, W. *et al.* LorBin: efficient binning of long-read metagenomes by
multiscale adaptive clustering and evaluation. *Nat. Commun.* **16**, 9353
(2025). https://doi.org/10.1038/s41467-025-64916-8

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Long-read assemblies differ from short-read graphs: fewer, longer contigs,
sharper abundance separation, and often **unknown / imbalanced** taxa. Short-read
binners (and some DL tools trained mainly on short-read CAMI) under-recover
novel lineages in that regime.

LorBin is an **unsupervised** long-read binner: multiscale adaptive DBSCAN then
BIRCH, with iterative single-copy-gene evaluation to accept/recluster bins. The
paper reports large gains in high-quality MAGs and novel taxa vs several
competitors on oral, gut, and marine long-read sets — treat those as
**benchmark-conditioned**, not universal guarantees.

Within this package:

| Role | Skill |
|------|--------|
| Long-read single binner | `lorbin` (or SemiBin2 long-read mode) |
| Short-read single binners | `metabat2` · `semibin2` · `vamb` · `comebin` |
| Ensemble refinement | `basalt` ★ · `metawrap` · `dastool` |

If using **BASALT** with LorBin as an extra binner (`-e l`), use the
**PKU-EMBL LorBin fork commit** documented in the BASALT guide — not an
arbitrary upstream tip.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Assembly | Long-read / hybrid contigs (metaFlye, metaMDBG, …) |
| Coverage | BAM or abundance table as required by upstream CLI |
| QC | Always follow with `checkm2` (+ `gunc` for chimera risk) |

## How to run

Map each long-read sample to the exact concatenated contig FASTA, then provide sorted BAMs. The installed entry point is case-sensitive (`LorBin`).

```bash
set -euo pipefail
[[ -s long_contigs.fa && -s sample1.sorted.bam ]] || exit 2
samtools quickcheck -v sample1.sorted.bam
LorBin --help >/dev/null
LorBin bin -o temp/bins/lorbin -fa long_contigs.fa \
  -b sample1.sorted.bam --num_process 16 \
  >lorbin.stdout.log 2>lorbin.stderr.log
```

For multiple related samples, list all BAMs after `-b` and add `--multi`. Do not use multi-sample mode across unrelated strata.

## Decision tree

```text
Long-read MAG recovery?
├─ Dedicated long-read binner → lorbin
├─ SemiBin2 long-read / ensemble-DBSCAN path → semibin2
├─ Multi-binner + refinement (related samples) → basalt ★
└─ Only short reads → prefer metabat2 / semibin2 / vamb (+ ensemble)
```

## Methods caveats

- Unsupervised clustering + SCG gates ≠ experimental species proof.
- Report assembler, read type (ONT/HiFi), LorBin version, and CheckM2 gates.
- Do not claim “novel phylum” from LorBin alone — require GTDB-Tk + literature
  placement and chimera screens (`gunc`).

## Validation, recovery, and provenance

Require completed logs, non-empty candidate bins/assignments, exact BAM/FASTA header agreement and unique final contig membership. Summarize binned/unbinned bases and evaluate candidates with CheckM2/GUNC; compare marker and no-marker evaluation modes only as a declared sensitivity analysis.

Use a new output after changing assembly, BAMs, `--multi`, evaluation model or reclustering threshold. Record LorBin commit/environment, command, input checksums, sample order, mapping parameters, model/evaluation mode, thresholds, logs and candidate checksums. A learned cluster is not a validated genome.

## Related skills

`metaflye` · `metamdbg` · `semibin2` · `vamb` · `basalt` · `checkm2` · `gunc` ·
`tool-selection` · `metagenomics-workflow`
