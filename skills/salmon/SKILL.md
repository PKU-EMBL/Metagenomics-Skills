---
name: salmon
description: >
  Fast quantification of gene/transcript abundance; use --meta for metagenomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "quantification, abundance"
  metagenomics.upstream: "https://github.com/COMBINE-lab/salmon"
  metagenomics.stage: "function"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "2.x workflow"
  metagenomics.command-status: "index/paired quant workflow checked against Salmon 2 documentation; not executed here"
---

# Salmon

Upstream: [COMBINE-lab/salmon](https://github.com/COMBINE-lab/salmon)

## Citation

Patro, R., Duggal, G., Love, M. I., Irizarry, R. A. & Kingsford, C. Salmon provides fast and bias-aware quantification of transcript expression. *Nat. Methods* **14**, 417–419 (2017). https://doi.org/10.1038/nmeth.4197

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Quantify a **non-redundant gene catalogue** (nucleotides) with dehosted PE reads.
Typical catalogue path:

```text
prodigal (contigs) → cd-hit | mmseqs2 (NR) → salmon quant --meta
                   → eggnog-mapper on NR proteins
```

For metagenomes pass **`--meta`**. Prefer TPM vs counts consciously — downstream
stats must match the unit. CoverM genome abundance ≠ gene catalogue TPM.

Note: salmon 2.x (Rust) changed index format — rebuild indexes when upgrading;
bioconda may still ship 1.x (`salmon-cpp`). Pin and document the version.

## How to run

Build one immutable index, then quantify each synchronized pair into a fresh
sample directory. Confirm `--meta` exists in the pinned major version before use.

```bash
set -Eeuo pipefail
id="${1:?usage: quantify-salmon.sh SAMPLE_ID CATALOGUE_FNA R1 R2 RUN_ROOT}"
catalogue="${2:?usage: quantify-salmon.sh SAMPLE_ID CATALOGUE_FNA R1 R2 RUN_ROOT}"
r1="${3:?usage: quantify-salmon.sh SAMPLE_ID CATALOGUE_FNA R1 R2 RUN_ROOT}"
r2="${4:?usage: quantify-salmon.sh SAMPLE_ID CATALOGUE_FNA R1 R2 RUN_ROOT}"
root="${5:?usage: quantify-salmon.sh SAMPLE_ID CATALOGUE_FNA R1 R2 RUN_ROOT}"
threads="${THREADS:-8}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$catalogue" "$r1" "$r2"; do test -s "$input" || exit 2; done
gzip -t "$r1" "$r2"
test ! -e "$root" || { echo "use a new run root: $root" >&2; exit 2; }
mkdir -p "$root"

salmon index -t "$catalogue" -i "$root/index" -p "$threads" \
  >"$root/index.stdout.log" 2>"$root/index.stderr.log"
salmon quant -i "$root/index" -l A -p "$threads" --meta \
  -1 "$r1" -2 "$r2" -o "$root/${id}.quant" \
  >"$root/${id}.quant.stdout.log" 2>"$root/${id}.quant.stderr.log"
```

## Key parameters

| Flag | Notes |
|------|-------|
| `--meta` | Metagenome mode — required for community catalogues |
| `-l A` | Auto library type; verify if stranded protocols used |
| Index | Rebuild after salmon major version change |

## Decision tree

```text
Abundance need?
├─ NR gene catalogue → salmon --meta
├─ Genome/MAG relative abundance → coverm
├─ Pathway/gene families from reads → humann
└─ Contig coverage for binning → coverm contig / mapper depths
```

## Validation, recovery, and provenance

Require `quant.sf`, auxiliary metadata/logs, catalogue-target agreement, unique
feature IDs, and retained paired-read accounting. Inspect inferred library type,
mapping rate, ambiguous/multimapping behavior, effective lengths, zero inflation,
and count/TPM sums. Merge samples only from the same index and version using an
explicit ordered quant-directory manifest; keep TPM and `NumReads` matrices
separate.

Rebuild indexes across incompatible major versions or catalogue changes. Record
Salmon version/implementation, index and catalogue checksum, read checksums,
library type and `--meta` status, commands, logs, per-sample QC, merge manifest,
and output checksums. TPM/counts are model-based relative quantities, not
absolute gene copies or expression without the corresponding assay context.

## Related skills

`prodigal` · `cd-hit` · `mmseqs2` · `eggnog-mapper` · `coverm` · `kneaddata` ·
`humann` · `tool-selection`
