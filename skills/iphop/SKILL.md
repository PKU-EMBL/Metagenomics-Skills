---
name: iphop
description: >-
  Predict bacterial or archaeal virus hosts with iPHoP by integrating host-genome and phage-based signals, using a pinned iPHoP database and explicit confidence cutoff. Use on quality-gated phage genomes when genus- or genome-level computational host evidence is needed.
license: MIT
compatibility: Requires iPHoP 1.4.2, its large compatible host database, Linux/Conda or container runtime, and viral nucleotide FASTA.
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "iphop,phage-host,virus-host,crispr,host-prediction"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "1.4.2"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# iPHoP

iPHoP predicts hosts of bacteriophages and archaeal viruses. It does not address eukaryotic-virus hosts or experimentally prove infection.

## Inputs

- viral nucleotide genomes/contigs with unique IDs, preferably quality-gated with `$checkv`;
- iPHoP database compatible with the installed software;
- optional high-quality local bacterial/archaeal MAGs added to a copied database;
- explicit minimum score and thread/memory allocation.

Screen custom host MAGs for contamination. A viral contig mis-binned into a host MAG can produce a circular, high-confidence false host link.

## Database setup and verification

```bash
set -euo pipefail
DBROOT=/data/iphop_db
mkdir -p "$DBROOT"
iphop download --db_dir "$DBROOT" -dbv iPHoP_db_rw_1.4_for-test
iphop download --db_dir "$DBROOT" --full_verify
```

The small test database is for installation validation only. For production, pin and record the full database directory/release (for example the upstream June 2025 release when appropriate), archive checksums, and ensure sufficient storage/RAM.

## Predict

```bash
set -euo pipefail
viral=${1:?usage: iphop-run.sh viruses.fna database_dir output_dir}
db=${2:?usage: iphop-run.sh viruses.fna database_dir output_dir}
out=${3:?usage: iphop-run.sh viruses.fna database_dir output_dir}
[[ -s "$viral" && -d "$db" ]] || exit 2
[[ ! -e "$out" ]] || { echo "use a new output directory: $out" >&2; exit 2; }
iphop predict --fa_file "$viral" --db_dir "$db" --out_dir "$out" \
  --min_score 90 -t 16 >"${out}.stdout.log" 2>"${out}.stderr.log"
[[ -s "$out/Host_prediction_to_genus_m90.csv" && \
   -s "$out/Detailed_output_by_tool.csv" ]] || {
  echo "iPHoP did not produce required tables" >&2; exit 3;
}
```

The standard upstream command uses `--fa_file`, `--db_dir`, and `--out_dir`. Query `iphop predict -h` for the pinned release before changing options.

## Outputs and validation

- `Host_prediction_to_genus_mXX.csv`: integrated genus-level calls at cutoff XX;
- `Host_prediction_to_genome_mXX.csv`: host-based genome-level calls;
- `Detailed_output_by_tool.csv`: method-specific scores/evidence.

Validate that every reported virus exists in the input, scores meet the stated cutoff, duplicate/multiple host predictions are retained for review, and no internal component failed silently. Compare CRISPR, nucleotide homology, iPHoP-RF, and RaFAH evidence rather than using only the top label. Report the fraction of viruses with no prediction.

## Failure recovery

Use a fresh output directory after an early failure unless upstream explicitly documents safe reuse. For large-query failures, split FASTA deterministically and merge final tables while checking IDs. RaFAH/WIsH errors can leave partial integrated output; inspect warnings and `Wdir`, not just the final filename.

## Analytical thinking

Confidence is calibrated computational evidence conditional on database composition. Host range, active infection, and directionality are not observed. Genus predictions may include multiple candidates; habitat co-occurrence alone is weak corroboration.

## Source

- https://github.com/simroux/iphop
- https://doi.org/10.1371/journal.pbio.3002083
