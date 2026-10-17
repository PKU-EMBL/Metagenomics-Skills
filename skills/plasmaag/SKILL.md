---
name: plasmaag
description: >
  PlasMAAG — recover plasmids and cellular genomes from metagenomes using
  assembly–alignment graphs and contrastive learning across samples. Use when: (1)
  Plasmid MAG reconstruction beyond circular-path assemblers, (2) Improving plasmid
  contig classification vs geNomad alone, (3) Host–plasmid association across
  multi-sample datasets. Pair with genomad for MGE screening and checkv for viral (not
  plasmid) QC.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "plasmid, MAG, PlasMAAG, MGE, binning"
  metagenomics.upstream: "https://github.com/RasmussenLab/PlasMAAG"
  metagenomics.stage: "mining"
  metagenomics.maturity: "reviewed"
  metagenomics.upstream-version: "snapshot a6b39ac"
  metagenomics.last-reviewed: "2026-10-18"
  metagenomics.command-status: "CLI and output contract reviewed against upstream; not executed here"
---

# PlasMAAG

Upstream: [RasmussenLab/PlasMAAG](https://github.com/RasmussenLab/PlasMAAG)

## Citation

Piera Líndez, P. *et al.* Accurate plasmid reconstruction from metagenomics data
using assembly–alignment graphs and contrastive learning. *Nat. Biotechnol.*
(2026). https://doi.org/10.1038/s41587-026-03005-7

See also [docs/references.md](https://github.com/PKU-EMBL/Metagenomics-Skills/blob/main/docs/references.md).

## Analytical thinking

Plasmids are under-recovered by chromosome-oriented binning and by single-sample
circular-path assemblers (fragmentation, entanglement, low coverage). PlasMAAG
builds an **assembly–alignment graph** across samples and bins plasmids +
organisms together with contrastive learning.

```text
multi-sample assemblies / graphs + alignments
  → plasmaag (plasmids + cellular bins)
  → genomad (orthogonal MGE labels)
  → resistome on plasmid bins (rgi) as needed
```

geNomad classifies contigs; PlasMAAG aims to **reconstruct plasmid genomes**.
Use both when plasmid biology is a primary claim.

## Inputs and run

Use Linux and at least two paired libraries when cross-sample graph/coverage evidence is the objective. The whitespace-delimited manifest header must be exactly `read1 read2`; use absolute, non-empty, synchronized FASTQs.

```bash
set -euo pipefail
[[ -s reads.tsv ]] || exit 2
read -r h1 h2 extra < reads.tsv
[[ "$h1" == read1 && "$h2" == read2 && -z "${extra:-}" ]] || exit 3
PlasMAAG --help >/dev/null
PlasMAAG --reads reads.tsv --output result/plasmaag --threads 32 --dryrun
PlasMAAG --reads reads.tsv --output result/plasmaag --threads 32 \
  >plasmaag.stdout.log 2>plasmaag.stderr.log
```

For existing metaSPAdes outputs, provide `--reads_and_assembly_dir` with exact headers `read1 read2 assembly_dir` and require `contigs.fasta`, `assembly_graph_after_simplification.gfa`, and `contigs.paths` per row. For MEGAHIT, use `--reads_and_contigs` with `read1 read2 contigs`.

## Validation, recovery, and provenance

Require completed workflow/logs and `results/candidate_plasmids.tsv`, `candidate_genomes.tsv`, `candidate_virus.tsv`, `scores.tsv` (or release-equivalent score tables), with corresponding non-empty FASTA directories when rows exist. Reconcile every contig and sample prefix, inspect cluster scores/conflicts, circularity/coverage/graph support, geNomad/MOB/replicon evidence and host-link uncertainty; run CheckV only on viral candidates.

Use Snakemake's supported resume only with unchanged manifest/config/software; otherwise preserve the run and use a new output. Record PlasMAAG commit/environment, config, geNomad DB, assembler/index versions, ordered manifest and checksums, command, logs, cluster tables and FASTA checksums. A reconstructed candidate is not proof of an autonomous complete plasmid or host association.

## Related skills

`genomad` · `basalt` · `vamb` · `rgi` · `microbial-mining` · `tool-selection`
