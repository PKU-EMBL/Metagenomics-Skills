---
name: gtdbtk
description: >
  Assign bacterial/archaeal taxonomy to MAGs with GTDB. Use this skill when working with gtdbtk: installing, choosing parameters, running commands, interpreting outputs, or troubleshooting. Upstream: https://github.com/Ecogenomics/GTDBTk. For routing across tools, use tool-selection. For end-to-end pipelines, use metagenomics-workflow.
license: MIT
category: analysis-tools
tags: ['taxonomy', 'GTDB', 'MAG']
upstream: https://github.com/Ecogenomics/GTDBTk
---

# GTDB-Tk

Upstream: [Ecogenomics/GTDBTk](https://github.com/Ecogenomics/GTDBTk)

## Analytical thinking

GTDB-Tk places genomes into the Genome Taxonomy Database hierarchy. Taxonomy is
a **separate claim layer** from binning labels. Pin `GTDBTK_DATA_PATH` to a
specific GTDB release and cite it.

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

`drep` · `checkm2` · `visualization`

