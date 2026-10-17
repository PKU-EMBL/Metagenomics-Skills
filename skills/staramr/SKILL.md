---
name: staramr
description: >
  staramr — scan assemblies against ResFinder, PointFinder, and PlasmidFinder databases
  in one report (PHAC-NML). Use for isolate AMR + plasmid replicon summaries when you
  want CGE DBs without running each Finder separately. Route via cge-finders /
  microbial-mining; CARD catalogues still via rgi.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "staramr, CGE, ResFinder, PointFinder, PlasmidFinder, AMR, plasmid"
  metagenomics.upstream: "https://github.com/phac-nml/staramr"
  metagenomics.stage: "mining"
---

# staramr

Upstream: [phac-nml/staramr](https://github.com/phac-nml/staramr)

## Citation

Bharat, A. *et al.* Correlation between Phenotypic and In Silico Detection of
Antimicrobial Resistance in *Salmonella enterica* in Canada Using Staramr.
*Microorganisms* **10**, 292 (2022).
https://doi.org/10.3390/microorganisms10020292

Uses CGE databases — also cite ResFinder / PointFinder / PlasmidFinder papers
(see `resfinder`, `pointfinder`, `plasmidfinder`).

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

staramr is a **convenience scanner** over CGE ResFinder + PointFinder +
PlasmidFinder DBs with summary TSVs. Ideal for isolate batches and One-Health
surveillance pipelines. Still genotype-level — phenotype concordance is
organism/drug dependent.

Does **not** replace VirulenceFinder or MobileElementFinder. Does **not** use
CARD; keep `rgi` separate. For PointFinder, set the correct
`--pointfinder-organism`.

## How to run

```bash
# bioconda recommended
mamba install -c bioconda -c conda-forge staramr
staramr db update   # or pin a local DB directory
staramr search --pointfinder-organism salmonella \
  -o staramr_out assembly.fasta
# outputs include summary, resfinder, pointfinder, plasmidfinder TSVs
```

## Decision tree

```text
Need Res + Point + Plasmid in one pass?
├─ Yes (isolates) → staramr
├─ Only acquired AMR CLI → resfinder
├─ Only replicons → plasmidfinder
├─ Virulence / named MGEs → virulencefinder / mobileelementfinder
└─ CARD meta catalogue → rgi
```

## Related skills

`cge-finders` · `resfinder` · `pointfinder` · `plasmidfinder` ·
`virulencefinder` · `mobileelementfinder` · `rgi` · `mob-suite` · `genomad` ·
`microbial-mining` · `tool-selection`
