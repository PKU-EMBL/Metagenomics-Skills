---
name: mebs
description: >
  MEBS (Multigenomic Entropy-Based Score) — score genomes/metagenomes for biogeochemical
  cycle machinery via informative Pfam domains; strongest for sulfur (S), also supports
  N, O, CH4, and Fe cycle scores. Use for comparative cycle enrichment across large
  (meta)genome collections. Gene-level Fe → fegenie; multi-element diagrams → metabolic.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MEBS, sulfur, S, N, CH4, Fe, biogeochemistry, element-cycling"
  metagenomics.upstream: "https://github.com/valdeanda/mebs"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.upstream-version: "MEBS 1.2; snapshot c385984"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Perl and visualization CLIs reviewed against v1.2 manual; not executed here"
---

# MEBS

Upstream: [valdeanda/mebs](https://github.com/valdeanda/mebs) ·
legacy/core: https://github.com/eead-csic-compbio/metagenome_Pfam_score

## Citation

De Anda, V. *et al.* MEBS, a software platform to evaluate large (meta)genomic
collections according to their metabolic machinery: unraveling the sulfur cycle.
*Gigascience* **6**, 1–17 (2017).
https://doi.org/10.1093/gigascience/gix096

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

MEBS compresses curated cycle machinery into **relative-entropy scores** over
Pfam domains. Benchmarked deeply on the **sulfur (S)** cycle; documentation
also supports **N**, **O**, **CH₄**, and **Fe** scoring modes. Ideal for
ranking many genomes/metagenomes by cycle “machinery presence,” not for
drawing full METABOLIC-style pathway cartoons.

| vs | Prefer MEBS when |
|----|------------------|
| `metabolic` | Comparative S/N/CH₄/Fe scores across large collections |
| `fegenie` | Score-level Fe vs explicit Fe gene neighborhoods |
| `dram` | Cycle enrichment metric vs distilled product tables |

Input: directory of `.faa` peptide FASTA; use genomic vs metagenomic mode per
docs (fragmentary metagenomes need the metagenomic entropy tables).

## Inputs and run

Provide a directory of non-empty `.faa` files. Choose `genomic` for genomes/MAGs and `metagenomic` for fragmentary community protein sets; MEBS must run from its pinned checkout because `mebs.pl` resolves bundled files relative to the working directory.

```bash
set -euo pipefail
root=${MEBS_ROOT:?set MEBS_ROOT to the pinned MEBS 1.2 checkout}
proteins=$(realpath proteins)
out=$(realpath -m result/mebs)
find "$proteins" -maxdepth 1 -name '*.faa' -size +0c | grep -q .
mkdir -p "$out"
(
  cd "$root"
  perl mebs.pl -input "$proteins" -type genomic -comp \
    >"$out/scores.tsv" 2>"$out/mebs.stderr.log"
  python3 mebs_vis.py "$out/scores.tsv" -o "$out/visual"
)
test -s "$out/scores.tsv"
```

## Decision tree

```text
Cycle scoring need?
├─ S (or N/O/CH₄/Fe) entropy scores → mebs
├─ C/N/S diagrams + networks → metabolic
├─ Fe gene calls → fegenie
└─ Broad distillate → dram
```

## Validation, recovery, and provenance

Require one score/completeness row per input or an explicit failure, finite cycle scores and completed HMMER/visualization logs. Inspect the genomic/metagenomic mode, FDR, completeness markers and score distributions; sulfur has the strongest original benchmark, so do not imply equal validation for every cycle. Keep Pfam hit evidence behind aggregate entropy scores.

Use a fresh output after changing proteins, Pfam/MEBS assets or options. Record MEBS commit/version, bundled model/table hashes, HMMER/Python/R dependencies, command, input/checksum manifest, mode/FDR/completeness options and output checksums. Entropy scores rank encoded machinery; they do not measure pathway completeness, expression or elemental flux.

## Related skills

`element-cycling` · `metabolic` · `fegenie` · `dram` · `microbial-mining` ·
`tool-selection`
