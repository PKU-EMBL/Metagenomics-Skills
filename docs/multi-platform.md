# Multi-platform installation

Metagenomics Skills follows the open [Agent Skills](https://agentskills.io)
`<skill-name>/SKILL.md` format. The canonical content lives only under
`skills/`; platform manifests and installers expose that same tree without
maintaining vendor-specific forks.

## Supported discovery paths

| Platform / key | User scope | Project scope | Other supported route |
|----------------|------------|---------------|-----------------------|
| Claude Code · `claude` | `~/.claude/skills` | `.claude/skills` | Claude marketplace |
| Codex · `codex` | `~/.agents/skills` | `.agents/skills` | Codex marketplace + `agents/openai.yaml` UI metadata |
| Cursor · `cursor` | `~/.cursor/skills` | `.cursor/skills` | direct Skills install; custom roots via `--target` |
| Kimi Code · `kimi` | `$KIMI_CODE_HOME/skills` (default `~/.kimi-code/skills`) | `.kimi-code/skills` | also `.agents/skills`; `--skills-dir` |
| ZCode · `zcode` | `~/.zcode/skills` | `.zcode/skills` | also `.agents/skills`; ZCode marketplace |
| Qwen Code · `qwen` | `~/.qwen/skills` | `.qwen/skills` | `qwen-extension.json` / Agent Plugins v1 |
| Grok Build · `grok` | `~/.grok/skills` | `.grok/skills` | Agent Skills directory |
| Shared · `agents` | `~/.agents/skills` | `.agents/skills` | read by Codex, Kimi Code, and ZCode |
| Shared XDG · `agents-xdg` | `${XDG_CONFIG_HOME:-~/.config}/agents/skills` | `.agents/skills` | for clients configured for XDG discovery |

Client discovery behavior changes over time. `--target /exact/path/to/skills`
is the escape hatch for any client or custom configuration not listed here.

## Installer

The Python installer works on macOS, Linux, and Windows; the shell entrypoint is
a convenience wrapper for macOS/Linux.

```bash
# Inspect support without writing
python3 scripts/install-skills.py --list-platforms
python3 scripts/install-skills.py --list-profiles

# Kimi Code, ZCode, and Qwen Code
python3 scripts/install-skills.py --user --profile core kimi zcode qwen

# One shared tree for Codex + Kimi + ZCode, plus Qwen native discovery
python3 scripts/install-skills.py --user --profile core agents qwen

# Install into another project (not necessarily this repository)
python3 scripts/install-skills.py --project \
  --project-root /path/to/project --profile genome-resolved agents qwen

# Unknown/new client
python3 scripts/install-skills.py --target ~/.new-agent/skills --profile routing

# Preview and use copies instead of links
python3 scripts/install-skills.py --target /path/to/skills \
  --profile full --mode copy --dry-run
```

The legacy command remains supported:

```bash
./scripts/install-platforms.sh --user --profile core all
```

### Installation behavior

- A platform key, `all`, or `--target PATH` is required; a bare command never
  modifies every user directory implicitly.
- `--profile full` is the backward-compatible default and exposes all 201
  skills. `core` (48 skills) is recommended when the client has a small skill
  metadata budget.
- Repeat `--profile` to union task-focused sets. With profiles, `--skill NAME`
  adds individual skills; without a profile, one or more `--skill` options form
  an individual-only selection. `--exclude NAME` removes from either selection.
- On Unix, `--mode auto` creates directory symlinks; on Windows it copies.
  If a Unix client/filesystem rejects symlinks, auto mode falls back to copies.
- Existing unrelated paths are never overwritten by default. `--force` first
  moves them under `.metagenomics-skills-backups/`; review conflicts before use.
- Copy installs are tracked by a hidden state file. An unchanged managed copy can
  be updated safely; locally modified copies are treated as conflicts.
- `--project-root` defaults to the current working directory, not the source
  repository location.
- Installation is additive by default. Add `--prune` to remove previously
  managed skills outside the requested selection. Unchanged managed paths are
  removed; edited paths become conflicts and require `--force`, which backs them
  up first.

Preview profile switching before pruning:

```bash
python3 scripts/install-skills.py --user --profile routing --prune --dry-run kimi
python3 scripts/install-skills.py --user --profile routing --prune kimi
```

Only paths recorded in that destination's hidden installer state are eligible;
unrelated directories are never pruned.

## Skill profiles

| Profile | Intended use |
|---------|--------------|
| `routing` | Planning hubs only; smallest startup catalog |
| `core` | Common read profiling, MAG recovery, mining, statistics, and routers |
| `read-profiling` | QC, host depletion, read taxonomy and function |
| `genome-resolved` | Assembly, mapping, binning, MAG QC, taxonomy and annotation |
| `mining` | BGC, AMR, virus, plasmid/MGE, metabolism and defense discovery |
| `statistics` | QC aggregation, DA, figures, networks and workflow managers |
| `ai-search` | Homology, structure, phylogenomics, genome/protein language models |
| `contamination` | Controls, contaminant evidence, and host depletion |
| `long-read` | ONT/PacBio QC, filtering, mapping, assembly, and profiling |
| `virome` | Viral discovery, quality, vOTUs, abundance, taxonomy, and hosts |
| `strain-resolved` | Marker phylogenies, cohort SNVs, and microdiversity |
| `eukaryotic` | Microbial-eukaryote contigs, genes, bins, and QC |
| `pangenome` | Prokaryotic pangenomes, annotation, dereplication, and trees |
| `metatranscriptomics` | Microbial RNA QC, rRNA removal, quantification, and function |
| `metabolic-modeling` | Genome-scale reconstruction and community simulation |
| `workflows` | Workflow engines and pinned nf-core pipelines |
| `full` | Every skill |

Profiles only control discovery/context size; they do not install the underlying
bioinformatics software or databases.

## Native package routes

### Claude Code marketplace

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

The repository includes both `.claude-plugin/marketplace.json` and
`.claude-plugin/plugin.json`.

### Codex marketplace

```bash
codex plugin marketplace add PKU-EMBL/Metagenomics-Skills
codex plugin add metagenomics@metagenomics-skills
```

Codex can consume the marketplace entry, `.codex-plugin/plugin.json`, the root
Agent Plugins v1 manifest, and optional per-skill `agents/openai.yaml` metadata.
Use the direct `.agents/skills` install when a smaller profile is preferable to
the full plugin catalog.

### Kimi Code

Use installed directories above, or load this checkout directly for one session:

```bash
kimi --skills-dir /absolute/path/to/Metagenomics-Skills/skills
```

### ZCode

The repository includes `.zcode-plugin/plugin.json` and a root
`marketplace.json`. For plugin installation, add the repository root through
**Plugin Marketplace → Add → Add Plugin Marketplace**, then install
**Metagenomics Skills**. Direct `.zcode/skills` or shared `.agents/skills`
installation is simpler when only Skills are required.

### Qwen Code

Qwen discovers native user/project directories directly. The repository also
ships `qwen-extension.json` and the portable Agent Plugins v1 `plugin.json`, so a
local development checkout can be linked using the Qwen extension command:

```bash
qwen extensions link /absolute/path/to/Metagenomics-Skills
```

Restart Qwen Code and inspect `/skills`. Extension-owned skill names may be
shown with an extension prefix; direct `.qwen/skills` installs keep plain names.

### Agent Plugins v1

`plugin.json` uses the canonical `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`
schema. Clients implementing Agent Plugins v1 can install the repository as a
portable package and discover direct children of `skills/`.

## Verify discovery

1. Start a **new** agent session or reload its Skills panel/cache.
2. Search for `metagenomics-workflow`, `tool-selection`, and `study-design`.
3. Ask: “Plan a shotgun-metagenomics workflow; do not execute.”
4. Confirm the agent loads the relevant `SKILL.md`, states assumptions, and
   proposes validation gates rather than claiming tools are already installed.

If discovery fails, see [troubleshooting](troubleshooting.md) and run a copy-mode
installation to rule out a client that does not follow directory symlinks.
