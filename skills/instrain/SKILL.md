---
name: instrain
description: >
  Strain-level microdiversity and shared-strain detection from metagenomes. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "strain, microdiversity, snp"
  metagenomics.upstream: "https://github.com/MrOlm/inStrain"
  metagenomics.stage: "strain"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "profile/compare interfaces checked against current user manual; not executed here"
---

# inStrain

Upstream: [inStrain](https://github.com/MrOlm/inStrain)

## Citation

Olm, M. R. *et al.* inStrain profiles population microdiversity from metagenomic data and sensitively detects shared microbial strains. *Nat. Biotechnol.* **39**, 727–736 (2021). https://doi.org/10.1038/s41587-020-00797-0

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Species-level profilers (MetaPhlAn, Kraken, sylph) and MAG catalogues do not
resolve **within-species** SNP microdiversity or prove strain sharing across
samples. inStrain profiles diversity from reads mapped to genomes/MAGs and
detects shared strains with sensitive comparisons.

Requirements for trustworthy results:

- High-quality mapping to **dereplicated**, preferably high-completeness genomes
- Adequate breadth/depth of coverage (tool filters — report them)
- Not a replacement for species profiling or for ANI catalogue building (`drep` /
  `skani`)

Typical order: bin → CheckM2/GUNC → dRep → map reads → `inStrain profile` →
optional compare for shared strains.

## How to run

Profile one sample against the same dereplicated reference used to build its BAM.
Optional `INSTRAIN_STB` must be a coordinate-matched scaffold-to-bin TSV.

```bash
set -Eeuo pipefail
bam="${1:?usage: profile-instrain.sh SORTED_BAM REFERENCE_FASTA OUTPUT_DIR}"
reference="${2:?usage: profile-instrain.sh SORTED_BAM REFERENCE_FASTA OUTPUT_DIR}"
out="${3:?usage: profile-instrain.sh SORTED_BAM REFERENCE_FASTA OUTPUT_DIR}"
threads="${THREADS:-16}"
test -s "$bam" && test -s "$reference" || exit 2
test -s "$bam.bai" || test -s "${bam%.bam}.bai" || exit 2
samtools quickcheck "$bam"
test ! -e "$out" && test ! -e "${out}.logs" || {
  echo "use new output and log paths" >&2; exit 2;
}
mkdir -p "$(dirname "$out")" "${out}.logs"
stb_args=()
if [[ -n "${INSTRAIN_STB:-}" ]]; then
  test -s "$INSTRAIN_STB" || exit 2
  stb_args=(-s "$INSTRAIN_STB")
fi
inStrain profile "$bam" "$reference" -o "$out" -p "$threads" \
  "${stb_args[@]}" >"${out}.logs/profile.stdout.log" \
  2>"${out}.logs/profile.stderr.log"
test -s "$out/output/scaffold_info.tsv"
test -s "$out/output/mapping_info.tsv"
```

For cohort comparison, build an ordered list of completed profiles mapped to the
identical reference, then run `inStrain compare -i <profiles...> -o <fresh-out>
-p <threads>`. Require `output/comparisonsTable.tsv`; record coverage overlap,
minimum coverage/frequency, ANI and clustering thresholds.

## Key parameters

| Input | Notes |
|-------|-------|
| BAM | To dereplicated references; consistent mapper |
| Coverage / breadth filters | Record the installed defaults and predeclare every override |
| `compare` | Shared-strain detection across profiles |

## Validation, recovery, and provenance

Inspect mapping/read-filter retention, breadth, depth, expected breadth,
read-to-reference ANI, SNV/SNS counts, linkage, scaffold/genome summaries, and
callability before comparing samples. Shared-strain calls require comparable
profiles, sufficient overlap, threshold sensitivity, and background prevalence;
they do not by themselves prove transmission.

Use fresh outputs after changing BAM, reference, STB, filters, or release. Record
inStrain/mapper/samtools versions, identical reference and BAM checksums, mapping
parameters, STB, profile/compare commands, logs, native objects and table
checksums, all thresholds, and excluded sample pairs. Never compare profiles
built against different FASTA content/order without documented reconciliation.

## Related skills

`bowtie2` · `strobealign` · `drep` · `skani` · `coverm` · `metaphlan` ·
`strain-resolved-analysis` · `strain-transmission` · `tool-selection` ·
`metagenomics-workflow`
