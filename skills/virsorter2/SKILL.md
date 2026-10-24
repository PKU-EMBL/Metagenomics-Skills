---
name: virsorter2
description: >
  Viral sequence identification from metagenomic assemblies. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "virus, phage, genome-mining"
  metagenomics.upstream: "https://github.com/jiarong/VirSorter2"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "run/setup output contract checked against upstream documentation; not executed here"
---

# VirSorter2

Upstream: [VirSorter2](https://github.com/jiarong/VirSorter2)

## Citation

Guo, J. *et al.* VirSorter2: a multi-classifier, expert-guided approach to detect diverse DNA and RNA viruses. *Microbiome* **9**, 37 (2021). https://doi.org/10.1186/s40168-020-00990-y

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Classic viral contig mining. Pair with **CheckV** for quality and optionally geNomad for cross-method consensus. Viral taxonomy is a separate claim from bacterial MAG taxonomy.

## How to run

Install the database once with `virsorter setup -d <pinned-db> -j <n>`, verify
completion, and freeze it for the cohort. The current default groups are not all
available viral groups, so state the chosen scope explicitly.

```bash
set -Eeuo pipefail
contigs="${1:?usage: run-virsorter2.sh CONTIGS_FASTA OUTPUT_DIR}"
out="${2:?usage: run-virsorter2.sh CONTIGS_FASTA OUTPUT_DIR}"
threads="${THREADS:-16}"
groups="${VIRSORTER_GROUPS:-dsDNAphage,ssDNA}"
test -s "$contigs" || exit 2
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "${out}.logs"

virsorter run -w "$out" -i "$contigs" --min-length 1500 \
  --include-groups "$groups" -j "$threads" all \
  >"${out}.logs/virsorter.stdout.log" 2>"${out}.logs/virsorter.stderr.log"
test -f "$out/final-viral-combined.fa"
test -s "$out/final-viral-score.tsv"
test -s "$out/final-viral-boundary.tsv"
```

## Key parameters

| `--min-length` | 1500+ | Reduce noise |
| DB | vs2 setup | Once |

## Decision notes

- Run mining on **QC-filtered genomes/MAGs** (or contigs for MGE/virus screens)
- Computational hits are hypotheses — state validation limits in Methods
- Pin software + database releases

## Validation, recovery, and provenance

Require combined viral FASTA, score and boundary tables, logs, and an audit of
all input sequences. Inspect selected groups, score and length distributions,
hallmark genes, full/partial/`lt2gene` suffixes, duplicate/overlapping fragments,
contig-edge status, and host-rich false-positive risk. Apply CheckV and, where
useful, an independently modeled caller before defining a high-confidence set.

VirSorter2 can resume a compatible interrupted work directory, but use fresh
outputs after changing input, database, groups, or major options. Record
VirSorter2/Snakemake/dependency versions, database source/version/checksum,
input checksum, complete command, logs, output checksums, and downstream filters.
A viral score is not taxonomy, completeness, infectivity, or host assignment.

## Related skills

`checkv` · `genomad` · `megahit` · `microbial-mining` · `tool-selection` ·
`metagenomics-workflow`
