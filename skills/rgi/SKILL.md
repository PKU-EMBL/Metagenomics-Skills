---
name: rgi
description: >
  Antibiotic resistance gene annotation against CARD. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "AMR, CARD, resistance"
  metagenomics.upstream: "https://github.com/arpcard/rgi"
---

# RGI (CARD)

Upstream: [arpcard/rgi](https://github.com/arpcard/rgi) · CARD database

## Citation

Alcock, B. P. *et al.* CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database. *Nucleic Acids Res.* **51**, D690–D699 (2023). https://doi.org/10.1093/nar/gkac920

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

RGI predicts AMR genes from proteins or contigs against **CARD**. Hits are
sequence homology / model matches — **not phenotypic resistance**, expression,
or clinical breakpoints.

Prefer protein mode on NR or MAG proteomes. Intersect with `genomad`/`plasmaag`
when claiming plasmid-borne AMR. Optional ML/complement: `deeparg` (different
model — do not merge unlabeled). Isolate CGE screens: `resfinder` / `staramr`
(ResFinder DB — keep separate from CARD).

## How to run

```bash
# load CARD JSON per RGI docs, then:
rgi main -i proteins.faa -t protein -n 8 -a DIAMOND --clean \
  -o result/card/protein
```

## Key parameters

| Flag | Notes |
|------|-------|
| `-t protein` / contig | Protein preferred for catalogues |
| `-a DIAMOND` | Speed |
| CARD version | Pin with RGI version |

## Decision tree

```text
Resistome claim?
├─ Homology to CARD → rgi
├─ CGE ResFinder DB (isolates) → resfinder / staramr
├─ Chromosomal AMR SNPs → pointfinder
├─ ML complement → deeparg (separate table)
├─ On plasmids? → intersect genomad / plasmaag / plasmidfinder
└─ Phenotype → needs experiments / MICs (out of scope)
```

## Related skills

`deeparg` · `resfinder` · `pointfinder` · `staramr` · `cge-finders` ·
`genomad` · `plasmaag` · `plasmidfinder` · `eggnog-mapper` · `prodigal` ·
`microbial-mining` · `visualization` · `tool-selection`
