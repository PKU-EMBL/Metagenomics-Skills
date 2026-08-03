# Metagenomics Skills

**24 Agent Skills for shotgun metagenomics** — one skill per core tool (fastp,
KneadData, MetaPhlAn, HUMAnN, Kraken2, MEGAHIT, metaSPAdes, Prodigal, CD-HIT,
Salmon, eggNOG-mapper, RGI, MetaWRAP, dRep, CoverM, GTDB-Tk, CheckM2, BASALT)
plus orchestration, QC policy, and visualization.

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

### Codex / Cursor / Kimi / Grok

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills
./scripts/install-platforms.sh --user all
```

→ [docs/multi-platform.md](docs/multi-platform.md)

---

## Layout

```text
skills/<tool>/SKILL.md     # per-software instructions + analytical thinking
skills/<tool>/references/  # optional deep detail inside that skill only
docs/                      # catalogs and pipelines
.claude-plugin/ .codex-plugin/ .cursor-plugin/
scripts/install-platforms.sh
```

---

## Quick start

> Recover refined MAGs from related bioreactor samples

Expected routing: `study-design` → `fastp` → `kneaddata` → `megahit` → `basalt`
→ `checkm2` / `mag-qc`.

> Species + pathway tables only

`fastp` → `kneaddata` → `humann` (or `metaphlan` / `kraken2`) → `visualization`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New **software** skills go under
`skills/<tool-name>/` with upstream GitHub links and a clear “Analytical thinking”
section.

## License

MIT

## References

- [BASALT](https://github.com/PKU-EMBL/BASALT) · [BASALT-Air](https://github.com/PKU-EMBL/BASALT-Air)
- [Agent Skills](https://agentskills.io)
- [Anthropic Skills](https://github.com/anthropics/skills)
