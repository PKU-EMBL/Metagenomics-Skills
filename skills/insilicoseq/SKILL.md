---
name: insilicoseq
description: >
  InSilicoSeq — simulate realistic Illumina (meta)genomic reads for benchmarking and
  experimental design. Use when: (1) Generating Illumina-like test sets from genomes,
  (2) Simple abundance-controlled mock communities, (3) Complementing CAMISIM for
  CAMI-style community simulation. For full CAMI gold standards prefer cami / CAMISIM.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "simulation, Illumina, benchmark, InSilicoSeq"
  metagenomics.upstream: "https://github.com/HadrienG/InSilicoSeq"
  metagenomics.stage: "assessment"
---

# InSilicoSeq

Upstream: [HadrienG/InSilicoSeq](https://github.com/HadrienG/InSilicoSeq) ·
Docs: https://insilicoseq.readthedocs.io/

## Citation

Gourlé, H., Karlsson-Lindsjö, O., Hayer, J. & Bongcam-Rudloff, E. Simulating
Illumina metagenomic data with InSilicoSeq. *Bioinformatics* **35**, 521–522
(2019). https://doi.org/10.1093/bioinformatics/bty630

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

| Simulator | Strength |
|-----------|----------|
| `insilicoseq` | Fast Illumina metagenome reads; simple CLI |
| CAMISIM (`cami`) | Multi-sample designs, strain diversity, CAMI gold standards |

Use InSilicoSeq for lightweight tool tests; use CAMISIM/CAMI when you need
challenge-grade gold standards for assembly/binning/profiling.

## How to run

```bash
conda install -c conda-forge -c bioconda insilicoseq
iss generate --genomes genome1.fa genome2.fa --model NovaSeq \
  --abundance_file abundances.txt --output temp/iss/mock --n_reads 5M
```

## Related skills

`cami` · `quast` · `metaphlan` · `kraken2` · `tool-selection`
