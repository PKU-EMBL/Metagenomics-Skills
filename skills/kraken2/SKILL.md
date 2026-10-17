---
name: kraken2
description: >
  k-mer taxonomic classification; pair with Bracken for abundance. Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, k-mer, bracken"
  metagenomics.upstream: "https://github.com/DerrickWood/kraken2"
---

# Kraken2 (+ Bracken)

Upstream: [DerrickWood/kraken2](https://github.com/DerrickWood/kraken2) ·
Bracken: [jenniferlu717/Bracken](https://github.com/jenniferlu717/Bracken)

## Citation

Wood, D. E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. *Genome Biol.* **20**, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0

Lu, J., Breitwieser, F. P., Thielen, P. & Salzberg, S. L. Bracken: estimating species abundance in metagenomics data. *PeerJ Comput. Sci.* **3**, e104 (2017). https://doi.org/10.7717/peerj-cs.104

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Kraken2 classifies each read by **minimizer / k-mer LCA** against a database.
Sensitivity and false positives are **database-dominated** (RefSeq completeness,
eukaryotic host contamination in DB, custom biome DBs).

Bracken re-estimates abundances at a chosen rank from Kraken reports; it does
not validate rare taxa. MetaPhlAn 4 comparisons reported elevated false-positive
rates for some Bracken configurations — keep method-specific Results and avoid
“species X confirmed by both” unless thresholds are pre-registered.

Use Kraken2 for speed, custom DBs, or contig classification. Prefer MetaPhlAn
for marker specificity; Metabuli when joint DNA+AA classification is desired;
sylph for sketch containment against genome sets.

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

bracken -d $KRAKEN2_DB -i result/kraken2/${id}.report \
  -o result/kraken2/${id}.bracken -r 150 -l S
```

## Decision tree

```text
Classification goal?
├─ Broad/custom DNA DB → kraken2
├─ Species abundance smoothing → bracken after kraken2
├─ Marker SGBs → metaphlan
├─ Joint DNA+AA → metabuli
└─ Genome containment sketches → sylph
```

## Related skills

`bracken` · `metaphlan` · `metabuli` · `kaiju` · `sylph` · `visualization` · `tool-selection`
