---
name: motus
description: >
  Marker-gene taxonomic profiling across environments (mOTUs3). Use for installation,
  parameter choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, marker, profile"
  metagenomics.upstream: "https://github.com/motu-tool/mOTUs"
  metagenomics.stage: "taxonomy"
---

# mOTUs

Upstream: [mOTUs](https://github.com/motu-tool/mOTUs)

## Citation

Ruscheweyh, H.-J. *et al.* Cultivation-independent genomes greatly expand taxonomic-profiling capabilities of mOTUs across various environments. *Microbiome* **10**, 212 (2022). https://doi.org/10.1186/s40168-022-01410-z

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

mOTUs profiles communities with a curated set of **universal single-copy
phylogenetic marker genes**, updated with cultivation-independent genomes so
environmental / non-human biomes are better covered than early gut-centric
releases.

Compared with MetaPhlAn:

| | mOTUs | MetaPhlAn 4 |
|--|-------|-------------|
| Marker philosophy | Mostly universal SCGs → mOTU clusters | Clade-/SGB-specific marker packs |
| Strength | Cross-environment comparability | Fine SGB resolution incl. unknowns |
| Merge rule | Do not average with Kraken/MetaPhlAn unlabeled |

Pin mOTUs DB version; host-deplete first.

## How to run

```bash
motus profile -f clean_1.fq.gz -r clean_2.fq.gz -t 16 -o temp/motus/${id}.motus
```

## Key parameters

| Item | Notes |
|------|-------|
| DB | `motus download-db` — pin version |
| `-t` | Threads |
| Downstream | Diversity / ecology tables — not MAG taxonomy (`gtdbtk`) |

## Related skills

`metaphlan` · `kraken2` · `sylph` · `metabuli` · `tool-selection` · `metagenomics-workflow`
