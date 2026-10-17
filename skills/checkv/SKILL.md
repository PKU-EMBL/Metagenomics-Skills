---
name: checkv
description: >
  Quality assessment of metagenome-assembled viral genomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "virus, qc, genome-mining"
  metagenomics.upstream: "https://bitbucket.org/berkeleylab/checkv"
  metagenomics.stage: "mining"
---

# CheckV

Upstream: [CheckV](https://bitbucket.org/berkeleylab/checkv)

## Citation

Nayfach, S. *et al.* CheckV assesses the quality and completeness of metagenome-assembled viral genomes. *Nat. Biotechnol.* **39**, 578–585 (2021). https://doi.org/10.1038/s41587-020-00774-7

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Prokaryotic CheckM/CheckM2 marker logic does **not** transfer to viruses. CheckV
estimates viral genome completeness/contamination using viral-specific AAI
databases and contig QC, guiding which viral MAGs/contigs to trust.

Use after `genomad` / `virsorter2` (or similar) nomination. Always report CheckV
DB version. Completeness tiers in the paper (e.g. high-/medium-quality viral
genomes) should be stated explicitly in Methods — do not call every viral hit a
“complete phage genome.”

Host prediction / taxonomy are separate tools; CheckV is quality-centric.

## How to run

```bash
checkv end_to_end viral_contigs.fa temp/checkv -t 16 -d $CHECKVDB
```

## Key parameters

| Item | Notes |
|------|-------|
| `$CHECKVDB` | Required — pin release |
| Input | Putative viral sequences from VirSorter2/geNomad |
| Output tiers | Use CheckV quality categories in Results filters |

## Related skills

`virsorter2` · `genomad` · `mag-qc` · `microbial-mining` · `tool-selection`
`vcontact`
