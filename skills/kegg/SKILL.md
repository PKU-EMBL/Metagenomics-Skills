---
name: kegg
description: >
  KEGG as a reference for gene/protein annotation — KO orthologs, pathways,
  modules, BRITE (BlastKOALA / GhostKOALA and related assignment). Use when:
  (1) Mapping genes/MAGs to KEGG Orthology, (2) Reconstructing pathways/modules,
  (3) Choosing KEGG vs eggNOG / MetaCyc / DRAM distillation, (4) Citing KEGG
  releases in Methods. Portal: https://www.kegg.jp/. Licensing/access constraints
  apply for bulk use — verify institutional rights. For eggNOG use eggnog-mapper.
  For pathway abundance from reads use humann. For routing use public-databases.
license: MIT
category: utilities
tags: [database, KEGG, KO, pathway, annotation]
upstream: https://www.kegg.jp/
---

# KEGG (Kyoto Encyclopedia of Genes and Genomes)

Portal: https://www.kegg.jp/ · https://www.genome.jp/kegg/

## Citation

Kanehisa, M., Sato, Y., Kawashima, M., Furumichi, M. & Tanabe, M. KEGG as a
reference resource for gene and protein annotation. *Nucleic Acids Res.* **44**,
D457–D462 (2016). https://doi.org/10.1093/nar/gkv1070

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

KEGG links genes to **high-level functions** via KO (K numbers) → PATHWAY /
MODULE / BRITE networks. In shotgun workflows it appears as:

| Path | Typical tools |
|------|----------------|
| Gene → KO assignment | BlastKOALA / GhostKOALA / KofamKOALA; or via eggNOG-mapper KEGG fields |
| Pathway abundance from reads | Often MetaCyc via `humann` (not raw KEGG API) |
| Distilled metabolism tables | `dram` (multi-DB including KEGG-related sources) |

Hard rules:

1. **License / redistributability** — KEGG is not a free-for-all dump; confirm
   access rights before bulk downloads or redistributing KO databases.
2. Pin KEGG / KOALA DB versions next to software versions.
3. Pathway presence from incomplete MAGs ≠ organism capability proof.
4. Do not merge HUMAnN MetaCyc pathway names with KEGG map IDs unlabeled.

## Decision tree

```text
Functional reference need?
├─ KO / KEGG pathway maps with institutional access → kegg
├─ Orthology + multi-DB (COG/KEGG/CAZy fields) → eggnog-mapper
├─ Read-level gene families / MetaCyc pathways → humann + biobakery-databases
├─ Curated MAG metabolism distillate → dram
└─ CAZymes specifically → dbcan
```

## Related skills

`public-databases` · `eggnog-mapper` · `humann` · `dram` · `gapseq` ·
`progenomes` · `biobakery-databases`
