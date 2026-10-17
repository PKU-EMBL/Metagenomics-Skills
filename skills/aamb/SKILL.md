---
name: aamb
description: >
  AAMB / AVAMB — adversarial autoencoder metagenomic binning and its ensemble with VAMB
  for improved near-complete MAG recovery. Use when: (1) Running AAMB as a DL single
  binner, (2) AVAMB ensemble (VAMB+AAMB) for extra NC genomes, (3) Diversifying bins
  before DAS Tool/BASALT. Still QC with checkm2; prefer basalt ★ for multi-assembly
  catalogues.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "binning, AAMB, AVAMB, VAMB, deep-learning"
  metagenomics.upstream: "https://github.com/RasmussenLab/vamb"
  metagenomics.stage: "binning"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.upstream-version: "AVAMB workflow 4.1.3; current VAMB snapshot b146fb6"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "legacy workflow CLI reviewed; not executed here"
---

# AAMB / AVAMB

Upstream: [RasmussenLab/vamb](https://github.com/RasmussenLab/vamb) (AAMB/AVAMB
paths documented in the VAMB repository)

## Citation

Piera Líndez, P. *et al.* Adversarial and variational autoencoders improve
metagenomic binning. *Commun. Biol.* **6**, 1073 (2023).
https://doi.org/10.1038/s42003-023-05452-3

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

AAMB uses **adversarial autoencoders** on coabundance + TNF; AVAMB ensembles
AAMB with VAMB and recovered substantially more near-complete genomes in the
paper vs VAMB alone. Treat as a **diverse DL binner** for ensembles — not a
replacement for `basalt` multi-assembly refinement.

Related VAMB-family tools: `vamb`, `taxvamb`. Current VAMB documentation calls AVAMB obsolete and recommends TaxVAMB when reliable contig taxonomy and sufficient compute are available; use AVAMB mainly for reproducing its published workflow.

## Inputs and run

The archived AVAMB Snakemake workflow requires `config.json`, an ordered one-path-per-line `contigs.txt`, and a tab-separated `samples2data.tsv` containing sample ID, R1 and R2. Pin VAMB `v4.1.3` for this workflow rather than mixing it with current-main internals.

```bash
set -euo pipefail
root=${VAMB_413:?set VAMB_413 to a VAMB v4.1.3 checkout}
[[ -s config.json && -s contigs.txt && -s samples2data.tsv ]] || exit 2
python -m json.tool config.json >/dev/null
snakemake --cores 20 --use-conda --configfile config.json \
  --snakefile "$root/workflow_avamb/avamb.snake.conda.smk" --dry-run
snakemake --cores 20 --use-conda --configfile config.json \
  --snakefile "$root/workflow_avamb/avamb.snake.conda.smk" \
  >avamb.stdout.log 2>avamb.stderr.log
```

Review `outdir`, quality thresholds and `avamb_params` before execution; use a new output when changing them.

## Validation, recovery, and provenance

Require completed Snakemake rules, `Final_clusters.tsv`, `Final_bins/quality_report.tsv`, matching final FASTAs and VAE/AAE component assignments. Reconcile every final contig, ensure unique retained membership, review CheckM2 gates and compare VAMB/AAMB contributions under identical criteria. Reassess with GUNC and current CheckM2 rather than assuming workflow-era QC is final.

Resume only from unchanged Snakemake inputs/config/environments; otherwise archive and rerun. Record workflow/VAMB/CheckM2 commits, database, config, commands, ordered sample/read/assembly checksums, mapper settings, seeds/device, logs, component/final memberships and candidate checksums. AAMB/AVAMB clusters remain candidate genomes.

## Related skills

`vamb` · `taxvamb` · `semibin2` · `dastool` · `basalt` · `tool-selection`
