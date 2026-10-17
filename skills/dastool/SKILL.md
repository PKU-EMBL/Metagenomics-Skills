---
name: dastool
description: >
  DAS Tool (Dereplication, Aggregation and Scoring) integrates multiple binning
  predictions into one non-redundant MAG set for a single assembly. Use this skill when
  working with DAS_Tool: preparing contig2bin tables, choosing score thresholds,
  comparing ensemble binning options, or writing Methods. For suite-style MetaBAT/MaxBin
  refinement use metawrap. For recommended multi-assembly refined recovery use basalt.
  For routing, use tool-selection.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "MAG, ensemble-binning, DAS_Tool, refinement"
  metagenomics.upstream: "https://github.com/cmks/DAS_Tool"
---

# DAS Tool

Upstream: [cmks/DAS_Tool](https://github.com/cmks/DAS_Tool)

## Citation

Sieber, C. M. K. *et al.* Recovery of genomes from metagenomes via a
dereplication, aggregation and scoring strategy. *Nat. Microbiol.* **3**,
836–843 (2018). https://doi.org/10.1038/s41564-018-0171-1

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

DAS Tool sits in the **ensemble binning** family with MetaWRAP and BASALT:
run several independent binners (MetaBAT2, MaxBin2, CONCOCT, …) on the **same
assembly**, then select an optimized non-redundant set.

DAS Tool scores candidates with **single-copy marker genes** and aggregates
across binning predictions. It does **not** invent new contig membership from
cross-assembly connectivity or deep learning — that is BASALT’s role.

Choose DAS Tool when you already have multiple contig2bin tables and want a
lightweight, classical consensus. Prefer **`basalt`** as the default ensemble
route for related samples / multi-assembly work; use **`metawrap`** when you
want a packaged binning + CheckM-style refinement suite.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Assembly FASTA + ≥2 contig2bin TSVs | MetaBAT2 + MaxBin2 (+ CONCOCT) |
| Search engine | DIAMOND / BLAST+ / USEARCH | DIAMOND (large datasets) |
| Threads | 1 | 8–16 |

## How to run

```bash
conda install -c bioconda das_tool

# Convert FASTA bins → contig2bin if needed
Fasta_to_Contigs2Bin.sh -i metabat2_bins -e fa > metabat2.contigs2bin.tsv
Fasta_to_Contigs2Bin.sh -i maxbin2_bins -e fasta > maxbin2.contigs2bin.tsv

DAS_Tool \
  -i metabat2.contigs2bin.tsv,maxbin2.contigs2bin.tsv \
  -l metabat,maxbin \
  -c contigs.fa \
  -o temp/dastool/run1 \
  -t 8 \
  --write_bins \
  --write_bin_evals \
  --search_engine diamond
```

## Key parameters

| Parameter | Typical | Notes |
|-----------|---------|-------|
| `-i` | comma-separated contig2bin TSVs | Tab: contig_id\<TAB\>bin_id |
| `-l` | labels matching `-i` order | Human-readable binner names |
| `-c` | assembly FASTA | Same contigs used for binning |
| `--score_threshold` | 0.5 default | Higher → fewer, stricter bins |
| `--write_bins` | on for MAG export | Writes FASTA bins |
| `-p` | optional proteins | Skip Prodigal if reused |

## Output

```text
*_DASTool_summary.tsv
*_DASTool_contigs2bin.tsv
DASTool_bins/          # if --write_bins
*_allBins.eval         # if --write_bin_evals
```

## Decision tree

```text
Ensemble MAG recovery?
├─ Recommended default (related samples / multi-assembly) → basalt
├─ Packaged multi-binner + CheckM refinement suite → metawrap
└─ Classical SCG aggregation of existing contig2bin sets → dastool
```


## Literature notes (Nat. Microbiol. 2018)

Sieber *et al.* motivate DAS Tool with observations still true operationally:

- **No single binner wins on all ecosystems**; tools reconstruct different genomes
  at different completeness — combining predictions recovers more near-complete
  genomes than any single method.
- Early work showed manual/curated multi-binner merges help; naive automation can
  reduce contamination **and** completeness — DAS Tool’s SCG scoring aims for an
  optimized non-redundant set from one assembly.
- Input is **contig2bin tables on one assembly**, not cross-assembly DL refinement
  (contrast `basalt`).

Practical rule from the paper’s logic: diversify binners (MetaBAT2 + MaxBin2 +
CONCOCT/SemiBin2/VAMB/COMEBin), then aggregate — do not run DAS Tool on a
single contig2bin table expecting magic.

## Related skills

`metawrap` · `basalt` · `megahit` · `metaspades` · `checkm2` · `drep` · `mag-qc` · `tool-selection`
