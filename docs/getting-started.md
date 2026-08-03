# Getting started

Step-by-step setup for Metagenomics Skills across agent platforms.

## Prerequisites

- An Agent Skills–compatible client (Claude Code, Codex, Cursor, Kimi Code, Grok Build, …)
- Linux recommended for running the bioinformatics tools themselves
- Python 3.10+ only if you use helper scripts locally

## Step 1: Install skills

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Symlink installer (Cursor / Kimi / Grok / shared Agents)

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills
./scripts/install-platforms.sh --user all
```

See [multi-platform.md](multi-platform.md) for per-platform paths.

## Step 2: Prepare analysis environments

Skills document **how** to run tools; they do not replace Conda environments.

```bash
# example checks
micromamba -V || conda -V
mkdir -p meta/{seq,temp,result,logs}
```

Follow the `setup` skill for database and BASALT weight installation.

## Step 3: Add metadata and reads

```text
meta/
├── seq/SampleA_1.fq.gz
├── seq/SampleA_2.fq.gz
└── result/metadata.txt
```

## Step 4: Ask for a routed plan

Example prompts:

- "Choose read-based vs MAG recovery for these samples"
- "Write a BASALT pilot command for one assembly + PE reads"
- "Design a co-assembly vs sample-specific experiment"

Expected skill routing: `tool-selection` / `study-design` → stage skills.

## Next

- [Skills catalog](skills.md)
- [Standard pipeline](standard-pipeline.md)
- [Compute setup](compute-setup.md)
