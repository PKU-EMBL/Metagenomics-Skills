---
name: pathofact
description: >-
  Run and audit PathoFact 2.0 for integrated prediction of antimicrobial-resistance
  genes, virulence factors, toxins, biosynthetic clusters, and geNomad MGE context from
  metagenomic contigs or proteins. Use when component databases, model thresholds,
  compressed-input rules, and method-specific evidence must remain visible.
license: MIT
compatibility: Requires Linux, Snakemake 7.25-era workflow support, multiple Conda environments, PathoFact 2.0 databases/models, and gzipped contig or protein FASTA.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PathoFact,AMR,virulence,toxin,MGE,BGC,Snakemake"
  metagenomics.upstream: "https://gitlab.com/uniluxembourg/lcsb/systems-ecology/pathofact2"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "2.0 commit bd5d527ede15"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "workflow/config/output contract reviewed; not executed here"
---

# PathoFact 2.0

PathoFact integrates AMRFinderPlus, DeepARG, RGI, geNomad, HMM and machine-learning
predictions, with optional antiSMASH and SignalP. Preserve each component’s call and score;
the combined report is not a single experimentally calibrated classifier.

## Input and setup contract

- inputs must be gzip-compressed contig or protein FASTA;
- `list_of_samples.csv` has unique IDs, absolute paths, and correct `contigs`/`proteins` type;
- `Config.yaml` uses absolute work/output/database/model paths;
- pin workflow commit `bd5d527ede15` or a later explicitly reviewed release;
- pin Zenodo database archive record, geNomad/DeepARG/CARD/RGI data, and optional
  antiSMASH/SignalP assets independently;
- archive all thresholds in the config, including ambiguous-call handling.

SignalP has separate licensing/distribution requirements. Do not enable optional modules
unless their assets and licenses have been reviewed.

## Preflight and run

Use a run-specific checkout or immutable container. First perform a Snakemake dry run,
then execute the same DAG.

```bash
set -euo pipefail
workflow=${PATHOFACT_RUN:?set PATHOFACT_RUN to a writable copy of the pinned checkout}
runconfig=${CONFIG:?set CONFIG to reviewed Config.yaml}
samples=${SAMPLES:?set SAMPLES to list_of_samples.csv}
logdir=${LOGDIR:-}
[[ -s "$workflow/Main.smk" && -s "$runconfig" && -s "$samples" ]] || exit 2
cp "$runconfig" "$workflow/Config.yaml"
out=$(python3 - "$workflow/Config.yaml" "$samples" <<'PY'
import pathlib, sys, yaml
config_path = pathlib.Path(sys.argv[1]).resolve()
with config_path.open(encoding="utf-8") as handle:
    config = yaml.safe_load(handle)
def resolved(value):
    path = pathlib.Path(value)
    return (path if path.is_absolute() else config_path.parent / path).resolve()
if resolved(config["samples_info"]) != pathlib.Path(sys.argv[2]).resolve():
    raise SystemExit("Config.yaml samples_info does not match SAMPLES")
print(resolved(config["output_dir"]))
PY
)
logdir=${logdir:-${out}.logs}
[[ ! -e "$out" && ! -e "$logdir" ]] || {
  echo "use new output and log directories: $out ; $logdir" >&2; exit 2;
}
mkdir -p "$logdir"
(
  cd "$workflow"
  snakemake -s Main.smk --cores 32 --use-conda --rerun-incomplete -n -p
  snakemake -s Main.smk --cores 32 --use-conda --rerun-incomplete -p
) >"$logdir/pathofact.stdout.log" 2>"$logdir/pathofact.stderr.log"
find "$out/summary" -type f \( -name 'combined_report.tsv' -o -name 'combined_report_with_MGE.tsv' \) -size +0c -print -quit | grep -q .
```

The short Python block reads configuration only; it does not validate biological output.
`PATHOFACT_RUN` must be a run-specific writable copy; keep the pinned source checkout
immutable. The preflight rejects a config whose `samples_info` does not resolve to the
reviewed manifest.

## Output gates

For every declared sample, require the appropriate summary report and component outputs.
For contigs with geNomad enabled, inspect `*_with_MGE.tsv` plus geNomad JSON/summary files.
Reconcile representative proteins after MMseqs2 clustering to original IDs using
`clean_cluster.tsv`. Confirm AMRFinder, DeepARG, RGI, HMM/ML and optional antiSMASH modules
completed; a combined file can exist despite a component warning.

## Validation

- count samples from the manifest versus each output branch;
- verify contig/protein identifiers and coordinate mappings;
- retain ambiguous VF/toxin calls separately;
- distinguish agreement from duplicated evidence derived from related databases;
- inspect MGE context as geNomad classification, not proof of transfer or host;
- compare headline ARGs with method-native outputs and controls;
- record zero-hit samples rather than dropping them.

## Recovery and provenance

Use `--rerun-incomplete` only with unchanged input, config, databases, and workflow commit.
Any change requires a new run directory. Archive workflow commit, `Config.yaml`, manifest,
Conda environment exports, every database/model release and checksum, Snakemake DAG/logs,
and all component reports.

## Interpretation

Predicted AMR, virulence, toxin, BGC, and MGE labels are computational evidence. They do
not establish expression, toxicity, virulence phenotype, clinical resistance, a complete
mobile element, host range, or transfer.

## Sources

- https://gitlab.com/uniluxembourg/lcsb/systems-ecology/pathofact2
- https://doi.org/10.1093/gigascience/giag062

## Related skills

`resistome-analysis` · `amrfinderplus` · `rgi` · `deeparg` · `genomad` ·
`antismash` · `mobilome-analysis` · `arg-mge-host-linkage` · `snakemake`
