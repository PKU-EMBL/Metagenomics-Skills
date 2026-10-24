---
name: minimap2
description: >
  Fast pairwise alignment for long reads and genome-to-genome maps. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, long-read"
  metagenomics.upstream: "https://github.com/lh3/minimap2"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Minimap2/Samtools long-read template statically reviewed; not executed here"
---

# Minimap2

Upstream: [Minimap2](https://github.com/lh3/minimap2)

## Citation

Li, H. Minimap2: pairwise alignment for nucleotide sequences. *Bioinformatics* **34**, 3094–3100 (2018). https://doi.org/10.1093/bioinformatics/bty191

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Use for ONT/PacBio→assembly (`map-ont`/`map-hifi`) and assembly polishing/scaffolding maps. Not the first choice for Illumina→contig coverage (prefer Bowtie2/BWA/strobealign).

## How to run

Choose the preset from sequencing chemistry and the biological comparison.

```bash
set -Eeuo pipefail
ref="${1:?usage: map-lr.sh REF READS OUTPUT_DIR}"
reads="${2:?usage: map-lr.sh REF READS OUTPUT_DIR}"
out="${3:?usage: map-lr.sh REF READS OUTPUT_DIR}"
threads="${THREADS:-16}"
preset="${MINIMAP_PRESET:-map-ont}"
for input in "$ref" "$reads"; do test -s "$input" || exit 2; done
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
case "$preset" in map-ont|map-pb|map-hifi|sr|asm5|asm10|asm20) ;; *) exit 2 ;; esac
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out"

minimap2 -ax "$preset" -t "$threads" "$ref" "$reads" \
  2>"$out/minimap2.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/alignment.bam" -
samtools index "$out/alignment.bam"
```

## Key parameters

| `-ax map-ont` | ONT | |
| `-ax map-hifi` | PacBio HiFi | |
| `-ax sr` | short reads | OK but Bowtie2/BWA often preferred |

## Decision notes

- Stage: **mapping** (long reads / genome-to-genome)
- Prefer for ONT/PacBio→contigs and assembly polish maps; not default Illumina coverage mapper

## Validation, recovery, and provenance

```bash
samtools quickcheck -v "$out/alignment.bam"
samtools view -H "$out/alignment.bam" | grep -q '^@HD.*SO:coordinate'
test -s "$out/alignment.bam.bai"
samtools flagstat -@ 4 -O tsv "$out/alignment.bam" >"$out/flagstat.tsv"
samtools coverage "$out/alignment.bam" >"$out/coverage.tsv"
```

Review mapping identity/coverage, supplementary/secondary alignment policy,
reference names, and coverage heterogeneity for the intended downstream tool.
Assembly-to-assembly presets and read-to-assembly presets answer different
questions. Record Minimap2/Samtools versions, preset and filters, reference/read
checksums, commands, logs, BAM checksum, and QC tables. Rerun failed streams into
a fresh directory.

## Related skills

`bowtie2` · `bwa` · `metaflye` · `metamdbg` · `samtools` · `tool-selection` ·
`metagenomics-workflow`
