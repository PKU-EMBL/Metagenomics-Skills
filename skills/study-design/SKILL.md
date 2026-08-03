---
name: study-design
description: >
  Study design for shotgun metagenomics and genome-resolved analyses.
  Use this skill when: (1) Deciding co-assembly vs sample-specific assembly,
  (2) Defining biological strata (time, treatment, habitat, host),
  (3) Building a sample/assembly/coverage manifest,
  (4) Planning multi-assembly BASALT runs,
  (5) Avoiding invalid pooling of unrelated samples.

  For tool routing, use tool-selection.
  For full pipeline steps, use metagenomics-workflow.
license: MIT
category: orchestration
tags: [study-design, co-assembly, pooling, provenance]
---

# Study Design

## Design principle

Analyse assemblies jointly only when coverage remains biologically interpretable.
Unrelated samples create ambiguous mappings and invalid selection.

Informative multi-sample designs need:
- enough shared genomes for complementary observation
- enough abundance contrast to discriminate contig profiles

## Decision table

| Question | If yes | If no |
|----------|--------|-------|
| One coherent biological stratum? | May share one recovery run | Split by stratum |
| Coverage traceable to reads + assembly? | Record mapping | Repair provenance first |
| Pooled assembly justified? | Pilot with individuals + matched pool | Prefer sample-specific |
| Pooling erases primary contrast? | Keep strata separate | Pooling may be tested |

## When multi-assembly helps

Reactor replicates, longitudinal hosts, nearby sites, matched extraction methods,
before/after intervention, related growth stages, continuous environmental gradients.

## Manifest (required fields)

| Field | Purpose |
|-------|---------|
| `sample_id` | Stable ID matching filenames |
| `stratum` / `Group` | Biological partition |
| `host_reference` | Host genome for depletion |
| `assembly` | Contig FASTA |
| `assembly_type` | `individual` / `pool` / `subgroup` |
| `assembly_reads` / `coverage_reads` | Exact provenance |
| `run_directory` | Dedicated working directory |

## Patterns

```text
# Related replicates
sample-specific assemblies ─┐
matched co-assembly ────────┴─> one BASALT / MAG run

# Longitudinal / treatment
stage1 → run1
stage2 → run2
then compare MAGs with declared ANI threshold
```

Subgroup when samples > ~30 or data > ~300 Gb.

## Pilot evaluation

Compare designs on retained MAGs under fixed completeness/contamination,
redundancy (ANI), taxonomy, contiguity, and compute cost — not raw bin count.

## Related skills

- `tool-selection` — classical MAG vs BASALT
- `basalt` — multi-assembly execution
- `mag-classical` — MetaWRAP-style catalogues
