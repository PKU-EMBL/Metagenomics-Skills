---
name: taxvamb
description: >
  TaxVAMB — semisupervised bimodal VAE binning that integrates TNF, coabundance, and
  contig taxonomy for improved MAG recovery (incl. incomplete genomes and long-read
  sets). Use when: (1) Taxonomy-informed binning, (2) Comparing to VAMB/AAMB/SemiBin2,
  (3) Single-sample setups needing more HQ bins. Taxonomy labels are an input feature —
  garbage taxonomy in, garbage bins out.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, TaxVAMB, VAMB, taxonomy, deep-learning"
  metagenomics.upstream: "https://github.com/RasmussenLab/vamb"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot b146fb6"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and taxonomy schema reviewed against upstream; not executed here"
---

# TaxVAMB

Upstream: [RasmussenLab/vamb](https://github.com/RasmussenLab/vamb)

## Citation

Kutuzova, S. *et al.* Improving metagenome binning by integrating intrinsic
features and taxonomy. *Nat. Biotechnol.* (2026).
https://doi.org/10.1038/s41587-026-03098-0

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

TaxVAMB adds **contig-level taxonomy** into a VAMB-style VAE. Strong reported
gains on CAMI2 human sets and long-read data, and on incomplete genomes — but
performance inherits taxonomy DB bias. Prefer high-quality taxonomic inputs;
do not circularly claim novelty from taxonomy-informed bins without independent
QC (`checkm2`, `gunc`, `gtdbtk`).

## Inputs and run

Use the current VAMB concatenated-contig naming contract, an abundance TSV generated against that exact FASTA, and a taxonomy TSV beginning with `contigs<TAB>predictions`. Each later field is a semicolon-delimited lineage; unclassified contigs must remain explicit.

```bash
set -euo pipefail
[[ -s contigs.fna.gz && -s abundance.tsv && -s taxonomy.tsv ]] || exit 2
[[ "$(head -n1 taxonomy.tsv)" == $'contigs\tpredictions' ]] || exit 3
vamb --version
vamb bin taxvamb --outdir result/taxvamb \
  --fasta contigs.fna.gz --abundance_tsv abundance.tsv \
  --taxonomy taxonomy.tsv \
  >taxvamb.stdout.log 2>taxvamb.stderr.log
```

By default TaxVAMB refines an unrefined taxonomy with Taxometer; use `--no_predictor` only as a declared sensitivity route. Never supply taxonomy from a database/release that conflicts with downstream novelty claims.

## Validation, recovery, and provenance

Require completed `log.txt`, Taxometer predictions when enabled, TaxVAMB cluster tables and matching FASTAs/assignments. Reconcile FASTA, abundance and taxonomy refhash/IDs; inspect missing taxonomy, prediction confidence, ambiguous ranks, unique final membership and binned bases. Evaluate candidates with CheckM2/GUNC and compare a default VAMB run to quantify taxonomy dependence.

Use a fresh output after any input, taxonomy, predictor or training change. Record VAMB/PyTorch/CUDA versions, command, FASTA/abundance/taxonomy checksums and database provenance, sample order, predictor settings, seeds/device, cluster/checksum tables and independent QC. Taxonomy-informed clustering cannot independently validate the taxonomy supplied to it.

## Related skills

`vamb` · `aamb` · `metabuli` · `mmseqs2` · `basalt` · `checkm2` · `tool-selection`
