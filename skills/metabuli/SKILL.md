---
name: metabuli
description: >
  Metabuli — metagenomic taxonomic classification via joint DNA + amino-acid (metamer)
  analysis for sensitive homology and specific close-taxon resolution. Use when: (1)
  Choosing a classifier beyond DNA-only (Kraken2) or AA-only (Kaiju), (2) Profiling
  understudied clades where DNA k-mers fail, (3) CAMI- style or plant/environment
  datasets needing both sensitivity and specificity, (4) Writing Methods for joint
  DNA/AA classification. Complementary to metaphlan / kraken2 / kaiju — do not merge
  tables unlabeled.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, Metabuli, DNA, amino-acid, classification"
  metagenomics.upstream: "https://github.com/steineggerlab/Metabuli"
  metagenomics.stage: "taxonomy"
---

# Metabuli

Upstream: [steineggerlab/Metabuli](https://github.com/steineggerlab/Metabuli) ·
https://metabuli.steineggerlab.com

## Citation

Kim, J. & Steinegger, M. Metabuli: sensitive and specific metagenomic
classification via joint analysis of amino acid and DNA. *Nat. Methods* **21**,
971–973 (2024). https://doi.org/10.1038/s41592-024-02273-y

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classical dilemma:

| Signal | Strength | Weakness |
|--------|----------|----------|
| DNA k-mers (Kraken-like) | Distinguishes close, well-studied taxa | Misses remote homology |
| AA / 6-frame (Kaiju-like) | Sensitive to understudied clades | Weaker close-species separation |

Metabuli jointly analyzes DNA and AA via **metamers**, aiming to keep both
sensitivity and specificity. In CAMI2 plant-associated benchmarks it recovered
nearly all classifications of strong DNA- and AA-only tools.

Still database-bound: unclassified reads ≠ empty community. Prefer MetaPhlAn
when you need **clade-specific marker** abundances for pathways (HUMAnN); prefer
Metabuli/Kraken/Kaiju when you need read-level classification against large
nucleotide/protein DBs.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| DB | Metabuli database matching software version |
| RAM / disk | Large DBs — plan like Kraken-scale resources |
| Input | Preferably host-depleted FASTQ |

## How to run

```bash
# verify subcommands against upstream docs
metabuli classify \
  $METABULI_DB \
  temp/hr/${id}_1.fastq temp/hr/${id}_2.fastq \
  temp/metabuli/${id} \
  --threads 16
```

## Decision tree

```text
Taxonomic classification goal?
├─ Marker-gene relative abundance → metaphlan / motus
├─ Fast DNA k-mer + Bracken abundance → kraken2 + bracken
├─ Protein-level sensitivity → kaiju
├─ Joint DNA+AA (sensitivity + specificity) → metabuli
└─ Sketch containment / ANI-aware presence → sylph
```

## Methods caveats

- Do not average Metabuli with MetaPhlAn/Kraken without labeling method.
- Pin Metabuli + DB release; report paired-end mode and filters.
- Species labels for novel lineages remain reference-dependent.

## Related skills

`kraken2` · `bracken` · `kaiju` · `metaphlan` · `sylph` · `motus` ·
`tool-selection` · `metagenomics-workflow`
