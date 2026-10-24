---
name: bowtie2
description: >
  Gapped short-read alignment to contigs/genomes for coverage used in binning and
  abundance. Use when indexing assemblies, mapping cleaned PE reads, choosing
  sensitivity presets, QC of BAM rates, or preparing depths for MetaBAT2/CoverM/BASALT.
  Alternatives: strobealign, bwa-mem2. Always pair with samtools.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "mapping, alignment, short-read, coverage"
  metagenomics.upstream: "https://github.com/BenLangmead/bowtie2"
  metagenomics.stage: "mapping"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-24"
  metagenomics.command-status: "Bowtie2/Samtools paired-end coverage template statically reviewed; not executed here"
---

# Bowtie 2

Upstream: [BenLangmead/bowtie2](https://github.com/BenLangmead/bowtie2)

## Citation

Langmead, B. & Salzberg, S. L. Fast gapped-read alignment with Bowtie 2.
*Nat. Methods* **9**, 357–359 (2012). https://doi.org/10.1038/nmeth.1923

## Analytical thinking

Mapping is the bridge from **assembly → binning**. Coverage profiles (not raw
reads) drive MetaBAT2/MaxBin2/CONCOCT/SemiBin2 and inform BASALT. Index **once
per assembly**; map every sample that should contribute coverage.

Use the **same cleaned PE reads** that fed assembly (or the declared coverage
set from `study-design`). Mixing host-contaminated and dehosted libraries
silently biases bins.

Presets trade sensitivity vs speed: `--sensitive` / `--very-sensitive` for
catalogue work; `--very-sensitive-local` allows soft-clipping useful on
fragmented metagenome contigs. Do not treat higher sensitivity as “more true
species”.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Contigs | FASTA from assembly | Filtered min-length if huge |
| Reads | Clean PE FASTQ | From `kneaddata` |
| Tools | bowtie2 + samtools | Same env |
| Threads | 8 | 16–32 |
| Disk | BAM ≈ 1–2× read set | Keep sorted BAM + `.bai` |

## How to run

Build one index per immutable assembly, then map each manifest-defined read pair
into a separate output directory.

```bash
set -Eeuo pipefail
id="${1:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
ref="${2:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
r1="${3:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
r2="${4:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
out="${5:?usage: map-one.sh SAMPLE_ID REF R1 R2 OUTPUT_DIR}"
threads="${THREADS:-16}"
[[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || exit 2
for input in "$ref" "$r1" "$r2"; do test -s "$input" || exit 2; done
[[ "$threads" =~ ^[1-9][0-9]*$ ]] || exit 2
test ! -e "$out" || { echo "use a new output directory: $out" >&2; exit 2; }
mkdir -p "$out/index"

bowtie2-build --threads "$threads" "$ref" "$out/index/reference" \
  >"$out/bowtie2-build.stdout.log" 2>"$out/bowtie2-build.stderr.log"
bowtie2 -x "$out/index/reference" -1 "$r1" -2 "$r2" \
  -p "$threads" --very-sensitive-local \
  2>"$out/${id}.bowtie2.stderr.log" \
  | samtools sort -@ "$threads" -o "$out/${id}.bam" -
samtools index "$out/${id}.bam"
```

For multi-sample binning, build the depth table from an explicit, ordered BAM
manifest; do not rely on an unreviewed wildcard or mix references/mappers.

## Key parameters

| Option | Guidance |
|--------|----------|
| `-x` | Index prefix from `bowtie2-build` |
| `-1/-2` | PE mates; keep order from KneadData `--reorder` |
| `-U` | SE only when truly single-end |
| `-p` | Threads (aligner); samtools sort uses `-@` |
| `--very-sensitive-local` | Soft-clip friendly on short contigs |
| `--no-unal` | Smaller SAM/BAM; lose unmapped diagnostics |

## Output & QC

| Artifact | Use |
|----------|-----|
| `${id}.bam` + `.bai` | CoverM, binners, inStrain |
| `depth.txt` | MetaBAT2 `-a` |
| stderr overall alignment rate | Library/assembly sanity |

```bash
samtools quickcheck -v "$out/${id}.bam"
samtools view -H "$out/${id}.bam" | grep -q '^@HD.*SO:coordinate'
test -s "$out/${id}.bam.bai"
samtools flagstat -@ 4 -O tsv "$out/${id}.bam" >"$out/${id}.flagstat.tsv"
samtools idxstats "$out/${id}.bam" >"$out/${id}.idxstats.tsv"
```

Inspect paired/primary mapping, insert-size behavior, reference names, and depth
rather than applying a universal mapping-rate cutoff. Preserve Bowtie2/Samtools
versions, reference/read checksums, sensitivity and alignment-policy flags,
commands, logs, BAM checksum, and QC tables. Failed streams can leave partial
BAMs; only expose downstream after these checks pass.

## Decision tree

```text
Illumina → contig coverage?
├─ Large cohort / speed critical → strobealign (or bwa-mem2)
├─ Lab standard / KneadData ecosystem → bowtie2
└─ Long reads → minimap2 (not bowtie2)
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| ~0% mapped | Contigs/reads mismatch; wrong sample IDs |
| PE sync errors | Re-KneadData with `--reorder` |
| `bowtie2-build` RAM blowup | Split huge contig sets or raise node RAM |
| Unsorted BAM breaks MetaBAT | Always `samtools sort` + `index` |

## Related skills

`samtools` · `strobealign` · `bwa-mem2` · `coverm` · `metabat2` · `basalt` · `study-design`
