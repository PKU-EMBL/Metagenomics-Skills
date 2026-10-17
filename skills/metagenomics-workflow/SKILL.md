---
name: metagenomics-workflow
description: >
  End-to-end shotgun metagenomics: quality control, assembly, mapping, binning,
  taxonomic annotation, functional annotation, microbial mining (BGCs, AMR, MGEs,
  element cycling, DOM, defense), and research analysis (stats/figures). Use when
  starting a project or ordering stages. For tool choice use tool-selection. For mining
  use microbial-mining; for paper stats use research-analysis. For public DBs use
  public-databases.
license: MIT
metadata:
  metagenomics.category: "orchestration"
  metagenomics.tags: "guidance, pipeline, workflow, QC, assembly, mapping, binning, taxonomy, function, mining, research-analysis"
---

# Metagenomics Workflow

Organize by **scientific stage**. Mapping sits between assembly and binning.
Microbial mining is an optional discovery track on contigs/MAGs.

## Agent contract

1. State the mode: **advise**, **plan**, **prepare**, **execute**, or **review**.
2. Inspect sample metadata, read layout, existing outputs, compute, and databases
   before selecting commands. Mark unknowns; never infer groups from filenames.
3. Produce a stage table with inputs, outputs, resources, validation gates, and
   resume behavior. Stop at preflight if required information is missing.
4. Pilot one representative sample/partition before expensive scale-out.
5. Report separately what was prepared, executed, verified, failed, or not run.

For a multi-stage execution request, read
[the bundled execution gates](references/standard-pipeline.md) before writing or
running commands.

## Path

```text
study-design + setup (+ public-databases)
        │
        v
1 QC      fastp → kneaddata
        │
        ├─► 5 taxonomy / 6 function (reads) ─► research-analysis
        │
        v
2 Assembly   megahit | metaspades | metaflye | metamdbg
             (± binchicken for targeted coassembly)
        │
        v
3 Mapping    strobealign | bowtie2 | bwa-mem2 | minimap2 → samtools
        │
        ├─► 6 function (genes)
        │
        v
4 Binning    single binners → basalt ★ | metawrap | dastool
             → (± anvio refine | deepurify clean)
             → drep → coverm → checkm2 / gunc / mag-qc
        │
        ├─► 5 taxonomy (genomes): gtdbtk
        ├─► 6 function (genomes): bakta / prokka / eggnog-mapper / rgi
        └─► 7 microbial mining: antismash / genomad→checkv→vcontact / dram / …
        │
        v
   research-analysis (multiqc · microeco · maaslin2 · …) → Methods archive
```

## Choose the branch before tools

| Input / objective | Branch |
|-------------------|--------|
| Illumina/MGI composition or pathways only | short-read QC → read taxonomy/function; no assembly by default |
| Short-read MAG catalogue | short-read QC → assembly → short-read mapping → ensemble binning |
| ONT/CLR | long-read QC (outside `fastp`) → `metaflye` → `minimap2` → long-read-aware binning/polish |
| PacBio HiFi | HiFi QC → `metamdbg`/`metaflye` → `minimap2` → MAG route |
| Hybrid reads | keep technologies separate through QC; declare assembler/polishing evidence |
| Existing contigs/MAGs | audit provenance and QC first; do not silently rerun upstream stages |

## Common paths

| Goal | Route |
|------|-------|
| Composition only | QC → `metaphlan` / `singlem` / `kraken2` → `research-analysis` |
| Genome-resolved catalogue | QC → assembly → mapping → `basalt` ★ → mag-qc → gtdbtk |
| Interactive MAG polish | After auto-bins → `anvio` → re-QC |
| Environmental unknowns | QC → `singlem` (± `binchicken` coassembly) |
| Viral ecology | contigs → `genomad`/`virsorter2` → `checkv` → `vcontact` |

## Quality gates

- [ ] Design, statistical unit, controls, exclusions, and DB plan are locked
- [ ] Raw inputs are immutable; checksums and a one-row-per-sample manifest exist
- [ ] QC preserves PE order and explains read/base loss
- [ ] Assembly IDs are unique; QUAST-style statistics were inspected
- [ ] BAMs match the assembly checksum, are coordinate-sorted/indexed, and have
      reviewed mapping/depth summaries (multi-coverage for related samples)
- [ ] Ensemble binning route is declared (`basalt` recommended); every refine or
      clean step (`anvio` / `deepurify`) is followed by re-QC
- [ ] Accepted and rejected bins remain traceable through `mag-qc`
- [ ] Taxonomy/function layers and abundance semantics are not merged unlabeled
- [ ] Mining routes through `microbial-mining`; DBs/thresholds are pinned and
      computational hits remain hypotheses
- [ ] Trees route through `phylogenomics` (ANI is not a phylogeny)
- [ ] Statistics route through `research-analysis`; sample IDs, transforms,
      covariates, effect sizes, uncertainty, and FDR are recorded
- [ ] Software versions, database releases, commands, logs, and validation
      evidence are archived

## Related skills

`tool-selection` · `research-analysis` · `microbial-mining` · `homology-search` ·
`phylogenomics` · `metagenomics-llm` · `public-databases` · `study-design` ·
`mag-qc` · stage skills under `skills/`
