---
name: dbcan
description: >
  Annotate carbohydrate-active enzymes (CAZymes) with dbCAN3 / run_dbcan on genomes or
  protein sets, including CGC finding and glycan substrate prediction (dbCAN-sub /
  dbCAN-PUL) relevant to dissolved organic matter (DOM) polymer processing. Use for
  CAZyme mining complementary to DRAM/eggNOG and to dom-biosurfactant routing.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "CAZy, CAZyme, DOM, glycan, substrate, genome-mining, dbCAN3"
  metagenomics.upstream: "https://github.com/bcb-unl/run_dbcan"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "run_dbcan 5 interface"
  metagenomics.command-status: "CAZyme_annotation CLI checked against official v5 documentation; not executed here"
---

# dbCAN (run_dbcan / dbCAN3)

Upstream: [bcb-unl/run_dbcan](https://github.com/bcb-unl/run_dbcan) ·
Documentation: https://run-dbcan.readthedocs.io/ ·
Server: https://bcb.unl.edu/dbCAN2/

## Citation

Zheng, J. *et al.* dbCAN3: automated carbohydrate-active enzyme and substrate
annotation. *Nucleic Acids Res.* **51**, W115–W121 (2023).
https://doi.org/10.1093/nar/gkad328

Earlier: Zhang, H. *et al.* dbCAN2: a meta server for automated carbohydrate-active
enzyme annotation. *Nucleic Acids Res.* **46**, W95–W101 (2018).
https://doi.org/10.1093/nar/gky418

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

CAZymes process complex carbohydrates — a major fraction of **DOM / polymer
organic matter** (cellulose, xylan, pectin, mucin, etc.). dbCAN3 adds
**substrate prediction** at subfamily and CGC/PUL levels. Prefer protein FASTA
(+ GFF for CGC) from `bakta`/`prodigal`. Consensus across HMMER/DIAMOND/
dbCAN-sub is stronger than a single hit.

| vs | Prefer dbCAN when |
|----|-------------------|
| `hadeg` / `biosurfdb` | Glycan DOM vs HC/biosurfactant genes |
| `dram` | Dedicated CAZyme/substrate detail vs distillate sheets |
| `element-cycling` | Organic C polymer enzymes vs inorganic C/N/S cycles |

## How to run

run_dbcan 5 uses subcommands. This protein-mode example runs the three core
methods against a pinned database prepared with `run_dbcan database`.

```bash
set -Eeuo pipefail
proteins="${1:?usage: annotate-dbcan.sh PROTEINS_FAA DB_DIR OUTPUT_DIR}"
db="${2:?usage: annotate-dbcan.sh PROTEINS_FAA DB_DIR OUTPUT_DIR}"
out="${3:?usage: annotate-dbcan.sh PROTEINS_FAA DB_DIR OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$proteins" && test -d "$db" || exit 2
log_dir="${out}.logs"
test ! -e "$out" && test ! -e "$log_dir" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "$log_dir"

run_dbcan CAZyme_annotation \
  --input_raw_data "$proteins" --output_dir "$out" --db_dir "$db" \
  --mode protein --methods diamond --methods hmm --methods dbCANsub \
  --threads "$threads" --log-file "$log_dir/run_dbcan.log" \
  >"$log_dir/dbcan.stdout.log" 2>"$log_dir/dbcan.stderr.log"
```

For CGC and substrate prediction, retain genome coordinates/GFF and use the
version-matched `easy_CGC` or `easy_substrate` workflow. Legacy run_dbcan 4 uses
a different positional interface and must be reported separately.

## Decision tree

```text
Glycan / DOM polymer capacity?
├─ CAZymes + substrates / CGC → dbcan
├─ HC / biosurfactant / plastic → hadeg (± biosurfdb)
├─ Broad distillate → dram
└─ Route menu → dom-biosurfactant
```

## Validation, recovery, and provenance

Require `overview.txt` plus method-specific DIAMOND, HMM, and dbCAN-sub outputs;
reconcile input protein IDs and retain method agreement instead of collapsing to
an undocumented Boolean. For CGCs, verify GFF/protein ID consistency, genomic
neighborhoods, boundaries, substrate evidence, and contig-edge truncation.

Use fresh outputs after changing database, methods, or release. Record run_dbcan
and dependency versions, database snapshot/checksum, input/GFF checksums,
methods and thresholds, commands, logs, method-level and consensus tables, and
result checksums. CAZyme/substrate calls indicate predicted capacity, not measured
DOM transformation.

## Related skills

`dom-biosurfactant` · `hadeg` · `biosurfdb` · `dram` · `eggnog-mapper` ·
`bakta` · `prodigal` · `element-cycling` · `microbial-mining` · `tool-selection`
