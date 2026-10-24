---
name: busco
description: >
  Benchmarking Universal Single-Copy Orthologs for genome completeness. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "qc, completeness, busco"
  metagenomics.upstream: "https://gitlab.com/ezlab/busco"
  metagenomics.stage: "assessment"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "genome mode and out_path contract statically reviewed; not executed here"
---

# BUSCO

Upstream: [BUSCO](https://gitlab.com/ezlab/busco)

## Citation

Manni, M. *et al.* BUSCO update: novel and streamlined workflows along with broader and deeper phylogenetic coverage for scoring of eukaryotic, prokaryotic, and viral genomes. *Mol. Biol. Evol.* **38**, 4647–4654 (2021). https://doi.org/10.1093/molbev/msab199

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Useful for isolates/eukaryotes; for prokaryotic MAGs prefer **CheckM2** (+ GUNC). Do not mix BUSCO% with CheckM2% unlabeled.

## How to run

Select and freeze a domain/lineage dataset before comparisons. BUSCO's `-o` is
a run name; use `--out_path` for the parent directory.

```bash
set -Eeuo pipefail
id="${1:?usage: run-busco.sh GENOME_ID GENOME_FASTA OUTPUT_PARENT}"
genome="${2:?usage: run-busco.sh GENOME_ID GENOME_FASTA OUTPUT_PARENT}"
out_parent="${3:?usage: run-busco.sh GENOME_ID GENOME_FASTA OUTPUT_PARENT}"
lineage="${BUSCO_LINEAGE:-bacteria_odb10}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
test -s "$genome" || exit 2
test ! -e "$out_parent/$id" && \
  test ! -e "$out_parent/logs/${id}.stdout.log" && \
  test ! -e "$out_parent/logs/${id}.stderr.log" || {
  echo "use a new BUSCO run name" >&2; exit 2;
}
mkdir -p "$out_parent" "$out_parent/logs"

busco -i "$genome" -l "$lineage" -o "$id" --out_path "$out_parent" \
  -m genome -c "$threads" --offline \
  >"$out_parent/logs/${id}.stdout.log" \
  2>"$out_parent/logs/${id}.stderr.log"
find "$out_parent/$id" -type f -name 'short_summary*.txt' -size +0c -print -quit | grep -q .
find "$out_parent/$id" -type f -name 'full_table*.tsv' -size +0c -print -quit | grep -q .
```

## Key parameters

| `-l` | lineage DB | Match domain |
| `-m` | genome/proteins | |

## Decision notes

- Stage: **assessment** (gene-set completeness; complementary to CheckM2 for some lineages)
- Prefer lineage-appropriate BUSCO DB; do not treat BUSCO % as MAG contamination
- Pin software + DB versions in Methods

## Validation, recovery, and provenance

Require short/full summaries, missing-BUSCO list, logs and lineage metadata.
Inspect complete single-copy, duplicated, fragmented and missing fractions,
gene-predictor behavior, assembly mode, lineage appropriateness, and sample
failures. For MAGs, duplicated BUSCOs are not a calibrated contamination metric;
compare only like-for-like lineage and BUSCO releases.

Use fresh run names after changing input, lineage, predictor, or release. Record
BUSCO, predictor and dependency versions, lineage name/date/checksum, genome
checksum, mode/options, command, logs, summary/full-table checksums, and any
exclusions. Keep BUSCO gene-set completeness distinct from CheckM2 estimates.

## Related skills

`checkm2` · `gunc` · `mag-qc` · `tool-selection` · `metagenomics-workflow`
