---
name: dram
description: >
  Distill microbial metabolism annotations for MAGs/genomes into curated product tables
  (DRAM annotate + distill). Use for ecological functional potential, pathway summaries,
  and MAG metabolism figures.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "metabolism, annotation, genome-mining, DRAM"
  metagenomics.upstream: "https://github.com/WrightonLabCSU/DRAM"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy-interface"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "DRAM 1.x CLI contract documented; not executed here"
---

# DRAM

Upstream: [WrightonLabCSU/DRAM](https://github.com/WrightonLabCSU/DRAM)

## Citation

Shaffer, M. *et al.* DRAM for distilling microbial metabolism to automate the
curation of microbiome function. *Nucleic Acids Res.* **48**, 8883–8900 (2020).
https://doi.org/10.1093/nar/gkaa621

## Analytical thinking

DRAM wraps multiple DBs (KEGG, MEROPS, CAZy, … depending on install) then
**distills** annotations into interpretable metabolism sheets. Ideal after
binning QC when the question is “what can these MAGs do?”, not read-level
HUMAnN pathways.

Heavy **one-time DB install** — share a read-only DRAM DB on the cluster. Pin
DRAM version + DB pull date. Low-completeness MAGs yield sparse distillates;
filter with `mag-qc` first.

Complementary: `eggnog-mapper` (orthology), `antismash` (BGCs), `gapseq`
(GEMs). Do not merge DRAM distillate rows with HUMAnN pathway abundances
without stating different evidence layers.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| DRAM DB | Configured via DRAM manuals | Shared `$DRAM_DATA` |
| Input | Genome/MAG FASTA directory | CheckM2-filtered |
| RAM | 64 GB | 128 GB+ for large batches |
| CPU | 8 | 16–32 |

## How to run

```bash
# DRAM 1.x-style interface after a pinned database/configuration preflight:
mkdir -p temp/dram
DRAM.py annotate \
  -i 'bins_hq/*.fa' \
  -o temp/dram/annotate \
  --threads 16

DRAM.py distill \
  -i temp/dram/annotate/annotations.tsv \
  -o temp/dram/distill \
  --trna_path temp/dram/annotate/trnas.tsv \
  --rrna_path temp/dram/annotate/rrnas.tsv
```

This block targets the DRAM 1.x `DRAM.py` interface. Treat `DRAM.py annotate -h` and `DRAM.py distill -h` as mandatory preflight; DRAM2 requires its own pinned command contract rather than silently translating flags.

## Key products

| Output | Use |
|--------|-----|
| `annotations.tsv` | Per-gene annotations |
| distillate / product sheets | Metabolism summary heatmaps |
| genome stats | Completeness-aware interpretation |

## Decision tree

```text
Functional question?
├─ Read-level pathways → humann
├─ MAG metabolism distillate → dram
├─ Genome-scale model → gapseq (HQ MAGs)
└─ BGCs only → antismash
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| DB not configured | Complete DRAM database setup before annotate |
| Annotate dies on one bad FASTA | Validate FASTA headers/unique names |
| Empty distillate | Check annotate finished; tRNA/rRNA paths |

## Validation, recovery, and provenance

Require non-empty `annotations.tsv`, tRNA/rRNA outputs when requested, completed logs, and distillate/product tables. Reconcile every genome and gene ID, inspect annotation coverage by database, duplicate IDs, database failures and low-completeness genomes; retain gene-level evidence behind each distilled trait. Treat a pathway/module as supported only under an explicit required-step rule rather than one matching gene.

Database setup is version-sensitive. Use a fresh output after changing DRAM/config/databases and do not combine sheets from unlike releases. Record DRAM/dependency versions, configuration export, each enabled database version/date/checksum and license status, full commands, genome/checksum manifest, QC table, and result checksums. Distillates predict encoded potential—not pathway activity, flux, or phenotype.

## Related skills

`microbial-mining` · `eggnog-mapper` · `bakta` · `gapseq` · `antismash` · `dbcan` · `mag-qc`
