---
name: kneaddata
description: >
  QC wrapper focused on host (and contaminant) read removal via Bowtie2. Use for
  installation, parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "host-depletion, bowtie2, qc"
  metagenomics.upstream: "https://github.com/biobakery/kneaddata"
---

# KneadData

Upstream: [biobakery/kneaddata](https://github.com/biobakery/kneaddata)

## Citation

Beghini, F. *et al.* Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. *eLife* **10**, e65088 (2021). https://doi.org/10.7554/eLife.65088

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Host reads inflate false microbial signal and waste assembly/binning compute.
KneadData’s value is **reproducible host subtraction** with a documented Bowtie2
index. Always record which host genome build you used.

Critical for PE workflows: enable **`--reorder`** so mate order stays synchronized;
MetaWRAP, salmon, and BASALT connectivity all assume paired IDs.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | QC’d PE FASTQ | From `fastp` |
| Host DB | Bowtie2 index | Matching species/build |
| RAM | 16 GB | 32 GB+ |
| Threads | 4 | 8–16 |

## How to run

```bash
conda activate kneaddata   # or bioconda install kneaddata bowtie2

kneaddata \
  -i1 temp/qc/${id}_1.fastq -i2 temp/qc/${id}_2.fastq \
  -o temp/hr \
  --bypass-trim --bypass-trf --reorder \
  --bowtie2-options '--very-sensitive --dovetail' \
  -db ${db}/kneaddata/human/hg_39 \
  --remove-intermediate-output -v -t 8
```

If fastp already trimmed, `--bypass-trim` avoids double-trimming.

## Key parameters

| Parameter | Guidance |
|-----------|----------|
| `-db` | Absolute path to Bowtie2 index prefix directory |
| `--reorder` | **Required** for PE concordance |
| `--bypass-trim` | On if upstream fastp already cleaned |
| `-t` | Threads per sample |

## Output

Paired dehosted FASTQs (names depend on KneadData version; rename consistently).

## Decision tree

```text
Host-associated matrix?
├─ Yes → KneadData with correct host index
├─ Environmental, negligible host → document skip; still keep QC
└─ Publishing human data → prefer releasing dehosted reads
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| PE count mismatch downstream | Re-run with `--reorder`; compare headers |
| Java/Trimmomatic errors | Align Java/Trimmomatic versions or bypass trim |
| Almost all reads removed | Wrong host index or extremely host-dominated library |

## Related skills

`fastp` upstream · `megahit` / `humann` / `kraken2` / `basalt` downstream

