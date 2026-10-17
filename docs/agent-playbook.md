# Coding-agent playbook

A platform-neutral execution contract for Claude Code, Codex, Cursor, Kimi
Code, ZCode, Qwen Code, and other Agent Skills clients.

## Choose the operating mode

Infer the least destructive mode that satisfies the request and state it:

| Mode | Agent action |
|------|--------------|
| Advise | Explain choices; do not create files or run analyses |
| Plan | Inspect available metadata/files and produce a staged, resource-aware plan |
| Prepare | Create manifests, configs, workflow files, and dry-run commands |
| Execute | Run approved stages, inspect outputs, and iterate through quality gates |
| Review | Audit an existing run without silently rerunning or rewriting it |

If the user asks for execution but key biological or compute inputs are absent,
stop at a concrete preflight report instead of guessing.

## Intake before tool selection

Collect or infer, then mark unknowns explicitly:

- scientific question, primary contrast, and statistical unit
- sample sheet, biological replicates, repeated measures, controls, and batches
- read technology, layout, compression, expected depth, and file locations
- host/background depletion requirements and data-governance constraints
- read-based, assembly-based, genome-resolved, mining, or combined deliverables
- available CPU, RAM, scratch, scheduler/container runtime, and wall-time limits
- database locations/releases, network policy, and storage budget
- existing outputs that must be reused rather than recomputed

Never infer biological groups from filenames when a sample sheet can be obtained.
Never upload human-associated reads, credentials, or unpublished data to an
external service without explicit authorization.

## Inspect, plan, then execute

1. **Discover without mutation.** List relevant files, inspect small headers,
   check read pairing and sample IDs, and identify existing environments/outputs.
2. **Lock the design.** Define inclusion/exclusion rules, assembly grouping,
   coverage mapping, contrasts, covariates, and expected deliverables.
3. **Route skills.** Load `metagenomics-workflow` and `tool-selection`, then only
   the specialist skills needed for the chosen route.
4. **Write an execution plan.** For every stage provide inputs, outputs, command
   or workflow rule, resources, validation gate, and resume behavior.
5. **Preflight.** Verify binaries, versions, database paths/releases, free space,
   permissions, and scheduler/container availability. Do not start a large run
   if any mandatory check fails.
6. **Pilot.** Dry-run the workflow or process one representative sample/partition
   before scaling out. Estimate output and scratch growth from the pilot.
7. **Execute with logs.** Use strict shell settings in generated scripts, quote
   paths, preserve paired reads, keep one log per sample/task, and avoid
   destructive globbing.
8. **Validate each boundary.** Check exit status plus biological/file-level
   invariants before downstream use; a zero exit code alone is insufficient.
9. **Report truthfully.** Distinguish commands prepared, commands executed,
   checks passed, checks failed, and checks not run.

## Minimum quality gates

| Boundary | Required checks before continuing |
|----------|-----------------------------------|
| Raw → cleaned reads | pairs retained and synchronized; report files exist; read/base loss explained |
| Clean reads → assembly | non-empty inputs; expected samples; no accidental lane/sample mixing |
| Assembly → mapping | unique contig IDs; assembly statistics reviewed; index matches FASTA checksum |
| Mapping → coverage/binning | coordinate-sorted/indexed BAM; mapping rate and depth sanity checks; sample-to-assembly provenance |
| Bins → MAG catalogue | CheckM2-style completeness/contamination plus chimerism checks; thresholds stated; refinement followed by re-QC |
| MAGs → taxonomy/function | stable genome IDs; exact GTDB/annotation DB releases; failed genomes retained in audit table |
| Profiles → statistics | sample IDs join one-to-one; abundance semantics and normalization declared; batch/confounding assessed |
| Mining → claims | hit thresholds and genomic context retained; predictions labeled as hypotheses, not validated phenotypes/products |

## Reproducibility bundle

Keep these alongside final results (TSV/YAML/JSON are preferable to prose-only
records):

```text
provenance/
├── samples.tsv              # immutable sample IDs, groups, batches, read paths
├── analysis-plan.yaml       # stages, parameters, resources, expected outputs
├── software-versions.tsv    # executable/container + exact version/digest
├── database-manifest.tsv    # DB name, release, path/URL, checksum/date
├── input-checksums.sha256
├── commands/                # scripts or workflow configs actually used
├── logs/
└── validation-summary.tsv   # gate, status, evidence, exception/reason
```

Record both software and database versions. If a command changes after a failed
run, preserve the failed command/log and document the reason for the change.

## Response contract

For plans and completed work, report in this order:

1. **Goal and mode**
2. **Observed inputs** (not assumptions)
3. **Assumptions / blockers / questions**
4. **Selected route and rejected alternatives**
5. **Commands or files changed**
6. **Validation evidence**
7. **Outputs and provenance paths**
8. **Remaining risks and next decision**

Do not report “completed,” “clean,” “high quality,” or “significant” without the
corresponding inspected evidence and threshold/test definition.

## Prompt template

```text
Use the metagenomics skills in [plan|prepare|execute|review] mode.
Goal: ...
Samples/metadata: ...
Reads: [Illumina PE|ONT|HiFi|hybrid], paths: ...
Primary contrast/statistical unit: ...
Compute: ...
Databases already available: ...
Required deliverables: ...
Constraints (privacy, network, deadline, tools): ...
Return a stage table with inputs, outputs, resources, validation gates, and
provenance files. Do not execute large downloads or compute without approval.
```
