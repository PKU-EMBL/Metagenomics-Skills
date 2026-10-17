---
name: virulencefinder
description: >
  VirulenceFinder — CGE virulence gene detection in bacterial assemblies/reads for
  supported species (historically E. coli, Enterococcus, S. aureus, Listeria, …). Route
  via cge-finders / microbial-mining; not a general metagenome pathogenicity score.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "VirulenceFinder, CGE, virulence, pathogen, isolate, typing"
  metagenomics.upstream: "https://bitbucket.org/genomicepidemiology/virulencefinder"
  metagenomics.stage: "mining"
---

# VirulenceFinder

Upstream: [virulencefinder](https://bitbucket.org/genomicepidemiology/virulencefinder) ·
DB: [virulencefinder_db](https://bitbucket.org/genomicepidemiology/virulencefinder_db) ·
PyPI: [Virulencefinder](https://pypi.org/project/Virulencefinder/)

## Citation

Joensen, K. G. *et al.* Real-time whole-genome sequencing for routine typing,
surveillance, and outbreak detection of verotoxigenic *Escherichia coli*.
*J. Clin. Microbiol.* **52**, 4214–4220 (2014).
https://doi.org/10.1128/JCM.02452-14

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md) and `cge-finders`.

## Analytical thinking

VirulenceFinder matches curated virulence markers for **supported species
databases**. Coverage is not pan-bacterial; check which species DB is selected.
Gene presence ≠ expression, toxin production, or clinical virulence.

For open metagenomes, treat hits cautiously (contamination / partial contigs).
Pair with taxonomy (`gtdbtk` / isolate ID) before strong pathogenicity claims.
AMR remains `resfinder` / `rgi`; plasmids `plasmidfinder` / `genomad`.

## How to run

```bash
# install per upstream / pip; clone virulencefinder_db
python -m virulencefinder -ifa assembly.fasta -o vf_out \
  -db_path /path/to/virulencefinder_db
# species DB selection follows installed CLI / speciesinfo options
```

Pin tool + DB versions; report which species database was used.

## Decision tree

```text
Virulence markers?
├─ Supported CGE species DB → virulencefinder
├─ AMR genes → resfinder / rgi
├─ Plasmids → plasmidfinder / genomad
├─ Named MGEs → mobileelementfinder
└─ Unsure / environmental community → do not over-claim from VF hits alone
```

## Related skills

`cge-finders` · `resfinder` · `plasmidfinder` · `mobileelementfinder` ·
`staramr` · `rgi` · `genomad` · `microbial-mining` · `tool-selection`
