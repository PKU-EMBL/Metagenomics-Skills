# Multi-platform install

Metagenomics Skills uses the portable [Agent Skills](https://agentskills.io)
`skills/<name>/SKILL.md` layout. Platform manifests adapt the same tree.

## Canonical layout

```text
skills/
  preprocessing/SKILL.md
  basalt/SKILL.md
  ...
.claude-plugin/marketplace.json   # Claude Code marketplace
.codex-plugin/plugin.json         # Codex plugin manifest
.cursor-plugin/plugin.json        # Cursor helper manifest
plugin-manifest.json              # package metadata
scripts/install-platforms.sh      # symlink installer
```

## Platform paths

| Platform | User skills directory | Project skills directory | Plugin entry |
|----------|----------------------|--------------------------|--------------|
| Claude Code | `~/.claude/skills` | `.claude/skills` | `.claude-plugin/marketplace.json` |
| Codex | `~/.agents/skills` | `.agents/skills` | `.codex-plugin/plugin.json` |
| Cursor | `~/.cursor/skills` | `.cursor/skills` | `.cursor-plugin/plugin.json` |
| Kimi Code | `~/.kimi-code/skills` (or `$KIMI_CODE_HOME/skills`) | `.kimi-code/skills` | Agent Skills dirs |
| Grok Build | `~/.grok/skills` | `.grok/skills` | Agent Skills dirs |
| Shared Agents | `~/.agents/skills` | `.agents/skills` | — |

## Installer

```bash
./scripts/install-platforms.sh --user all
./scripts/install-platforms.sh --project claude codex kimi
./scripts/install-platforms.sh --user cursor grok
```

The script symlinks each skill directory (except `_shared`) into the target
skills root so all platforms see identical content.

## Claude marketplace

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

## Codex plugin

Point a Codex marketplace entry at this repository root (contains
`.codex-plugin/plugin.json` with `"skills": "./skills/"`). Each skill also
ships `agents/openai.yaml` for Codex UI metadata.

## Notes

- Restart / reload the agent session after installing
- Do not duplicate skills by copying; prefer symlinks from this repo
- Keep analysis tool envs separate from the skill install
