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
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and utility contracts reviewed; not executed here"
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

## Validation, recovery, and provenance

Require `quality_summary.tsv` plus contamination/provirus/complete-genome tables and processed FASTAs produced by the pinned release. Reconcile every input sequence to a quality row or explicit failure, inspect quality category, completeness method/range, contamination, host boundaries, terminal repeats, and warnings, and preserve parent-to-trimmed coordinates. Zero hits can be valid; missing summary output is not.

Run vOTU clustering on the exact quality-gated/trimmed sequences and keep IDs stable. Use a fresh output after changing input or database. Record CheckV and dependency versions, database release/checksum, command, FASTA checksums, and acceptance rule. Completeness and contamination are estimates; CheckV does not establish taxonomy, host, or activity.

## Related skills

`virome-analysis` · `votu-workflow` · `virsorter2` · `genomad` · `mag-qc` ·
`microbial-mining` · `tool-selection` · `vcontact`
