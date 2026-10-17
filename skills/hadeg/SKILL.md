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

## How to run

```bash
# download HADEG_protein_database_*.faa from upstream releases
# typical: diamond blastp -q proteins.faa --db HADEG.dmnd -o hits.tsv …
# or Proteinortho workflows in upstream README; then parse group tables
# (Alkanes / Alkenes / Aromatics / Biosurfactants / Plastics)
```

## Decision tree

```text
HC / plastic / biosurfactant genes?
├─ Curated experimental set → hadeg
├─ BioSurfDB portal pathways → biosurfdb
├─ Glycan DOM → dbcan
└─ Surfactant BGCs → antismash
```

## Related skills

`dom-biosurfactant` · `biosurfdb` · `dbcan` · `antismash` · `dram` ·
`microbial-mining` · `tool-selection`
