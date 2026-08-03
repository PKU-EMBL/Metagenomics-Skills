# Contributing to Metagenomics Skills

Thank you for contributing. This repository packages **Metagenomics Skills** as
portable Agent Skills (see [agentskills.io](https://agentskills.io) and
[Anthropic Skills](https://github.com/anthropics/skills)): one directory per
skill under `skills/`, plus docs and multi-platform plugin manifests.

## Skill structure

```text
skills/
  skill-name/
    SKILL.md                 # required
    agents/openai.yaml       # recommended (Codex UI)
    references/              # optional progressive disclosure
    scripts/                 # optional helpers
    assets/                  # optional templates
```

Do **not** add a repository-root `references/` tree for skill content. Deep
detail belongs inside each skill's own `references/` folder.

## Required frontmatter

```yaml
---
name: skill-name
description: >
  What it does. Use this skill when: (1) ..., (2) ..., (3) ...
  For related work, use other-skill.
license: MIT
category: analysis-tools | evaluation | utilities | orchestration
tags: [relevant, tags]
---
```

## Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `analysis-tools` | Core analysis stages | preprocessing, basalt |
| `evaluation` | Metrics and figures | mag-qc, visualization |
| `utilities` | Setup / access | setup |
| `orchestration` | Routing and pipelines | tool-selection, metagenomics-workflow |

## Checklist for new skills

- [ ] `SKILL.md` under 500 lines
- [ ] Frontmatter complete
- [ ] Cross-links to related skills
- [ ] `agents/openai.yaml` present
- [ ] Listed in `docs/skills.md` and `plugin-manifest.json`
- [ ] No vendor-specific Cursor trailers in commits
- [ ] Works via `scripts/install-platforms.sh`

## Multi-platform

Update manifests if packaging changes:

- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `plugin-manifest.json`
- `docs/multi-platform.md`
