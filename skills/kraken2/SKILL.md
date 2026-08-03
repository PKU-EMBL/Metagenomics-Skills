---
name: kraken2
description: >
  k-mer taxonomic classification; pair with Bracken for abundance. Use this skill when working with kraken2: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/DerrickWood/kraken2. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'k-mer', 'bracken']
upstream: https://github.com/DerrickWood/kraken2
---

# Kraken2 (+ Bracken)

Upstream: [DerrickWood/kraken2](https://github.com/DerrickWood/kraken2) ·
Bracken: [jenniferlu717/Bracken](https://github.com/jenniferlu717/Bracken)

## Citation

Wood, D. E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. *Genome Biol.* **20**, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0

See also [docs/references.md](../../docs/references.md).

## Analytical thinking

Kraken2 classifies each read by k-mer LCA against a database. Sensitivity and
false positives are **database-dominated**. Bracken re-estimates abundances at a
chosen rank; it does not magically validate rare taxa.

Use Kraken2 when you need speed, custom DBs, or contig classification. Prefer
MetaPhlAn when marker specificity matters more than breadth.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| DB | Built Kraken2 DB | Standard or custom; huge disk |
| RAM | Often ≥ DB size resident | 64–200 GB+ depending on DB |
| Input | FASTQ or FASTA | Dehosted preferred |

## How to run

```bash
kraken2 --db $KRAKEN2_DB --paired \
  temp/hr/${id}_1.fastq temp/hr/${id}_2.fastq \
  --report result/kraken2/${id}.report \
  --output result/kraken2/${id}.kraken \
  --threads 16

# abundance re-estimation (install Bracken separately)
bracken -d $KRAKEN2_DB -i result/kraken2/${id}.report \
  -o result/kraken2/${id}.bracken -l S
```

## Decision tree

```text
Classification goal?
├─ Broad/custom DB → kraken2
├─ Species abundance smoothing → bracken after kraken2
└─ Marker-based clades → metaphlan
```

## Related skills

`metaphlan` · `humann` · `visualization` · `metawrap` (can wrap Kraken modules)

