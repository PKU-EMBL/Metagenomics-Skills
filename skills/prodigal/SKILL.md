---
name: prodigal
description: >
  Protein-coding gene prediction; use -p meta for metagenomes. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "genes, orf"
  metagenomics.upstream: "https://github.com/hyattpd/Prodigal"
  metagenomics.stage: "gene"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Prodigal metagenome-mode CLI template statically reviewed; not executed here"
---

# Prodigal

Upstream: [hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)

## Citation

Hyatt, D. *et al.* Prodigal: prokaryotic gene recognition and translation initiation site identification. *BMC Bioinformatics* **11**, 119 (2010). https://doi.org/10.1186/1471-2105-11-119

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

For metagenomes always use **`-p meta`**. Gene catalogues inherit assembly
errors—garbage contigs produce garbage ORFs. Optionally keep only complete genes
(`partial=00`) when catalogs are huge.

## How to run

```bash
set -Eeuo pipefail
contigs="${1:?usage: call-genes.sh CONTIGS_FASTA OUTPUT_DIR}"
out="${2:?usage: call-genes.sh CONTIGS_FASTA OUTPUT_DIR}"
test -s "$contigs" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

prodigal -i "$contigs" -d "$out/genes.fna" -a "$out/genes.faa" \
  -o "$out/genes.gff" -p meta -f gff \
  >"$out/prodigal.stdout.log" 2>"$out/prodigal.stderr.log"
```

## Decision tree

```text
Have contigs?
├─ Build gene catalogue → prodigal → cd-hit → salmon → eggnog-mapper
└─ Only MAGs → predict genes per MAG later for annotation
```

## Validation, recovery, and provenance

Require non-empty nucleotide, protein, and GFF outputs with matching gene IDs.
Reconcile sequence counts, translation table, partial-gene flags, stop codons,
length distribution, coding density, and contigs with no calls. Preserve partial
status if filtering complete genes; do not silently discard edge-truncated ORFs.

Use fresh outputs after changing contigs, mode, or genetic code. Record Prodigal
version, input/output checksums, mode and translation table, command, logs, and
feature summary. ORFs inherit assembly errors and remain predictions.

## Related skills

`megahit` · `cd-hit` · `salmon` · `eggnog-mapper`

