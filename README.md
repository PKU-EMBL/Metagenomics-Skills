# Metagenomics Skills

Operational protocols for shotgun metagenomic analysis, integrating
community-scale profiling (**EasyMetagenome**) with genome-resolved MAG recovery
(**PKU-EMBL BASALT / BASALT-Air**).

## Contents

```text
SKILL.md                 # Primary protocol
agents/openai.yaml       # Interface metadata
references/
  easymetagenome.md      # EasyMetagenome workflow distillation
  read-based.md          # HUMAnN / MetaPhlAn / Kraken selection
  study-design.md        # Assembly and pooling design
  end-to-end-pipeline.md # Shared preprocessing to catalogue pathway
  basalt-cli.md          # BASALT and BASALT-Air command reference
  troubleshooting.md     # BASALT diagnostics
```

## Source protocols

- Bai et al. (2025). EasyMetagenome. *iMeta*.  
  https://github.com/YongxinLiu/EasyMetagenome
- BASALT (*Nature Communications*, 2024) and BASALT-Air.  
  https://github.com/PKU-EMBL/BASALT · https://github.com/PKU-EMBL/BASALT-Air

## Installation

Clone this repository and register it as an agent skill named
`metagenomics-analysis` in your skill search path, for example:

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
mkdir -p ~/agent-skills
ln -sfn "$(pwd)/Metagenomics-Skills" ~/agent-skills/metagenomics-analysis
```

Exact skill-path conventions depend on the agent runtime in use.

## Example prompts

- Design an EasyMetagenome read-based and MetaWRAP MAG analysis for paired-end data
- Specify KneadData host depletion and MEGAHIT gene-catalogue parameters
- Plan a BASALT multi-assembly MAG recovery with a study-design manifest
- Decide between co-assembly, sample-specific assembly, and stratified subgrouping
