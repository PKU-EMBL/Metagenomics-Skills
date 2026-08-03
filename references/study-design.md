# Module A — Study design for genome-resolved metagenomics

## Design principle

Assemblies may be analysed jointly only when their coverage evidence remains
biologically interpretable as a coherent comparison. Additional assemblies can
recover complementary genome fragments; unrelated samples introduce ambiguous
mappings and invalid cross-sample selection.

Informative multi-sample designs occupy an intermediate regime: sufficient shared
genomic content for complementary observation, together with sufficient abundance
contrast to discriminate contig profiles. Near-replicate samples add limited
differential signal; biologically distant samples share too little content and
can compromise mapping and bin selection.

## When multi-assembly designs help

Especially informative when samples share community continuity:

- reactor or experimental system replicates;
- longitudinal host sampling;
- nearby sites in one connected environment;
- matched aliquots with different DNA-extraction protocols;
- before/after intervention;
- related growth or cultivation stages;
- environmental gradients with substantial continuity.

Across related samples, concordant coverage changes act as an abundance
fingerprint that complements tetranucleotide composition and sequence overlap.
Treat this as **supporting evidence for candidate decisions**, not independent
proof of genome membership.

## Decision table

| Question | If yes | If no |
|---|---|---|
| One coherent biological stratum? | May share one BASALT run | Separate runs by stratum |
| Every coverage file traceable to reads + assembly? | Record mapping | Repair provenance first |
| Pooled assembly biologically justified? | Include with individuals in a pilot | Prefer sample-specific only |
| Would pooling erase time/treatment/host/habitat contrast? | Keep strata separate | Pooling may be evaluated |

## Pattern: individual + matched pool

```text
replicate reads ──> sample-specific assemblies ──┐
       │                                        ├─> one BASALT run
       └───────> biologically matched pool ─────┘
```

The pool must be built from the stated group only. Report assembler, version,
parameters, and exact reads for every assembly. Compare the pilot with
**prespecified** MAG, redundancy, taxonomy, and read-support criteria.

## Pattern: longitudinal or staged sampling

```text
stage 1 → individual + stage-1 pool → BASALT run 1
stage 2 → individual + stage-2 pool → BASALT run 2
stage 3 → individual + stage-3 pool → BASALT run 3
```

Downstream cross-stage taxonomy, abundance, or dereplication needs a declared
similarity threshold. Do not infer temporal persistence from shared bin names
or rough marker similarity.

## Pattern: habitats or treatments

- Habitat-specific populations → separate runs, compare final MAGs downstream.
- Shared catalogue → retain habitat labels, assess mapping specificity, declare
  dereplication rule.
- Do not pool solely to increase depth if the mixture is biologically meaningless.

## When not to pool

Avoid pooled assembly or pooled coverage by default when:

- samples define the primary contrast (treatment, host, site, time);
- a high-abundance sample would dominate a low-abundance group;
- strain variation is central;
- extraction/library/sequencing protocols are incompatible;
- contamination or sample swaps are unresolved;
- read-to-assembly provenance cannot be reconstructed.

## Minimum design manifest

| Column | Example | Purpose |
|---|---|---|
| `sample_id` | `stage1_sample1` | Stable ID |
| `stratum` | `stage1` | Biological group |
| `assembly` | `stage1_sample1.fa` | Input to recovery |
| `assembly_type` | `individual` / `pool` | Strategy label |
| `assembly_reads` | accessions or checksums | Assembly provenance |
| `coverage_reads` | R1/R2, ONT, CLR, HiFi | Coverage evidence |
| `assembler` | name, version, params | Reproducibility |
| `run_directory` | absolute path | Checkpoint isolation |

## Pilot evaluation criteria

Compare designs with the same acceptance rules and QC database:

- retained genomes under explicit completeness/contamination thresholds;
- redundancy at a declared ANI criterion;
- taxonomic consistency and strain resolution needs;
- size, contiguity, read support;
- genomes unique to pooled vs individual assemblies;
- wall time, peak memory, temporary storage.

Choose from those results and the biological question—not from raw bin count.
