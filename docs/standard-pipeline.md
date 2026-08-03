# Standard pipeline

End-to-end shotgun metagenomics workflow.

No single route is best for every study. Choose by **deliverable**, then execute
phases in order. Use `tool-selection` when undecided.

## Overview

```text
Target study → Setup → Preprocessing → Community and/or genomes → QC → Figures
 (study-design) (setup) (preprocessing) (read-based / gene-catalogue /
                                        mag-classical / basalt)
```

## Phase 1: Study design

**Skill**: `study-design`

- Define strata and whether co-assembly is biologically valid
- Build the sample/assembly/coverage manifest
- Predeclare MAG or profiling acceptance criteria

## Phase 2: Setup

**Skill**: `setup`

- Create `seq/`, `temp/`, `result/`
- Install stage environments and databases
- Optional: BASALT weights + CheckM2 DB

## Phase 3: Preprocessing

**Skill**: `preprocessing`

```bash
fastp ...
kneaddata ... --reorder ...
```

Checklist:
- [ ] PE IDs paired after host removal
- [ ] Host genome identity recorded
- [ ] Checksums stored

## Phase 4A: Read-based (optional)

**Skill**: `read-based`

Use for species/pathway tables without genomes.

## Phase 4B: Gene catalogue (optional)

**Skill**: `gene-catalogue`

```text
MEGAHIT → Prodigal → cd-hit → salmon → eggNOG/CARD
```

## Phase 5: MAG recovery (optional)

| Goal | Skill |
|------|-------|
| Classical catalogue | `mag-classical` |
| Refined multi-assembly MAGs | `basalt` |

Then apply `mag-qc` filters.

## Phase 6: Visualization and reporting

**Skill**: `visualization`

Label every figure with method + database release. Archive provenance with results.

## Alternative: BASALT-first genome path

```text
study-design → setup → preprocessing → assembly → basalt → mag-qc → visualization
```

Prefer when related multi-assembly evidence is central to the claim.
