# Getting started

Step-by-step setup for Metagenomics Skills across agent platforms.

## Prerequisites

- An Agent Skills–compatible client (Claude Code, Codex, Cursor, Kimi Code,
  ZCode, Qwen Code, Grok Build, …)
- Linux recommended for running the bioinformatics tools themselves
- Python 3.10+ for the portable installer and validation helpers

## Step 1: Install skills

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Codex plugin

```bash
codex plugin marketplace add PKU-EMBL/Metagenomics-Skills
codex plugin add metagenomics@metagenomics-skills
```

### Portable installer (Codex / Cursor / Kimi / ZCode / Qwen / others)

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills

# Recommended for most sessions: 48 high-use skills with routing hubs
./scripts/install-platforms.sh --user --profile core kimi zcode qwen

# Shared location read by Codex, Kimi Code, and ZCode; plus Qwen's native path
./scripts/install-platforms.sh --user --profile core agents qwen

# Every platform and all 201 skills (largest startup catalog)
./scripts/install-platforms.sh --user --profile full all
```

Profiles can be combined (`--profile genome-resolved --profile mining`). Use
`--mode copy` where symlinks are unavailable, `--target PATH` for any other
client, and `--dry-run` before a shared installation. When replacing an existing
large profile with a smaller one, preview and then add `--prune`; only paths
tracked by this installer are eligible for removal. Run
`./scripts/install-platforms.sh --list-platforms` and `--list-profiles` for the
current matrix.

Kimi Code can also use the repository without installation:

```bash
kimi --skills-dir "$PWD/skills"
```

See [multi-platform.md](multi-platform.md) for native paths, plugin/extension
manifests, project scope, Windows copy mode, and ZCode/Qwen options.

## Step 2: Prepare analysis environments

Skills document **how** to run tools; they do not replace Conda environments.

```bash
micromamba -V || conda -V
mkdir -p meta/{seq,temp,result,logs}
```

Follow `setup` and `public-databases` for software and reference installs.
For portable DAGs see `nextflow` / `snakemake`.

## Step 3: Add metadata and reads

```text
meta/
├── seq/SampleA_1.fq.gz
├── seq/SampleA_2.fq.gz
└── result/metadata.txt
```

## Step 4: Ask for a stage-routed plan

Start by naming the operating mode: **advise**, **plan**, **prepare**,
**execute**, or **review**. See the [coding-agent playbook](agent-playbook.md)
for the inspection, preflight, validation, and provenance contract.

Example prompts:

- "Plan QC → assembly → binning → taxonomy → function for these samples; do not execute yet"
- "Review this existing run, inspect its logs and quality gates, and do not rerun it"
- "Read-based taxonomic annotation only — which tools after KneadData?"
- "Recommended ensemble binning after MEGAHIT for related bioreactors"
- "Functional annotation via gene catalogue vs HUMAnN"
- "Environmental samples with many unknowns — SingleM vs MetaPhlAn?"
- "After binning: Deepurify or Anvi'o before GTDB-Tk?"
- "Viral contigs: geNomad → CheckV → vConTACT workflow"
- "Element cycling (N/S/Fe) on MAGs — METABOLIC vs FeGenie vs DRAM?"
- "Downstream stats and figures after MetaPhlAn — microeco vs MaAsLin2?"
- "Route protein language models for remote homology"

### Common analysis paths

| Goal | Skills path |
|------|-------------|
| Composition only | QC → `metaphlan` / `singlem` / `kraken2` → `research-analysis` |
| Genome-resolved catalogue | QC → assembly → mapping → `basalt` ★ → `mag-qc` → `gtdbtk` |
| Interactive MAG polish | bins → `anvio` → re-QC |
| Viral / MGE ecology | `genomad` → `checkv` → `vcontact` (± `mobileog` / `mob-suite`) |
| Isolate CGE Finders | `cge-finders` → `staramr` / `abricate` / `plasmidfinder` → `pmlst` / `mlst` |
| Mining (BGC / AMR / cycling / DOM) | `microbial-mining` |
| Paper stats & figures | `research-analysis` → `microeco` / `maaslin2` / … |
| DNA / protein LMs | `genome-language-model` / `protein-language-model` |

Expected routing: `tool-selection` / `metagenomics-workflow` / `study-design`
→ only the required stage skills → `research-analysis` for statistical delivery.
The agent should distinguish observed inputs, assumptions, prepared commands,
executed commands, validation evidence, and remaining blockers.

## Next

- [Coding-agent playbook](agent-playbook.md)
- [Standard pipeline](standard-pipeline.md)
- [Skills catalog](skills.md)
- [Public databases](public-databases.md)
- [Troubleshooting](troubleshooting.md)
- [Compute setup](compute-setup.md)
