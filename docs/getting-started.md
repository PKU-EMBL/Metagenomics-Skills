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
micromamba -V || conda -V
mkdir -p meta/{seq,temp,result,logs}
```

Follow `setup` and `public-databases` for software and reference installs.

## Step 3: Add metadata and reads

```text
meta/
├── seq/SampleA_1.fq.gz
├── seq/SampleA_2.fq.gz
└── result/metadata.txt
```

## Step 4: Ask for a stage-routed plan

Example prompts:

- "Plan QC → assembly → binning → taxonomy → function for these samples"
- "Read-based taxonomic annotation only — which tools after KneadData?"
- "Recommended ensemble binning after MEGAHIT for related bioreactors"
- "Functional annotation via gene catalogue vs HUMAnN"
- "Environmental samples with many unknowns — SingleM vs MetaPhlAn?"
- "After binning: Deepurify or Anvi'o before GTDB-Tk?"
- "Viral contigs: geNomad → CheckV → vConTACT workflow"

### Common analysis paths

| Goal | Skills path |
|------|-------------|
| Composition only | QC → `metaphlan` / `singlem` / `kraken2` → `visualization` |
| Genome-resolved catalogue | QC → assembly → mapping → `basalt` ★ → `mag-qc` → `gtdbtk` |
| Interactive MAG polish | bins → `anvio` → re-QC |
| Viral ecology | `genomad` → `checkv` → `vcontact` |

Expected routing: `tool-selection` / `metagenomics-workflow` / `study-design`
→ stage skills.

## Next

- [Standard pipeline](standard-pipeline.md)
- [Skills catalog](skills.md)
- [Public databases](public-databases.md)
- [Troubleshooting](troubleshooting.md)
- [Compute setup](compute-setup.md)
