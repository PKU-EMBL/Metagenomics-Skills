# Compute setup

Practical resource guidance for shotgun metagenomics.

## Hardware (order of magnitude)

| Workload | CPU | RAM | Scratch |
|----------|-----|-----|---------|
| QC + host removal | 8–32 cores | 32–64 GB | 3–5× raw |
| Mapping (Bowtie2 / strobealign / BWA-MEM2) | 16–64 | 32–128 GB | BAM ≈ 1–2× reads |
| HUMAnN / Kraken | 16–32 | 64–128 GB | moderate + DB |
| MEGAHIT co-assembly | 32+ | 128–512 GB | large |
| metaSPAdes | 32+ | 256 GB–1 TB | large |
| MetaWRAP / multi-binner | 32+ | 256 GB–1 TB | large |
| BASALT | 32+ | 128–256 GB+ | large |
| antiSMASH batch (many MAGs) | 16–32 | 64–128 GB | moderate |
| DRAM annotate | 16–32 | 64–128 GB+ | DB + outputs |
| geNomad end-to-end | 16–32 | 64–128 GB | DB tens of GB |

GPU is optional; BASALT refinement may use GPU when configured.

## Software layout

- Stage-specific Conda/Micromamba environments
- Persistent database directory: host indexes, Kraken, eggNOG, GTDB, CheckM2,
  antiSMASH, geNomad, CheckV, DRAM, Bakta, CARD
- One working directory per BASALT run
- Shared read-only DB mounts for multi-user clusters

## Scheduler tips

- Quote BASALT `-s` values when `/` is special to the scheduler
- Request hard memory limits independently of BASALT `-m` (advisory only)
- Map with streaming `aligner | samtools sort` and set `TMPDIR` to fast scratch
- Keep run directories on fast scratch; archive finals + provenance long-term

See also `skills/_shared/compute-notes.md`.
