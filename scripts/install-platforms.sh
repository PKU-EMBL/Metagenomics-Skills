#!/usr/bin/env bash
# Install Metagenomics Skills into one or more agent skill directories.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$ROOT/skills"

usage() {
  cat <<'EOF'
Usage: scripts/install-platforms.sh [--user|--project] [platform...]

Platforms:
  all       Install for every supported platform (default)
  claude    ~/.claude/skills  or  .claude/skills
  codex     ~/.agents/skills  or  .agents/skills  (also Codex plugin path)
  cursor    ~/.cursor/skills  or  .cursor/skills
  kimi      ~/.kimi-code/skills  or  .kimi-code/skills
  grok      ~/.grok/skills  or  .grok/skills
  agents    ~/.agents/skills  or  .agents/skills

Examples:
  scripts/install-platforms.sh --user all
  scripts/install-platforms.sh --project claude codex kimi
EOF
}

SCOPE=user
PLATFORMS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) SCOPE=user; shift ;;
    --project) SCOPE=project; shift ;;
    -h|--help) usage; exit 0 ;;
    *) PLATFORMS+=("$1"); shift ;;
  esac
done
[[ ${#PLATFORMS[@]} -eq 0 ]] && PLATFORMS=(all)

resolve_dir() {
  local platform="$1"
  if [[ "$SCOPE" == project ]]; then
    case "$platform" in
      claude) echo "$ROOT/.claude/skills" ;;
      codex|agents) echo "$ROOT/.agents/skills" ;;
      cursor) echo "$ROOT/.cursor/skills" ;;
      kimi) echo "$ROOT/.kimi-code/skills" ;;
      grok) echo "$ROOT/.grok/skills" ;;
      *) return 1 ;;
    esac
  else
    case "$platform" in
      claude) echo "${HOME}/.claude/skills" ;;
      codex|agents) echo "${HOME}/.agents/skills" ;;
      cursor) echo "${HOME}/.cursor/skills" ;;
      kimi) echo "${KIMI_CODE_HOME:-$HOME/.kimi-code}/skills" ;;
      grok) echo "${HOME}/.grok/skills" ;;
      *) return 1 ;;
    esac
  fi
}

install_into() {
  local dest_root="$1"
  mkdir -p "$dest_root"
  local skill
  for skill in "$SKILLS_SRC"/*; do
    [[ -d "$skill" ]] || continue
    local name
    name="$(basename "$skill")"
    [[ "$name" == _shared ]] && continue
    ln -sfn "$skill" "$dest_root/$name"
    echo "linked $name -> $dest_root/$name"
  done
}

expand_platforms() {
  local p
  for p in "${PLATFORMS[@]}"; do
    if [[ "$p" == all ]]; then
      echo claude codex cursor kimi grok agents
      return
    fi
    echo "$p"
  done
}

for platform in $(expand_platforms | tr ' ' '\n' | awk 'NF' | sort -u); do
  dest="$(resolve_dir "$platform")" || {
    echo "unknown platform: $platform" >&2
    exit 1
  }
  echo "==> $platform ($SCOPE): $dest"
  install_into "$dest"
done

echo
echo "Done. Restart or reload your agent session to pick up skills."
echo "Claude marketplace: /plugin marketplace add PKU-EMBL/Metagenomics-Skills"
echo "Codex plugin:       see docs/multi-platform.md"
