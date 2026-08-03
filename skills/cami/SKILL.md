---
name: cami
description: >
  CAMI / CAMI II metagenome benchmarking datasets and evaluation stack
  (CAMISIM, AMBER, OPAL, CAMI Benchmarking Portal). Use when: (1) Downloading
  CAMI challenge data / gold standards, (2) Choosing marine, plant-associated,
  strain-madness, mouse-gut, or human toy sets, (3) Evaluating binners with
  AMBER or profilers with OPAL, (4) Simulating communities with CAMISIM,
  (5) Citing CAMI results in Methods without over-generalizing to new biomes.
  Portal: https://cami-challenge.org/ and https://data.cami-challenge.org/.
  For real-world public reads use sra-ena; for biome MAG catalogues use mgnify.
license: MIT
category: utilities
tags: [CAMI, CAMI2, benchmark, AMBER, OPAL, CAMISIM, gold-standard]
upstream: https://cami-challenge.org/
---

# CAMI (Critical Assessment of Metagenome Interpretation)

Portal: https://cami-challenge.org/ ·
Data: https://data.cami-challenge.org/ ·
GitHub org: [CAMI-challenge](https://github.com/CAMI-challenge) ·
Benchmarking portal paper / server: see References

## Citation

Sczyrba, A. *et al.* Critical Assessment of Metagenome Interpretation—a benchmark
of metagenomics software. *Nat. Methods* **14**, 1063–1071 (2017).
https://doi.org/10.1038/nmeth.4458

Meyer, F. *et al.* Critical Assessment of Metagenome Interpretation: the second
round of challenges. *Nat. Methods* **19**, 429–440 (2022).
https://doi.org/10.1038/s41592-022-01431-4

Fritz, A. *et al.* CAMISIM: simulating metagenomes and microbial communities.
*Microbiome* **7**, 17 (2019). https://doi.org/10.1186/s40168-019-0633-6

Meyer, F. *et al.* AMBER: Assessment of Metagenome BinnERs. *GigaScience* **7**,
giy069 (2018). https://doi.org/10.1093/gigascience/giy069

Meyer, F. *et al.* Assessing taxonomic metagenome profilers with OPAL.
*Genome Biol.* **20**, 51 (2019). https://doi.org/10.1186/s13059-019-1646-y

Meyer, F. *et al.* CAMI Benchmarking Portal: online evaluation and ranking of
metagenomic software. *Nucleic Acids Res.* **53**, W102–W109 (2025).
https://doi.org/10.1093/nar/gkaf369

See also [docs/references.md](../../docs/references.md) and
[docs/public-databases.md](../../docs/public-databases.md).

## Analytical thinking

CAMI is a **community benchmarking initiative**, not a natural biome catalogue.
Datasets are computationally constructed (often via CAMISIM) with **gold
standards** for assembly, genome binning, taxonomic binning, and profiling.

Use CAMI when you need:

| Goal | Resource |
|------|----------|
| Compare assemblers / binners / profilers under controlled truth | CAMI / CAMI II challenge data |
| Generate custom gold-standard simulations | `CAMISIM` |
| Score genome bins vs gold | `AMBER` |
| Score taxonomic profiles vs gold | `OPAL` |
| Submit / browse rankings | CAMI Benchmarking Portal |

Do **not** treat CAMI rankings as a universal ordering for your soil/gut/reactor
study — CAMI II still found related strains hard for assembly/binning, and
viruses/Archaea underperformed for many profilers/binners. Cite the **dataset
name** (e.g. plant-associated, strain-madness, marine, mouse gut) you actually ran.

Abundance caveat (Sun *et al.*, *Nat. Methods* 2021): profilers report
**sequence abundance** vs **taxonomic abundance** — do not mix them when
scoring with OPAL or comparing MetaPhlAn vs Kraken.

## Dataset layers

```text
CAMISIM / community design
        ↓
short- and/or long-read metagenomes (+ multi-sample designs)
        ↓
gold standards (assembly / genome binning / tax. binning / profiling)
        ↓
your tool outputs (bioboxes / CAMI formats)
        ↓
AMBER (bins) · OPAL (profiles) · portal rankings
```

CAMI II scale (paper): ~1,700 genomes + ~600 plasmids/viruses; short + long
reads; thousands of submitted results across dozens of program versions.

## How to obtain data

Prefer the live portal paths over inventing FTP URLs:

```text
https://cami-challenge.org/
https://data.cami-challenge.org/participate
```

CAMI II challenge / exemplary datasets were also deposited with PUBLISSO DOIs
(marine, strain-madness, plant-associated, mouse gut, human) — resolve from the
CAMI II paper Data availability / portal, then pin the DOI + download date.

```bash
# Pattern only — resolve exact URLs from the portal for the dataset you need
mkdir -p db/cami/<dataset_id>
# download reads, assemblies (if provided), gold standards, taxonomy snapshot
# archive SHA256 / download date in provenance/
```

## Evaluation tools

| Tool | Upstream | Use |
|------|----------|-----|
| CAMISIM | https://github.com/CAMI-challenge/CAMISIM | Simulate communities + gold standards |
| AMBER | https://github.com/CAMI-challenge/AMBER | Assess genome binners |
| OPAL | https://github.com/CAMI-challenge/OPAL | Assess taxonomic profilers |
| Portal | https://cami-challenge.org/ | Online evaluation / ranking |

```bash
# Install from upstream docs (versions move) — examples:
# conda / pip per CAMI-challenge READMEs
# amber ...   # binning gold vs predictions
# opal ...    # profiling gold vs predictions
```

Use CAMI **bioboxes / profiling formats** when possible so AMBER/OPAL/portal
can ingest outputs without custom parsers.

## Decision tree

```text
Need public metagenome *data*?
├─ Controlled benchmark with gold standards → cami (this skill)
├─ Simulate custom communities → CAMISIM (this skill)
├─ Real environmental/clinical reads → sra-ena (± mgnify analysed studies)
├─ Biome MAG / protein catalogues → mgnify
└─ Rank-normalized prokaryotic taxonomy release → gtdb
```

## Methods caveats

1. Report CAMI challenge round + dataset ID + gold-standard version
2. Separate short-read vs long-read vs hybrid results
3. Do not equate CAMI “best tool” with production defaults for all biomes
4. Keep sequence- vs taxonomic-abundance definitions explicit in profiler benchmarks
5. Reference DBs frozen for a challenge (e.g. RefSeq snapshot dates) ≠ today’s GTDB/MGnify

## Related skills

`public-databases` · `sra-ena` · `mgnify` · `gtdb` · `quast` · `metabat2` ·
`basalt` · `metaphlan` · `kraken2` · `tool-selection` · `study-design`
