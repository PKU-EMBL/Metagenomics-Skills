---
name: metabolic
description: >
  METABOLIC (AnantharamanLab) — high-throughput metabolic and biogeochemical trait
  profiling of MAGs/SAGs/isolates with C, N, S, and other elemental cycle diagrams
  (METABOLIC-G genomes-only; METABOLIC-C with reads / community networks). Use for
  multi-element cycling potential and MW-score networks. Fe-deep dive → fegenie; S
  entropy scores → mebs.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "METABOLIC, biogeochemistry, C, N, S, P, element-cycling, MAG"
  metagenomics.upstream: "https://github.com/AnantharamanLab/METABOLIC"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed-legacy"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.upstream-version: "4.0 interface"
  metagenomics.command-status: "METABOLIC-G/C input contracts checked against upstream wiki; not executed here"
---

# METABOLIC

Upstream: [AnantharamanLab/METABOLIC](https://github.com/AnantharamanLab/METABOLIC)

## Citation

Zhou, Z. *et al.* METABOLIC: high-throughput profiling of microbial genomes for
functional traits, metabolism, biogeochemistry, and community-scale functional
networks. *Microbiome* **10**, 33 (2022).
https://doi.org/10.1186/s40168-021-01213-8

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

METABOLIC annotates genomes then draws **biogeochemical cycle** summaries —
commonly **carbon (C)**, **nitrogen (N)**, **sulfur (S)**, plus **other**
transformations (H₂, metals/metalloids as covered by the HMM/KOfam template).
Use **METABOLIC-G.pl** without reads; **METABOLIC-C.pl** when metagenomic reads
enable coverage / community contribution diagrams (MW-score, Sankey, networks).

| Element focus | Role of METABOLIC |
|---------------|-------------------|
| C | Fixation and organic C transformations |
| N | Fixation, nitrification, denitrification, anammox, … |
| S | Oxidative/reductive sulfur steps |
| P / H₂ / others | Via modules / “other” cycle panels — pin template version |
| Fe | Present at trait level; deep Fe → `fegenie` |

Heavy DB install (KOfam etc.). Pin METABOLIC version, module cutoff, and DB.

## How to run

METABOLIC expects its scripts and dependent databases together. The genome
folder must contain only `.fasta` genomes with globally unique sequence IDs.
Use absolute paths because this template runs from the pinned METABOLIC root.

```bash
set -Eeuo pipefail
home="${METABOLIC_HOME:?set METABOLIC_HOME to a pinned v4.0 checkout}"
genomes="${1:?usage: run-metabolic-g.sh ABS_GENOME_DIR ABS_OUTPUT_DIR}"
out="${2:?usage: run-metabolic-g.sh ABS_GENOME_DIR ABS_OUTPUT_DIR}"
threads="${THREADS:-20}"
[[ "$genomes" = /* && "$out" = /* ]] || exit 2
test -f "$home/METABOLIC-G.pl" && test -d "$genomes" || exit 2
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
shopt -s nullglob
genome_files=("$genomes"/*.fasta)
((${#genome_files[@]} > 0)) || exit 2
if find "$genomes" -maxdepth 1 -type f ! -name '*.fasta' -print -quit | grep -q .; then
  echo "genome directory must contain only .fasta files" >&2; exit 2
fi
awk '/^>/{id=$1; sub(/^>/,"",id); if (++seen[id]>1) exit 1}' \
  "${genome_files[@]}"
mkdir -p "$(dirname "$out")" "${out}.logs"

(
  cd "$home"
  perl ./METABOLIC-G.pl -t "$threads" -m-cutoff 0.75 \
    -in-gn "$genomes" -kofam-db full -o "$out"
) >"${out}.logs/METABOLIC-G.stdout.log" \
  2>"${out}.logs/METABOLIC-G.stderr.log"
test -s "$out/METABOLIC_run.log"
find "$out" -type f -name 'METABOLIC_result.xlsx' -size +0c -print -quit | grep -q .
```

For METABOLIC-C, provide nucleotide `.fasta` genomes and a text file whose each
line is an absolute `R1.fastq,R2.fastq` pair to `-r`; verify equal pair counts and
do not collapse mates. Record `-rt`, `-st`, `-tax`, and mapping behavior.

## Decision tree

```text
Multi-element biogeochem on MAGs?
├─ Genomes ± reads → metabolic (G or C)
├─ S-centric entropy → mebs
├─ Fe genes/siderophores → fegenie
└─ Distilled sheets → dram
```

## Validation, recovery, and provenance

Require run/log files, gene and KEGG hit tables, module/trait matrices, result
workbook, figure inputs, and an input-genome reconciliation including no-hit or
failed genomes. Inspect unique IDs, HMM/motif support, module cutoff sensitivity,
MAG completeness/contamination, pathway missing steps, coverage units, taxonomic
aggregation, and whether figures agree with source tables.

Do not reuse partial outputs except through the documented second-run workflow.
Record METABOLIC code commit/release, KOfam and bundled HMM/template checksums,
all dependency versions, genome/read manifests and checksums, every option,
commands, logs, intermediate/output checksums, and exclusions. Trait calls and
MW-scores describe predicted potential/relative contribution, not process rates.

## Related skills

`element-cycling` · `mebs` · `fegenie` · `dram` · `kegg` · `gapseq` ·
`microbial-mining` · `tool-selection`
