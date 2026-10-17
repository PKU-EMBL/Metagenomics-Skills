---
name: spacedust
description: >
  Spacedust — de novo discovery of conserved gene clusters in microbial genomes using
  Foldseek structure comparison plus clustering/order-conservation statistics. Use when:
  (1) Finding conserved neighborhoods / modules in MAG collections, (2) Annotating dark
  genes via genomic context, (3) Recovering defense or other systems as clusters. Route
  via microbial-mining / metagenomics-llm; complement defensefinder / antismash for
  known systems.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "Spacedust, gene-cluster, Foldseek, annotation, structure"
  metagenomics.upstream: "https://github.com/soedinglab/Spacedust"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot f758eb1"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI reviewed against upstream; not executed here"
---

# Spacedust

Upstream: [soedinglab/Spacedust](https://github.com/soedinglab/Spacedust)

## Citation

Zhang, R., Mirdita, M. & Söding, J. De novo discovery of conserved gene clusters
in microbial genomes with Spacedust. *Nat. Methods* (2025).
https://doi.org/10.1038/s41592-025-02816-x

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

In prokaryotes/viruses, **gene neighborhood conservation** signals functional
association. Spacedust finds conserved clusters de novo with sensitive
**Foldseek** structure comparison and order-conservation statistics — useful
when sequence annotation covers only a fraction of genes.

Paper-scale demonstration: all-vs-all on >1k bacterial genomes recovered large
fractions of genes in conserved clusters and most PADLOC-annotated antiviral
defense clusters — still validate priority systems with specialized tools
(`defensefinder`, `padloc`, `antismash`, experiments).

| vs | Notes |
|----|-------|
| `antismash` | Known BGC rules vs de novo neighborhoods |
| `defensefinder` | Known defense HMMs vs de novo clusters |
| `eggnog-mapper` | Per-gene orthology vs multi-gene context |

## Inputs and run

Provide one Prodigal-header protein FASTA per prokaryotic genome, or paired nucleotide FASTA/GFF3 files with stable coordinates. This sequence-search route avoids inventing structures:

```bash
set -euo pipefail
command -v spacedust >/dev/null
mapfile -t proteins < <(find proteins -maxdepth 1 -name '*.faa' -size +0c | sort)
(( ${#proteins[@]} >= 2 )) || exit 2
printf '%s\n' "${proteins[@]}" > proteins.list
mkdir -p db tmp result
spacedust createsetdb "${proteins[@]}" db/setDB tmp/create
spacedust clustersearch db/setDB db/setDB result/clusters.tsv tmp/search \
  --num-iterations 1 \
  >result/spacedust.stdout.log 2>result/spacedust.stderr.log
test -f result/clusters.tsv
```

For structure mode, first map `setDB` with `aa2foldseek` against a pinned Foldseek structure DB, then use `clustersearch ... --search-mode 1`; mode 2 uses ProstT5-derived 3Di. Keep these evidence modes separate.

## Decision tree

```text
Dark genes / modules in MAG sets?
├─ Conserved neighborhoods de novo → spacedust
├─ Known BGCs → antismash
├─ Known defense → defensefinder
└─ Per-gene orthology → eggnog-mapper
```

## Validation, recovery, and provenance

Require parseable cluster summary lines beginning `#` and member-hit lines beginning `>`. Check genome/protein ID and coordinate recovery, minimum cluster size, self/reciprocal duplicates, finite cluster/multihit P-values and neighborhood order; compare selected systems with known annotations and specialized tools. Multiple tests and homologous mobile regions can inflate discoveries.

Database/temp files are coupled to input and mode; use clean paths after changes. Record Spacedust/MMseqs2/Foldseek/ProstT5 versions, commands, ordered FASTA/GFF checksums, gene caller, structure DB/checksum, search mode/iterations/thresholds, logs and TSV checksum. Conserved neighborhoods imply association, not a proven operon or phenotype.

## Related skills

`foldseek` · `folddisco` · `mmseqs2` · `metagenomics-llm` · `defensefinder` ·
`antismash` · `eggnog-mapper` · `deepblast` · `microbial-mining` · `tool-selection`
