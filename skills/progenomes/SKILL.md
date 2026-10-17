---
name: progenomes
description: >
  proGenomes4 — nearly 2 million consistently QC'd and annotated high-quality
  prokaryotic genomes with habitat metadata, pan-genomes, MGE/BGC annotations. Use when:
  (1) Building large microbial genome reference sets, (2) Comparative genomics /
  pan-genome analyses, (3) Selecting habitat-filtered genome cohorts, (4) Distinguishing
  proGenomes from GTDB reps or MGnify biome catalogues. For taxonomy releases use gtdb.
  For biome MAG catalogues use mgnify.
license: MIT
metadata:
  metagenomics.category: "utilities"
  metagenomics.tags: "database, proGenomes, genomes, pan-genome, EMBL"
  metagenomics.upstream: "https://progenomes.embl.de/"
---

# proGenomes

Portal: https://progenomes.embl.de/

## Citation

Fullam, A. *et al.* proGenomes4: providing 2 million accurately and consistently
annotated high-quality prokaryotic genomes. *Nucleic Acids Res.* (2025).
https://doi.org/10.1093/nar/gkaf1208

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

proGenomes is a **genome warehouse** with uniform QC and multi-workflow
functional annotation (including MGE and BGC calls), habitat metadata, and
precomputed pan-genomes — ~2M genomes / >7B genes / ~33k species in v4.

| Resource | Primary question |
|----------|------------------|
| `progenomes` | Large consistently annotated prokaryotic genome set |
| `gtdb` | Rank-normalized taxonomy + species clusters / reps |
| `mgnify` | Biome-specific MAG/protein catalogues + analysed studies |
| `sra-ena` | Raw sequencing runs |

Do not assume proGenomes species IDs == GTDB species clusters without mapping.
For MAG novelty in a biome, still use the matching MGnify catalogue + GTDB-Tk.

## How to access

```text
https://progenomes.embl.de/
# CLI described in the proGenomes4 paper / site — pin the release you download
```

Archive: release ID, genome filters (quality, habitat), annotation workflow
names, and download date.

## Decision tree

```text
Need many annotated prokaryotic genomes?
├─ Habitat-aware / pan-genome / consistent annotation → progenomes
├─ Taxonomy placement of *my* MAGs → gtdbtk + gtdb
├─ Human-gut (or other biome) species catalogue → mgnify
└─ Benchmark with gold standards → cami
```

## Related skills

`public-databases` · `gtdb` · `mgnify` · `gtdbtk` · `antismash` · `genomad` ·
`eggnog-mapper` · `kegg`
