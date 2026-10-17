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

Use only fields allowed by the portable Agent Skills specification. Package
annotations belong under string-to-string `metadata` keys:

```yaml
---
name: skill-name
description: >
  What it does and when the agent should use it. Mention adjacent skills when
  that prevents false triggering.
license: MIT
metadata:
  metagenomics.category: "analysis-tools"
  metagenomics.tags: "relevant, comma-separated, tags"
  metagenomics.upstream: "https://example.org/upstream"
  metagenomics.stage: "assembly"
---
```

Do not add vendor-only top-level keys. If a client-specific field is essential,
document the compatibility trade-off and keep the canonical skill usable by
clients that ignore it.

Optional Codex UI metadata lives in `agents/openai.yaml`. Keep `display_name`
at 3–30 characters, `short_description` at 25–64, and `default_prompt` at no
more than 200 characters. The prompt must invoke `$<skill-name>` and require
input inspection and output verification.

## Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `analysis-tools` | Core analysis stages | preprocessing, basalt |
| `evaluation` | Metrics and figures | mag-qc, visualization |
| `utilities` | Setup / access | setup |
| `orchestration` | Routing and pipelines | tool-selection, metagenomics-workflow |

## Checklist for new skills

- [ ] `SKILL.md` under 500 lines with a precise what+when description
- [ ] Portable frontmatter complete; directory and `name` match
- [ ] Commands validate inputs, quote paths, capture logs, and verify outputs
- [ ] Cross-links to related skills; every bundled resource disclosed from `SKILL.md`
- [ ] No relative link escapes the skill bundle
- [ ] Optional `agents/openai.yaml` included only when useful for Codex UI metadata
- [ ] Listed in `docs/skills.md` and counted in `plugin-manifest.json`
- [ ] Added to a task profile when appropriate
- [ ] `python3 scripts/validate-skills.py` passes
- [ ] Installer copy-mode smoke test passes

## Multi-platform

Update all applicable package surfaces when packaging or versions change:

- portable `plugin.json` (Agent Plugins v1)
- `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.zcode-plugin/plugin.json` and root `marketplace.json`
- `qwen-extension.json`
- `plugin-manifest.json`
- `config/skill-profiles.json` and `docs/multi-platform.md`

Run locally:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate-skills.py
python3 scripts/install-skills.py --list-profiles
python3 scripts/install-skills.py --target "$(mktemp -d)/skills" \
  --profile routing --mode copy
```
