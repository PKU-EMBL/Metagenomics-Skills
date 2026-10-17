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
  metagenomics.stage: "taxonomy"
  metagenomics.maturity: "reviewed"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and release-coupling contract reviewed; not executed here"
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
set -euo pipefail
: "${GTDBTK_DATA_PATH:?set GTDBTK_DATA_PATH to one pinned GTDB release}"
[[ -d "$GTDBTK_DATA_PATH" && -d drep95/dereplicated_genomes ]] || exit 2
gtdbtk classify_wf \
  --genome_dir drep95/dereplicated_genomes \
  --out_dir temp/gtdb_classify \
  --extension fa --cpus 16
```

Optional: `gtdbtk infer` for trees from MSA outputs.

## Validation, recovery, and provenance

Require bacterial and/or archaeal summary tables, warning/failure logs, marker alignments, and expected classified-genome accounting. Reconcile each input as classified, unclassified, failed, or excluded; inspect `classification_method`, ANI/relative evolutionary divergence, closest references, warnings, and multi-hit/translation issues. A name copied from the summary without these columns loses critical evidence.

GTDB-Tk outputs and reference data are release-coupled. Use a fresh output after changing either; never merge taxonomy labels across GTDB releases without an explicit mapping. Record GTDB-Tk/dependency versions, GTDB release and `GTDBTK_DATA_PATH` checksum/manifest, full command, input FASTA checksums, summary/tree checksums, and failed genomes.

## Related skills

`phylogenomics` · `gtdb` · `phylophlan` · `iqtree` · `drep` · `checkm2` ·
`visualization`

