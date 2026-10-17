---
name: hadeg
description: >
  HADEG — curated Hydrocarbon Aerobic Degradation Enzymes and Genes database (alkanes,
  alkenes, aromatics, plastics) plus biosurfactant production genes with experimental
  evidence. Use to annotate MAG/contig proteins for HC biodegradation and biosurfactant
  potential. Portal-style BioSurfDB → biosurfdb; glycan DOM → dbcan.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "HADEG, hydrocarbon, biosurfactant, plastic, biodegradation, DOM"
  metagenomics.upstream: "https://github.com/jarojasva/HADEG"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "database 231119; snapshot 8f1ff8f"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "Proteinortho/R workflow reviewed against upstream; not executed here"
---

# HADEG

Upstream: [jarojasva/HADEG](https://github.com/jarojasva/HADEG)

## Citation

Rojas-Vargas, J., Castelán-Sánchez, H. G. & Pardo-López, L. HADEG: A curated
hydrocarbon aerobic degradation enzymes and genes database. *Comput. Biol. Chem.*
**107**, 107966 (2023). https://doi.org/10.1016/j.compbiolchem.2023.107966

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

HADEG provides experimentally supported sequences for:

- **Alkanes / alkenes / aromatics** (aerobic HC degradation)
- **Plastics** / polymer degradation
- **Biosurfactant** production

Annotate proteomes (e.g. DIAMOND / Proteinortho patterns in upstream README).
Pin the HADEG FASTA release date — the GitHub DB grows over time.

| vs | Prefer HADEG when |
|----|-------------------|
| `biosurfdb` | Offline curated FASTA annotation vs portal BLAST |
| `dbcan` | HC/surfactant/plastic genes vs glycan CAZymes |
| `antismash` | Marker-gene presence vs full BGC regions |

## Inputs and run

Use unique predicted-protein FASTAs and an immutable HADEG checkout/database. The reviewed workflow uses Proteinortho's published `-identity=50 -conn=0.3` settings, whose reported sensitivity/specificity tradeoff is not a universal optimum.

```bash
set -euo pipefail
root=${HADEG_ROOT:?set HADEG_ROOT to the pinned HADEG checkout}
[[ -s "$root/HADEG_protein_database_231119.faa" ]] || exit 2
find proteomes -maxdepth 1 -name '*.faa' -size +0c | grep -q .
mkdir -p result/hadeg/work
cp proteomes/*.faa "$root/HADEG_protein_database_231119.faa" result/hadeg/work/
(
  cd result/hadeg/work
  proteinortho ./*.faa -identity=50 -conn=0.3 -project=Results_HADEG
)
cp -R "$root/Scripts" result/hadeg/report
cp result/hadeg/work/Results_HADEG.proteinortho.tsv result/hadeg/report/
(cd result/hadeg/report && Rscript HADEG.R)
test -s result/hadeg/report/3_table_HADEG_final.tsv
```

## Decision tree

```text
HC / plastic / biosurfactant genes?
├─ Curated experimental set → hadeg
├─ BioSurfDB portal pathways → biosurfdb
├─ Glycan DOM → dbcan
└─ Surfactant BGCs → antismash
```

## Validation, recovery, and provenance

Require Proteinortho and all three general HADEG tables, reconcile every reported code to input protein/genome and curated database sequence, and inspect identity/connectivity tradeoffs, paralogy and pathway coverage. Keep zero-hit genomes and gene-level codes; a single marker does not establish a complete degradation pathway or biosurfactant product.

Use a fresh work/report directory after changing proteomes, database or settings. Record HADEG commit/database date and checksum, Proteinortho/R versions, command, input manifest/checksums, thresholds, tables and plots. Orthology to experimentally characterized references supports genetic potential, not expression, substrate loss or rate.

## Related skills

`dom-biosurfactant` · `biosurfdb` · `dbcan` · `antismash` · `dram` ·
`microbial-mining` · `tool-selection`
