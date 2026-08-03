# Metagenomics Skills

Shotgun metagenomics protocols organized by analytical module: study design,
preprocessing, read-based profiling, gene catalogues, classical MAG recovery,
and PKU-EMBL BASALT / BASALT-Air refined MAG recovery.

## Contents

```text
SKILL.md
agents/openai.yaml
references/
  study-design.md        # Module A
  preprocessing.md       # Module B
  read-based.md          # Module C
  gene-catalogue.md      # Module D
  mag-classical.md       # Module E
  basalt-cli.md          # Module F
  visualization.md       # Module G
  end-to-end-pipeline.md # Module H
  troubleshooting.md     # Module I
```

## Source protocols

- BASALT (*Nature Communications*, 2024) and BASALT-Air  
  https://github.com/PKU-EMBL/BASALT · https://github.com/PKU-EMBL/BASALT-Air

## Installation

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
mkdir -p ~/agent-skills
ln -sfn "$(pwd)/Metagenomics-Skills" ~/agent-skills/metagenomics-analysis
```

## Example prompts

- Route a paired-end study into read-based profiling versus MAG recovery
- Specify KneadData host depletion and MEGAHIT gene-catalogue parameters
- Plan a BASALT multi-assembly MAG analysis with a study-design manifest
- Decide between co-assembly, sample-specific assembly, and subgrouping
