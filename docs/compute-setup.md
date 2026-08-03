# Compute setup

Practical resource guidance for shotgun metagenomics.

## Hardware (order of magnitude)

| Workload | CPU | RAM | Scratch |
|----------|-----|-----|---------|
| QC + host removal | 8–32 cores | 32–64 GB | 3–5× raw |
| HUMAnN / Kraken | 16–32 | 64–128 GB | moderate |
| MEGAHIT co-assembly | 32+ | 128–512 GB | large |
| MetaWRAP mixed binning | 32+ | 256 GB–1 TB | large |
| BASALT | 32+ | 128–256 GB+ | large |

GPU is optional; BASALT refinement may use GPU when configured.

## Software layout

- Stage-specific Conda/Micromamba environments
- Persistent database directory (host indexes, Kraken, eggNOG, GTDB, CheckM2)
- One working directory per BASALT run

## Scheduler tips

- Quote BASALT `-s` values when `/` is special to the scheduler
- Request hard memory limits independently of BASALT `-m` (advisory only)
- Keep run directories on fast scratch; archive finals + provenance to long-term storage

See also `skills/_shared/compute-notes.md`.
