# Metagenomics Skills

**11 Agent Skills for shotgun metagenomics** — study design, preprocessing,
read-based profiling, gene catalogues, classical MAG recovery, and PKU-EMBL
BASALT / BASALT-Air refined workflows.

[Getting started](docs/getting-started.md) ·
[Skills](docs/skills.md) ·
[Pipeline](docs/standard-pipeline.md) ·
[Platforms](docs/multi-platform.md)

---

## Install

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Codex

Clone this repository and register `.codex-plugin/plugin.json` through a Codex
marketplace entry (`"skills": "./skills/"`). Each skill includes
`agents/openai.yaml`.

### Cursor / Kimi / Grok / shared Agents

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills
./scripts/install-platforms.sh --user all
```

→ Full matrix: [docs/multi-platform.md](docs/multi-platform.md)

---

## Repository layout

```text
skills/                      # one directory per skill (SKILL.md + optional references/)
docs/                        # getting started, catalog, pipeline, platforms
.claude-plugin/              # Claude Code marketplace
.codex-plugin/               # Codex plugin manifest
.cursor-plugin/              # Cursor helper manifest
plugin-manifest.json         # package metadata
scripts/install-platforms.sh # multi-platform symlinks
```

Skill-local `references/` folders are for progressive disclosure inside a skill.
There is **no** repository-root skill `references/` tree.

---

## Skills at a glance

| Category | Skills |
|----------|--------|
| Analysis tools | `preprocessing`, `read-based`, `gene-catalogue`, `mag-classical`, `basalt` |
| Evaluation | `mag-qc`, `visualization` |
| Utilities | `setup` |
| Orchestration | `tool-selection`, `metagenomics-workflow`, `study-design` |

→ [docs/skills.md](docs/skills.md)

---

## Pipeline

```text
preprocessing → read-based and/or gene-catalogue
                      ↓
               mag-classical or basalt
                      ↓
                  mag-qc → visualization
```

→ [docs/standard-pipeline.md](docs/standard-pipeline.md)

---

## Quick start

> Plan a shotgun MAG analysis for related bioreactor time points

Expected routing: `study-design` + `tool-selection` → `preprocessing` →
`gene-catalogue` → `basalt` or `mag-classical` → `mag-qc`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New skills belong under `skills/<name>/`.

## License

MIT

## References

- [BASALT](https://github.com/PKU-EMBL/BASALT) · [BASALT-Air](https://github.com/PKU-EMBL/BASALT-Air)
- [Agent Skills](https://agentskills.io)
- [Anthropic Skills](https://github.com/anthropics/skills)
