# Repository agent guide

## Scope

This repository contains portable Agent Skills for shotgun metagenomics. The
canonical source is `skills/<name>/SKILL.md`; client manifests and installers
must point to that one tree rather than fork its content.

## Editing rules

- Follow the Agent Skills specification. Keep only `name`, `description`,
  `license`, `compatibility`, `metadata`, and `allowed-tools` at frontmatter
  top level.
- Put package-specific values under string-to-string `metadata` keys prefixed
  with `metagenomics.`.
- Keep each skill self-contained. A relative resource link must remain inside
  its skill directory; use an HTTPS link for repository-wide documentation.
- Keep `SKILL.md` under 500 lines and disclose every bundled reference or script
  from the main file with guidance on when to read or run it.
- If `agents/openai.yaml` is present, keep its UI strings within the validated
  limits and make `default_prompt` invoke `$<skill-name>` explicitly.
- Commands must preserve paired-read identity, quote paths, create output
  directories, capture logs, and include a verification step.
- Do not claim a command, database download, or analysis succeeded unless its
  output was actually inspected. Separate computational hypotheses from
  experimentally validated claims.

## When adding or removing a skill

Update `docs/skills.md`, `plugin-manifest.json`, and any relevant profile in
`config/skill-profiles.json`. Keep all manifest versions synchronized for a
release.

## Validation

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate-skills.py
python3 scripts/install-skills.py --list-profiles
```

Use `--target "$(mktemp -d)/skills" --profile routing --mode copy` for an
installer smoke test. Do not install into a real user directory during tests.
