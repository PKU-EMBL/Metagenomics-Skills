---
name: study-design
description: >
  Study design for shotgun metagenomics across QC, assembly, binning, and
  annotation. Use this skill when: (1) Deciding co-assembly vs sample-specific
  assembly, (2) Defining biological strata (time, treatment, habitat, host),
  (3) Building a sample/assembly/coverage manifest, (4) Planning multi-assembly
  binning (e.g. BASALT), (5) Avoiding invalid pooling of unrelated samples.
  For tool routing, use tool-selection.
  For stage order, use metagenomics-workflow.
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
# Related replicates (feeds stage 3 binning)
sample-specific assemblies ─┐
matched co-assembly ────────┴─> one ensemble binning run (basalt★ / metawrap)

# Longitudinal / treatment
stage1 → run1
stage2 → run2
then compare bins/genomes with declared ANI threshold
```

Subgroup when samples > ~30 or data > ~300 Gb.

## Multi-coverage vs single-coverage binning

Mattock & Watson (*Nat. Methods* 2023) compared single- vs multi-coverage
binning on the **same** per-sample assemblies: multi-coverage recovered more
filtered bins and exposed contaminant/chimeric structure that single-coverage
misses (co-abundant contigs within one sample look “genome-like” without
cross-sample contrast).

Practical rule: when related samples exist, map **all** relevant samples to each
assembly for binning coverage — even if you keep sample-specific assemblies.
Single-coverage is a resource compromise, not a scientific default.

## Low-abundance / novelty coassembly

Blind pooling is costly and can worsen assemblies. For large cohorts aimed at
rare/novel genomes, consider **`binchicken`** (targeted coassembly via shared
SingleM markers, optional novelty prioritization). Still enforce stratum rules
above — targeting is not a license to mix unrelated biology into one contrast.

## Pilot evaluation

Compare designs on retained bins under fixed completeness/contamination,
redundancy (ANI), taxonomy, contiguity, and compute cost — not raw bin count.

## Related skills

- `tool-selection` — stage routing; ensemble binning choice
- `metagenomics-workflow` — QC → assembly → binning → taxonomy → function → mining → research-analysis
- `basalt` · `metawrap` · `dastool` — binning stage
- `binchicken` — targeted coassembly planning for low-abundance recovery
- `lorbin` · `comebin` · `semibin2` · `vamb` — single binners
