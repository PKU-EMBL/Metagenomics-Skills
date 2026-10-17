---
name: eggnog-mapper
description: >
  Orthology-based functional annotation (COG/KEGG/CAZy via eggNOG). Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "annotation, orthology, function"
  metagenomics.upstream: "https://github.com/eggnogdb/eggnog-mapper"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI contract reviewed; not executed here"
---

# eggNOG-mapper

Upstream: [eggnogdb/eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper)

## Citation

Cantalapiedra, C. P., Hernández-Plaza, A., Letunic, I., Bork, P. & Huerta-Cepas, J. eggNOG-mapper v2: functional annotation, orthology assignments, and domain prediction at the metagenomic scale. *Mol. Biol. Evol.* **38**, 5825–5829 (2021). https://doi.org/10.1093/molbev/msab293

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Annotate **proteins** from an NR gene catalogue or MAG proteomes via eggNOG
orthology (COG/KEGG/CAZy fields, etc.). DIAMOND mode is the common metagenome
default.

Combine with abundances carefully: sum TPM/counts of genes mapping to a KO/COG
only when the gene→function mapping is declared. Orthology hit ≠ experimental
function.

| vs other function layers | Notes |
|--------------------------|-------|
| `humann` | Read-level pathways (MetaCyc/UniRef) — different claim |
| `dram` | Distilled MAG metabolism tables |
| `kegg` | Direct KO maps (license) — may overlap fields |

## How to run

```bash
emapper.py --data_dir ${db}/eggnog \
  -i NR/protein.fa --cpu 16 -m diamond --override \
  -o temp/eggnog/output
```

## Key parameters

| Flag | Notes |
|------|-------|
| `-m diamond` | Typical metagenome speed/sensitivity balance |
| `--data_dir` | Pin eggNOG DB release |
| Input | Proteins from `prodigal` / `bakta` |

## Decision tree

```text
Functional annotation need?
├─ Catalogue proteins → eggnog-mapper (+ salmon abundances)
├─ Read pathways → humann
├─ MAG metabolism distillate → dram
└─ AMR specifically → rgi
```

## Methods caveats

- Pin emapper + eggNOG DB versions
- Do not label KEGG-like fields as full KEGG pathway proof without rules

## Validation, recovery, and provenance

Require a non-empty `.emapper.annotations` table and completed seed-ortholog/hit files/logs. Reconcile every query as annotated or unannotated, verify unique protein IDs, inspect annotation coverage and taxonomic scope, and retain evidence columns (`seed_ortholog`, e-value, score, orthology level) alongside functions. Distinguish missing assignment from biological absence.

`--override` can replace prior results; archive or use a new prefix when changing input/database/options. Record eggNOG-mapper, DIAMOND/MMseqs versions, eggNOG database release/checksum, taxonomic scope, command, query checksum, and annotation-table checksum. Any KO/COG/EC label remains an orthology-based prediction.

## Related skills

`prodigal` · `salmon` · `diamond` · `dram` · `kegg` · `rgi` · `visualization` ·
`tool-selection`
