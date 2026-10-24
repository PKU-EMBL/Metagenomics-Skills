---
name: plass
description: >
  PLASS — protein-level assembler that recovers many more protein sequences from
  metagenomic reads than nucleotide assembly alone (Söding / Steinegger). Same package
  ships PenguiN (protein-guided nucleotide assembly). Use when: (1) Maximizing protein
  catalogue recovery from reads, (2) Building inputs for MMseqs/HH-suite/BFD-style
  search, (3) Viral/strain-resolved assemblies via PenguiN. Route via homology-search /
  assembly stages.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "PLASS, PenguiN, assembly, protein, metagenomics"
  metagenomics.upstream: "https://github.com/soedinglab/plass"
  metagenomics.stage: "assembly"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "paired/single assemble interface checked against current upstream README; not executed here"
---

# PLASS / PenguiN

Upstream: [soedinglab/plass](https://github.com/soedinglab/plass)

## Citation

Steinegger, M., Mirdita, M. & Söding, J. Protein-level assembly increases
protein sequence recovery from metagenomic samples manyfold. *Nat. Methods*
**16**, 603–606 (2019). https://doi.org/10.1038/s41592-019-0437-4

Jochheim, A. *et al.* Strain-resolved de-novo metagenomic assembly of viral
genomes and microbial 16S rRNAs. *Microbiome* **12**, 187 (2024).
https://doi.org/10.1186/s40168-024-01904-y

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Nucleotide assemblers miss many coding sequences. **PLASS** assembles at the
**protein** level from reads → denser protein catalogues for search/annotation.
**PenguiN** uses protein guidance for nucleotide assemblies (viruses/16S use
cases in the paper). Complements MEGAHIT/metaSPAdes, does not replace contig
binning paths.

Soil/Marine reference catalogues from PLASS and BFD HH-suite DBs are linked
from upstream.

## How to run

This paired-end template preserves explicit mate identity and writes a protein
catalogue, not nucleotide contigs.

```bash
set -Eeuo pipefail
r1="${1:?usage: run-plass.sh R1_FASTQ R2_FASTQ OUTPUT_DIR}"
r2="${2:?usage: run-plass.sh R1_FASTQ R2_FASTQ OUTPUT_DIR}"
out="${3:?usage: run-plass.sh R1_FASTQ R2_FASTQ OUTPUT_DIR}"
threads="${THREADS:-16}"
for file in "$r1" "$r2"; do
  test -s "$file" || exit 2
  [[ "$file" != *.gz ]] || gzip -t "$file"
done
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/tmp"
plass assemble "$r1" "$r2" "$out/proteins.fasta" "$out/tmp" \
  --threads "$threads" >"$out/plass.stdout.log" 2>"$out/plass.stderr.log"
test -s "$out/proteins.fasta"
seqkit stats -T "$out/proteins.fasta" >"$out/protein-stats.tsv"
```

Single-end input uses the distinct three-positional-argument form. PenguiN
nucleotide assembly is a separate `penguin guided_nuclassemble` workflow.

## Decision tree

```text
Goal from metagenomic reads?
├─ Contigs for binning → megahit / metaspades
├─ Maximize protein recovery for search → plass
├─ Protein-guided nt assembly (viruses/…) → penguin (plass package)
└─ Then search proteins → mmseqs2 / hh-suite / foldseek
```

## Validation, recovery, and provenance

Require valid protein FASTA, statistics, logs and an input/read reconciliation.
Inspect sequence count/length, invalid residues, redundancy, low-complexity,
short ORFs, known marker recovery, parameter sensitivity, and comparison with
proteins predicted from nucleotide assemblies. PLASS proteins lack contig,
coverage, neighborhood and bin context unless independently linked.

Use fresh output after changing reads, parameters, binary, or mode. Record PLASS
version/build, paired input checksums and library provenance, command/logs,
temporary-space policy, output checksum/statistics, clustering/deduplication and
annotation settings. Protein recovery is not proof of a complete gene, genome,
organism, or expressed product.

## Related skills

`megahit` · `metaspades` · `mmseqs2` · `hh-suite` · `homology-search` ·
`prodigal` · `tool-selection`
