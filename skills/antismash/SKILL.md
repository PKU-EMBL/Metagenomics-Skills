---
name: antismash
description: >
  Detect and annotate biosynthetic gene clusters (BGCs) on genomes and MAGs. Use for
  natural-product genome mining, choosing genefinding, interpreting region HTML/JSON,
  and stating validation limits.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "BGC, secondary-metabolite, genome-mining"
  metagenomics.upstream: "https://github.com/antismash/antismash"
  metagenomics.stage: "mining"
---

# antiSMASH

Upstream: [antismash/antismash](https://github.com/antismash/antismash)

## Citation

Blin, K. *et al.* antiSMASH 7.0: new and improved predictions for detection,
regulation, chemical structures and visualisation. *Nucleic Acids Res.* **51**,
W46–W50 (2023). https://doi.org/10.1093/nar/gkad344

## Analytical thinking

antiSMASH finds **BGC regions** (PKS, NRPS, RiPP, terpene, …). It does **not**
prove a compound is produced. Fragmented MAGs truncate clusters — prefer
near-complete bins (`checkm2` / `mag-qc`) and note contig breaks inside regions.

Run on **per-genome FASTA** (or GenBank from `bakta`/`prokka`), not mixed
community contigs, unless you explicitly want contig-level screens and will
not assign clusters to species without binning.

Record antiSMASH version **and** database download date. For comparative BGC
families across MAGs, follow with BiG-SCAPE (`bigscape`).

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Input | Genome/MAG FASTA | Completeness ≥50–70% for claims |
| DBs | `download-antismash-databases` | Shared read-only path |
| CPU | 8 | 16+ |
| Gene finding | prodigal (meta/MAGs) | Or use Bakta GenBank |

## How to run

```bash
conda install -c bioconda antismash
download-antismash-databases

# From nucleotide FASTA (MAG)
antismash bins/HQ_bin.fa \
  --output-dir temp/antismash/${id} \
  --html-title ${id} \
  --cpus 16 \
  --genefinding-tool prodigal \
  --taxon bacteria

# From Bakta/Prokka GenBank (preferred when available)
antismash temp/bakta/${id}/${id}.gbff \
  --output-dir temp/antismash/${id} \
  --cpus 16
```

## Key parameters

| Option | Guidance |
|--------|----------|
| `--genefinding-tool prodigal` | Default for MAG FASTA |
| `--taxon bacteria/fungi` | Affects rules; match organism |
| `--cb-knownclusters` / MiBIG opts | Enable when comparing to known BGCs (version-dependent) |
| `--minimal` | Faster, fewer analyses — for screens only |

## Outputs to archive

| Path | Meaning |
|------|---------|
| `index.html` | Interactive regions |
| `*.json` / region GenBanks | Machine-readable clusters |
| stdout cluster counts | Summary for tables |

## Decision tree

```text
BGC mining goal?
├─ Single HQ MAG → bakta/prokka → antismash → (optional) bigscape
├─ Many MAGs catalogue → filter by checkm2 first, then batch antismash
└─ Need AMP smORFs not BGCs → macrel (different claim)
```

## Troubleshooting

| Symptom | Action |
|---------|--------|
| DB missing errors | Re-run `download-antismash-databases` |
| Zero clusters on huge MAG | Check prodigal ran; try GenBank input |
| Huge runtime | Use `--minimal` for pilot; full mode for finals |

## Related skills

`microbial-mining` · `bakta` · `prokka` · `bigscape` · `dram` · `checkm2` · `mag-qc`
