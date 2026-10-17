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

```bash
conda install -c bioconda bowtie2 samtools

mkdir -p temp/map
bowtie2-build --threads 8 contigs.fa temp/map/contigs

bowtie2 -x temp/map/contigs \
  -1 temp/hr/${id}_1.fastq -2 temp/hr/${id}_2.fastq \
  -p 16 --very-sensitive-local \
  2> temp/map/${id}.bowtie2.log \
  | samtools sort -@ 8 -o temp/map/${id}.bam
samtools index temp/map/${id}.bam

# Multi-sample depth for MetaBAT2
jgi_summarize_bam_contig_depths --outputDepth temp/map/depth.txt temp/map/*.bam
```

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
samtools flagstat temp/map/${id}.bam
# Typical clean metagenomes: often 50–90% mapped; near-0% ⇒ wrong contigs/reads
```

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
