---
name: isescan
description: >
  ISEScan — automated annotation of insertion sequence (IS) elements in prokaryotic
  genomes via profile HMMs. Use for IS family catalogues on MAGs or contigs as part of
  MGE refinement beyond geNomad. Route via microbial-mining; pair with mobileog /
  integronfinder.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ISEScan, IS, insertion-sequence, MGE, genome-mining"
  metagenomics.upstream: "https://github.com/xiezhq/ISEScan"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "seqfile/output/nthread interface checked against upstream 1.7 documentation; not executed here"
---

# ISEScan

Upstream: [xiezhq/ISEScan](https://github.com/xiezhq/ISEScan)

## Citation

Xie, Z. & Tang, H. ISEScan: automated identification of insertion sequence
elements in prokaryotic genomes. *Bioinformatics* **33**, 3340–3347 (2017).
https://doi.org/10.1093/bioinformatics/btx433

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

IS elements drive rearrangements and can flank ARGs/BGCs. ISEScan reports IS
families/copies; it does **not** replace plasmid/virus classifiers (`genomad`)
or integron detection (`integronfinder`).

## How to run

ISEScan is Linux-oriented and depends on a compatible FragGeneScan release.
Run each assembly into a fresh directory; complete and partial IS calls are both
reported by default.

```bash
set -Eeuo pipefail
genome="${1:?usage: run-isescan.sh GENOME_FASTA OUTPUT_DIR}"
out="${2:?usage: run-isescan.sh GENOME_FASTA OUTPUT_DIR}"
threads="${THREADS:-4}"
test -s "$genome" || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

isescan.py --seqfile "$genome" --output "$out" --nthread "$threads" \
  >"$out/isescan.stdout.log" 2>"$out/isescan.stderr.log"
find "$out" -type f -name '*.tsv' -size +0c -print -quit | grep -q .
find "$out" -type f -name '*.gff' -size +0c -print -quit | grep -q .
```

## Decision tree

```text
Need IS annotation?
├─ Yes → isescan
├─ Broader MGE proteins → mobileog
├─ Integrons → integronfinder
└─ Plasmid/virus contigs → genomad
```

## Validation, recovery, and provenance

Require summary, TSV/CSV, GFF, nucleotide/protein FASTA, and logs, including
valid zero-hit files. Check sequence-ID uniqueness, coordinate bounds, TIRs,
transposase support, complete-versus-partial status, family assignment,
duplicate/overlapping calls, and contig-edge truncation. Inspect IS context
around genes of interest rather than inferring mobility from proximity alone.

Use fresh outputs after changing assemblies, HMMs, dependencies, or parameters.
Record ISEScan, FragGeneScan, HMMER, BLAST and HMM-library versions/checksums,
input checksum, command, logs, result checksums, and post-filter rules. Predicted
IS structure is not direct evidence that a neighboring gene transferred.

## Related skills

`mobileog` · `integronfinder` · `genomad` · `rgi` · `microbial-mining` ·
`tool-selection`
