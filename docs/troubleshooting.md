# Troubleshooting

## Skills not loading

1. Confirm `skills/<name>/SKILL.md` exists
2. Re-run `./scripts/install-platforms.sh` for your platform
3. Restart the agent session
4. For Claude, reinstall the marketplace plugin

## Missing bioinformatics binaries

Skills describe workflows; they do not install Conda packages automatically.
Use the `setup` skill and verify with `command -v`.

## BASALT failures

Use the `basalt` skill hard rules:

- one run directory
- unchanged provenance for `--mode continue`
- validate `BASALT_WEIGHT` (5 ensemble CSVs) and CheckM2 DB

Do not use `chmod 777` or `sudo` for installs.

## PE pairing errors

Re-run KneadData with `--reorder` and compare read headers before MetaWRAP,
salmon, or BASALT.
