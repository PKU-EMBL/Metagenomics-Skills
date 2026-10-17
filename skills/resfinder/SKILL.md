---
name: resfinder
description: >
  ResFinder — CGE identification of acquired antimicrobial resistance genes (and
  optional PointFinder chromosomal mutations / DisinFinder biocide genes) from
  assemblies or reads. Use for isolate resistome typing with ResFinder DB phenotype
  mapping. Route via cge-finders / microbial-mining; biocide-only → disinfinder;
  complement with rgi (CARD) and deeparg — keep tables separate.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "ResFinder, CGE, AMR, resistome, PointFinder, DisinFinder"
  metagenomics.upstream: "https://github.com/genomicepidemiology/resfinder"
  metagenomics.stage: "mining"
---

# ResFinder

Upstream: [genomicepidemiology/resfinder](https://github.com/genomicepidemiology/resfinder) ·
DB: [resfinder_db](https://bitbucket.org/genomicepidemiology/resfinder_db)

## Citation

Zankari, E. *et al.* Identification of acquired antimicrobial resistance genes.
*J. Antimicrob. Chemother.* **67**, 2640–2644 (2012).
https://doi.org/10.1093/jac/dks261

Bortolaia, V. *et al.* ResFinder 4.0 for predictions of phenotypes from
genotypes. *J. Antimicrob. Chemother.* **75**, 3491–3500 (2020).
https://doi.org/10.1093/jac/dkaa345

Bortolaia, V. *et al.* ResFinder – an open online resource for identification of
antimicrobial resistance genes in next-generation sequencing data and prediction
of phenotypes from genotypes. *J. Antimicrob. Chemother.* **77**, e1–e10 (2022).
https://doi.org/10.1093/jac/dkac018

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

ResFinder detects **acquired** AMR genes against the CGE ResFinder DB and can
emit genotype→phenotype summaries for supported taxa. Optional PointFinder
(`-c` / point DB) adds chromosomal resistance mutations; DisinFinder covers
selected disinfectant resistance markers when databases are installed.

**Not** interchangeable with CARD/`rgi` ontology. Genotype prediction ≠ MIC /
treatment guidance. For metagenomes, prefer gene catalogues + `rgi`/`deeparg`
and treat ResFinder as isolate/HQ-MAG screening.

## How to run

```bash
# install resfinder + clone resfinder_db (± pointfinder_db, disinfinder_db)
python -m resfinder -ifa assembly.fasta -o resfinder_out \
  -db_res /path/to/resfinder_db \
  -l 0.6 -t 0.9
# chromosomal mutations (species-aware):
python -m resfinder -ifa assembly.fasta -o resfinder_out \
  -db_res /path/to/resfinder_db -db_point /path/to/pointfinder_db -c
# convenience wrapper for Res+Point+Plasmid DBs → staramr
```

Pin ResFinder software and **all** DB versions used.

## Decision tree

```text
Resistome claim?
├─ CGE acquired AMR (+ optional phenotype map) → resfinder
├─ Chromosomal AMR SNPs → pointfinder / resfinder -c
├─ Biocide / disinfectant genes → disinfinder
├─ Combined Res+Point+Plasmid → staramr
├─ Multi-DB screen → abricate
├─ CARD catalogue / meta gene catalogue → rgi
├─ ML complement → deeparg (separate table)
└─ Plasmid context → plasmidfinder / pmlst / genomad / mob-suite ∩ hits
```

## Related skills

`cge-finders` · `pointfinder` · `disinfinder` · `plasmidfinder` · `pmlst` ·
`staramr` · `abricate` · `rgi` · `deeparg` · `virulencefinder` ·
`mobileelementfinder` · `genomad` · `microbial-mining` · `tool-selection`
