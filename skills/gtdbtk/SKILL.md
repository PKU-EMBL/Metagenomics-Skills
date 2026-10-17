---
name: gtdbtk
description: >
  Assign bacterial/archaeal taxonomy to MAGs with GTDB. Use for installation, parameter
  choice, execution, output interpretation, or troubleshooting.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "taxonomy, GTDB, MAG"
  metagenomics.upstream: "https://github.com/Ecogenomics/GTDBTk"
---

# GTDB-Tk

Upstream: [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk)

## Citation

Chaumeil, P.-A., Mussig, A. J., Hugenholtz, P. & Parks, D. H. GTDB-Tk v2: memory friendly classification with the Genome Taxonomy Database. *Bioinformatics* **38**, 5315–5316 (2022). https://doi.org/10.1093/bioinformatics/btac672

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

GTDB-Tk places genomes into the Genome Taxonomy Database hierarchy (bacterial/
archaeal). Taxonomy is a **separate claim layer** from binning labels and from
read profilers (MetaPhlAn/Kraken/sylph).

- Pin `GTDBTK_DATA_PATH` to a specific GTDB release and cite both GTDB-Tk and
  GTDB (`gtdb` skill).
- Low-quality / chimeric MAGs get misleading placements — filter with CheckM2 +
  GUNC first.
- “Novel” high-rank lineages require phylogenetic evidence beyond a single
  classify_wf row (trees, redundancy checks, literature).


## How to run

```bash
export GTDBTK_DATA_PATH=/path/to/gtdb
gtdbtk classify_wf \
  --genome_dir drep95/dereplicated_genomes \
  --out_dir temp/gtdb_classify \
  --extension fa --cpus 16
```

Optional: `gtdbtk infer` for trees from MSA outputs.

## Related skills

`phylogenomics` · `gtdb` · `phylophlan` · `iqtree` · `drep` · `checkm2` ·
`visualization`

