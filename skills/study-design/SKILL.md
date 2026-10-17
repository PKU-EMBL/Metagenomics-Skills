---
name: study-design
description: >
  Design shotgun-metagenomics studies and manifests: biological replication, statistical
  units, controls, batches/confounders, longitudinal structure, co-assembly versus
  sample-specific assembly, and multi-sample coverage. Use before generating a pipeline,
  pooling reads, binning related samples, or defining downstream contrasts. For tool
  routing use tool-selection; for stage order use metagenomics-workflow.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "study-design, co-assembly, pooling, provenance"
  metagenomics.stage: "utilities"
---

# Study Design

## Design principle

Analyse assemblies jointly only when coverage remains biologically interpretable.
Unrelated samples create ambiguous mappings and invalid selection.

Informative multi-sample designs need:
- enough shared genomes for complementary observation
- enough abundance contrast to discriminate contig profiles

## Lock the inferential design first

Record these before tool selection:

| Item | Required decision |
|------|-------------------|
| Scientific unit | Independent subject/site/reactor, not reads, genes, contigs, or MAGs |
| Primary contrast | One predeclared comparison and direction; secondary contrasts labeled |
| Replication | Biological replicates per stratum; technical replicates identified separately |
| Repeated measures | Subject/site ID and time/order; plan paired or mixed-effects analysis |
| Controls | Extraction blanks, no-template controls, mock communities, host/background controls as applicable; route decisions through `contamination-control` |
| Load calibration | Decide whether relative profiles suffice; otherwise predeclare spike-in, qPCR, flow-cytometry, or mass measurements for `absolute-abundance` |
| Source tracking | Predeclare candidate sources, sinks, negative controls, and held-out validation; an omitted source becomes “unknown” |
| Confounders | Extraction kit/batch, run/lane, site, host, storage, depth, and measured covariates |
| Randomization | Balance groups across extraction and sequencing batches where still possible |
| Exclusions | Objective QC rules defined before inspecting group outcomes |

Do not inflate sample size by treating multiple MAGs/features from one sample as
independent biological replicates. If group is perfectly confounded with batch,
state that the biological effect is not separately identifiable; software cannot
repair the design.

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

## Manifest

Start from the bundled
[manifest template](references/manifest-template.md) and keep one row per
sequencing library while preserving the biological-unit identifier.

| Field | Purpose |
|-------|---------|
| `sample_id` / `library_id` | Stable biological and library IDs; never derive groups from filenames |
| `subject_id` / `site_id` | Independent unit and repeated-measure linkage |
| `group`, `timepoint`, covariates | Predeclared contrast and model variables |
| `control_type` | Biological sample, blank, mock, no-template, or other control |
| `extraction_batch`, `library_batch`, `run`, `lane` | Detect and model technical structure |
| `read1`, `read2`, `long_reads` | Absolute/portable input paths and read technology |
| `rna_read1`, `rna_read2` | RNA libraries kept distinct from DNA; collection, stabilization, extraction and rRNA-depletion batch |
| `spike_id`, `spike_amount`, `qpcr_load`, `flow_count` | Calibration values, units, dilution and assay provenance; never infer missing values |
| `host_reference` | Exact host/background reference and release |
| `assembly`, `assembly_type` | Contig FASTA; `individual`, `pool`, or `subgroup` |
| `assembly_reads`, `coverage_reads` | Exact many-to-many provenance |
| `run_directory` | Dedicated working directory; no cross-run reuse |

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

Treat roughly 30 samples or 300 Gb as prompts to evaluate subgrouping, not as
universal cutoffs: pilot assembly complexity, shared-community signal, memory,
and the scientific contrast determine the actual partition.

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
Use the same QC gates for every candidate design and keep rejected outputs in the
audit table.

## Required design deliverable

Return a locked manifest plus a short design note containing: statistical unit,
primary/secondary contrasts, controls, batches, exclusion criteria, assembly
partition, coverage mapping matrix, anticipated model, power/precision limits,
and unresolved risks. Distinguish decisions from assumptions.

## Related skills

- `tool-selection` — stage routing; ensemble binning choice
- `metagenomics-workflow` — QC → assembly → binning → taxonomy → function → mining → research-analysis
- `basalt` · `metawrap` · `dastool` — binning stage
- `binchicken` — targeted coassembly planning for low-abundance recovery
- `lorbin` · `comebin` · `semibin2` · `vamb` · `metacoag` — single binners
- `contamination-control` · `absolute-abundance` · `source-tracking` — controls, calibration, and source/sink design
- `long-read-qc` · `metatranscriptomics` · `virome-analysis` · `eukaryotic-metagenomics` — assay-specific design
