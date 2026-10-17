#!/usr/bin/env python3
"""Install Metagenomics Skills into user, project, or custom agent directories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from uuid import uuid4

PACKAGE = "metagenomics-skills"
ROOT = Path(__file__).resolve().parent.parent
SKILLS_SOURCE = ROOT / "skills"
PROFILES_FILE = ROOT / "config" / "skill-profiles.json"
STATE_FILE = ".metagenomics-skills-install.json"


@dataclass(frozen=True)
class Platform:
    user_dir: Callable[[], Path]
    project_dir: str
    description: str


def home_path(*parts: str) -> Path:
    return Path.home().joinpath(*parts)


def kimi_user_dir() -> Path:
    base = Path(os.environ.get("KIMI_CODE_HOME", home_path(".kimi-code"))).expanduser()
    return base / "skills"


def xdg_agents_dir() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME", home_path(".config"))).expanduser()
    return base / "agents" / "skills"


PLATFORMS: dict[str, Platform] = {
    "claude": Platform(lambda: home_path(".claude", "skills"), ".claude/skills", "Claude Code"),
    "codex": Platform(lambda: home_path(".agents", "skills"), ".agents/skills", "OpenAI Codex"),
    "cursor": Platform(lambda: home_path(".cursor", "skills"), ".cursor/skills", "Cursor"),
    "kimi": Platform(kimi_user_dir, ".kimi-code/skills", "Kimi Code"),
    "zcode": Platform(lambda: home_path(".zcode", "skills"), ".zcode/skills", "ZCode"),
    "qwen": Platform(lambda: home_path(".qwen", "skills"), ".qwen/skills", "Qwen Code"),
    "grok": Platform(lambda: home_path(".grok", "skills"), ".grok/skills", "Grok Build"),
    "agents": Platform(lambda: home_path(".agents", "skills"), ".agents/skills", "shared .agents"),
    "agents-xdg": Platform(xdg_agents_dir, ".agents/skills", "shared XDG agents"),
}

ALIASES = {
    "claude-code": "claude",
    "kimi-code": "kimi",
    "z-code": "zcode",
    "qwen-code": "qwen",
    "grok-build": "grok",
    "shared": "agents",
    "xdg": "agents-xdg",
}

# Native destinations. The generic .agents destination remains available explicitly
# and is shared by Codex, Kimi Code, and ZCode.
ALL_PLATFORMS = ("claude", "codex", "cursor", "kimi", "zcode", "qwen", "grok")


class InstallError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install portable SKILL.md bundles for one or more coding agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  scripts/install-skills.py --user --profile core kimi zcode qwen
  scripts/install-skills.py --project --project-root /path/to/project agents qwen
  scripts/install-skills.py --user --mode copy --profile full all
  scripts/install-skills.py --user --profile routing --prune --dry-run kimi
  scripts/install-skills.py --user --skill fastp --skill multiqc kimi
  scripts/install-skills.py --target ~/.other-agent/skills --profile routing
""",
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--user", action="store_const", const="user", dest="scope", help="install for the current user (default)")
    scope.add_argument("--project", action="store_const", const="project", dest="scope", help="install into a project")
    parser.set_defaults(scope="user")
    parser.add_argument("platforms", nargs="*", help="platform names, or 'all'")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="target project root (default: current directory)")
    parser.add_argument("--target", action="append", type=Path, default=[], help="custom skills directory; repeatable")
    parser.add_argument("--profile", action="append", default=[], help="skill profile; repeatable and combined (default: full)")
    parser.add_argument("--skill", action="append", default=[], help="select a skill by name (or add to profiles); repeatable")
    parser.add_argument("--exclude", action="append", default=[], help="exclude one skill from this selection; repeatable")
    parser.add_argument("--mode", choices=("auto", "link", "copy"), default="auto", help="installation mode (default: symlink, copy fallback)")
    parser.add_argument("--prune", action="store_true", help="remove managed skills outside the current selection")
    parser.add_argument("--force", action="store_true", help="back up and replace conflicting or locally modified paths")
    parser.add_argument("--dry-run", action="store_true", help="show planned changes without writing")
    parser.add_argument("--verbose", action="store_true", help="print every installed skill")
    parser.add_argument("--list-platforms", action="store_true", help="list supported platform keys and exit")
    parser.add_argument("--list-profiles", action="store_true", help="list skill profiles and exit")
    return parser.parse_args()


def load_profiles() -> dict[str, dict[str, object]]:
    try:
        data = json.loads(PROFILES_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallError(f"cannot read {PROFILES_FILE}: {exc}") from exc
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise InstallError(f"{PROFILES_FILE} must contain a profiles object")
    return profiles


def available_skills() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in sorted(SKILLS_SOURCE.iterdir()):
        if path.is_dir() and path.name != "_shared" and (path / "SKILL.md").is_file():
            result[path.name] = path.resolve()
    if not result:
        raise InstallError(f"no skills found under {SKILLS_SOURCE}")
    return result


def resolve_profile(
    name: str,
    profiles: dict[str, dict[str, object]],
    all_names: set[str],
    stack: tuple[str, ...] = (),
) -> set[str]:
    if name == "full":
        return set(all_names)
    if name not in profiles:
        choices = ", ".join(["full", *sorted(profiles)])
        raise InstallError(f"unknown profile '{name}'; choose from: {choices}")
    if name in stack:
        raise InstallError(f"profile cycle: {' -> '.join((*stack, name))}")
    entry = profiles[name]
    if not isinstance(entry, dict):
        raise InstallError(f"profile '{name}' must be an object")
    selected: set[str] = set()
    includes = entry.get("include", [])
    if not isinstance(includes, list) or not all(isinstance(parent, str) for parent in includes):
        raise InstallError(f"profile '{name}'.include must be a list of profile names")
    for parent in includes:
        selected.update(resolve_profile(parent, profiles, all_names, (*stack, name)))
    skills = entry.get("skills", [])
    if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
        raise InstallError(f"profile '{name}'.skills must be a list of skill names")
    selected.update(map(str, skills))
    missing = selected - all_names
    if missing:
        raise InstallError(f"profile '{name}' references missing skills: {', '.join(sorted(missing))}")
    return selected


def select_skills(args: argparse.Namespace, profiles: dict[str, dict[str, object]], skills: dict[str, Path]) -> list[str]:
    names = set(skills)
    requested_profiles = args.profile or ([] if args.skill else ["full"])
    selected: set[str] = set()
    for profile in requested_profiles:
        selected.update(resolve_profile(profile, profiles, names))
    for name in args.skill:
        if name not in names:
            raise InstallError(f"unknown skill '{name}'")
        selected.add(name)
    for name in args.exclude:
        if name not in names:
            raise InstallError(f"unknown excluded skill '{name}'")
        selected.discard(name)
    if not selected:
        raise InstallError("selection is empty")
    return sorted(selected)


def normalize_platform(name: str) -> str:
    return ALIASES.get(name, name)


def resolve_destinations(args: argparse.Namespace) -> list[tuple[str, Path]]:
    requested = list(args.platforms)
    if not requested and not args.target:
        raise InstallError("specify at least one platform (or 'all') or use --target PATH")
    expanded: list[str] = []
    for item in requested:
        item = normalize_platform(item.lower())
        if item == "all":
            expanded.extend(ALL_PLATFORMS)
        else:
            expanded.append(item)

    destinations: list[tuple[str, Path]] = []
    project_root = args.project_root.expanduser().resolve()
    for platform_name in expanded:
        platform = PLATFORMS.get(platform_name)
        if platform is None:
            choices = ", ".join(["all", *sorted(PLATFORMS), *sorted(ALIASES)])
            raise InstallError(f"unknown platform '{platform_name}'; choose from: {choices}")
        path = platform.user_dir() if args.scope == "user" else project_root / platform.project_dir
        destinations.append((platform_name, path.expanduser().absolute()))
    for index, target in enumerate(args.target, start=1):
        destinations.append((f"custom-{index}", target.expanduser().absolute()))

    # Codex and shared agents intentionally resolve to the same directory. Install once.
    deduplicated: list[tuple[str, Path]] = []
    seen: dict[str, int] = {}
    for label, path in destinations:
        key = os.path.normcase(os.path.normpath(str(path)))
        if key in seen:
            old_label, old_path = deduplicated[seen[key]]
            deduplicated[seen[key]] = (f"{old_label}+{label}", old_path)
        else:
            seen[key] = len(deduplicated)
            deduplicated.append((label, path))
    if not deduplicated:
        raise InstallError("no destination selected")
    return deduplicated


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for entry in sorted(path.rglob("*"), key=lambda item: item.as_posix()):
        relative = entry.relative_to(path).as_posix().encode()
        if entry.is_symlink():
            digest.update(b"link\0" + relative + b"\0")
            digest.update(os.readlink(entry).encode())
            digest.update(b"\0")
        elif entry.is_dir():
            digest.update(b"dir\0" + relative + b"\0")
        elif entry.is_file():
            digest.update(b"file\0" + relative + b"\0")
            with entry.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(block)
            digest.update(b"\0")
    return digest.hexdigest()


def load_state(destination: Path) -> dict[str, object]:
    state_path = destination / STATE_FILE
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"package": PACKAGE, "entries": {}}
    except (OSError, json.JSONDecodeError):
        return {"package": PACKAGE, "entries": {}}
    if state.get("package") != PACKAGE or not isinstance(state.get("entries"), dict):
        return {"package": PACKAGE, "entries": {}}
    return state


def save_state(destination: Path, state: dict[str, object], dry_run: bool) -> None:
    if dry_run:
        return
    state["package"] = PACKAGE
    state["source"] = str(ROOT)
    state["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    state_path = destination / STATE_FILE
    temporary = state_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(state_path)


def same_symlink(destination: Path, source: Path) -> bool:
    if not destination.is_symlink():
        return False
    return Path(os.path.realpath(destination)) == source.resolve()


def backup_existing(destination_root: Path, destination: Path, dry_run: bool) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = destination_root / ".metagenomics-skills-backups" / stamp / destination.name
    counter = 1
    while os.path.lexists(backup):
        backup = backup.with_name(f"{destination.name}-{counter}")
        counter += 1
    if not dry_run:
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(backup))
    return backup


def copy_skill(source: Path, destination: Path, dry_run: bool) -> None:
    if dry_run:
        return
    temporary = destination.with_name(f".{destination.name}.tmp-{uuid4().hex}")
    try:
        shutil.copytree(source, temporary, symlinks=True)
        temporary.replace(destination)
    finally:
        if os.path.lexists(temporary):
            if temporary.is_symlink() or temporary.is_file():
                temporary.unlink()
            else:
                shutil.rmtree(temporary)


def link_skill(source: Path, destination: Path, dry_run: bool) -> None:
    if not dry_run:
        destination.symlink_to(source, target_is_directory=True)


def remove_path(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def managed_path_is_unchanged(destination: Path, previous: dict[str, object]) -> bool:
    mode = previous.get("mode")
    if mode == "link" and destination.is_symlink():
        source = previous.get("source")
        return isinstance(source, str) and os.path.realpath(destination) == os.path.realpath(source)
    if mode == "copy" and destination.is_dir() and not destination.is_symlink():
        digest = previous.get("digest")
        try:
            return isinstance(digest, str) and tree_digest(destination) == digest
        except OSError:
            return False
    return False


def prune_destination(
    destination_root: Path,
    selected: set[str],
    entries: dict[str, object],
    args: argparse.Namespace,
    counts: dict[str, int],
    messages: list[str],
) -> None:
    for name in sorted(set(entries) - selected):
        if name in {"", ".", ".."} or "/" in name or "\\" in name:
            counts["conflict"] += 1
            messages.append(f"  conflict  unsafe state entry ignored: {name!r}")
            continue
        destination = destination_root / name
        previous = entries.get(name)
        if not os.path.lexists(destination):
            entries.pop(name, None)
            counts["removed"] += 1
            if args.verbose:
                messages.append(f"  removed   {name} (already absent)")
            continue

        unchanged = isinstance(previous, dict) and managed_path_is_unchanged(destination, previous)
        if not unchanged and not args.force:
            counts["conflict"] += 1
            messages.append(f"  conflict  {name}: locally changed; not removed")
            continue
        try:
            if unchanged:
                remove_path(destination, args.dry_run)
            else:
                backup = backup_existing(destination_root, destination, args.dry_run)
                messages.append(f"  backup    {name} -> {backup}")
        except OSError as exc:
            counts["failed"] += 1
            messages.append(f"  failed    {name}: could not prune path: {exc}")
            continue
        entries.pop(name, None)
        counts["removed"] += 1
        if args.verbose:
            verb = "would remove" if args.dry_run else "removed"
            messages.append(f"  {verb:<10} {name}")


def install_destination(
    label: str,
    destination_root: Path,
    selected: list[str],
    skills: dict[str, Path],
    args: argparse.Namespace,
) -> tuple[dict[str, int], list[str]]:
    counts = {"installed": 0, "updated": 0, "removed": 0, "unchanged": 0, "conflict": 0, "failed": 0}
    messages: list[str] = []
    if not args.dry_run:
        destination_root.mkdir(parents=True, exist_ok=True)
    state = load_state(destination_root)
    entries = state.setdefault("entries", {})
    assert isinstance(entries, dict)

    preferred_mode = args.mode
    if preferred_mode == "auto":
        preferred_mode = "copy" if os.name == "nt" else "link"

    for name in selected:
        source = skills[name]
        destination = destination_root / name
        previous = entries.get(name) if isinstance(entries.get(name), dict) else {}
        exists = os.path.lexists(destination)
        action = "installed"

        if exists and same_symlink(destination, source):
            if args.mode in {"auto", "link"}:
                counts["unchanged"] += 1
                entries[name] = {"mode": "link", "source": str(source)}
                if args.verbose:
                    messages.append(f"  unchanged {name}")
                continue
            action = "updated"

        source_digest: str | None = None
        if exists and destination.is_dir() and not destination.is_symlink():
            try:
                source_digest = tree_digest(source)
                current_digest = tree_digest(destination)
            except OSError as exc:
                counts["failed"] += 1
                messages.append(f"  failed    {name}: could not inspect source/destination: {exc}")
                continue
            previous_digest = previous.get("digest") if isinstance(previous, dict) else None
            previous_mode = previous.get("mode") if isinstance(previous, dict) else None
            if current_digest == source_digest:
                if args.mode in {"auto", "copy"}:
                    counts["unchanged"] += 1
                    entries[name] = {"mode": "copy", "source": str(source), "digest": source_digest}
                    if args.verbose:
                        messages.append(f"  unchanged {name}")
                    continue
                action = "updated"
            elif previous_mode == "copy" and previous_digest == current_digest:
                action = "updated"
            elif not args.force:
                counts["conflict"] += 1
                messages.append(f"  conflict  {name}: {destination} already exists and is not managed/unchanged")
                continue
            else:
                action = "updated"
        elif exists:
            previous_source = previous.get("source") if isinstance(previous, dict) else None
            managed_old_link = (
                destination.is_symlink()
                and previous.get("mode") == "link"
                and isinstance(previous_source, str)
                and os.path.realpath(destination) == os.path.realpath(previous_source)
            )
            if action == "updated" or managed_old_link:
                action = "updated"
            elif not args.force:
                counts["conflict"] += 1
                messages.append(f"  conflict  {name}: {destination} already exists")
                continue
            else:
                action = "updated"

        backup: Path | None = None
        if exists:
            try:
                backup = backup_existing(destination_root, destination, args.dry_run)
            except OSError as exc:
                counts["failed"] += 1
                messages.append(f"  failed    {name}: could not back up existing path: {exc}")
                continue
            if args.verbose or args.force:
                messages.append(f"  backup    {name} -> {backup}")

        actual_mode = preferred_mode
        try:
            if preferred_mode == "link":
                try:
                    link_skill(source, destination, args.dry_run)
                except OSError:
                    if args.mode != "auto":
                        raise
                    actual_mode = "copy"
                    source_digest = source_digest or tree_digest(source)
                    copy_skill(source, destination, args.dry_run)
            else:
                source_digest = source_digest or tree_digest(source)
                copy_skill(source, destination, args.dry_run)
        except OSError as exc:
            counts["failed"] += 1
            messages.append(f"  failed    {name}: {exc}")
            if backup is not None and not args.dry_run and not os.path.lexists(destination):
                try:
                    shutil.move(str(backup), str(destination))
                    messages.append(f"  restored  {name} after failed update")
                except OSError as restore_exc:
                    messages.append(f"  failed    {name}: could not restore backup: {restore_exc}")
            continue

        if actual_mode == "copy":
            assert source_digest is not None
            entries[name] = {"mode": "copy", "source": str(source), "digest": source_digest}
        else:
            entries[name] = {"mode": "link", "source": str(source)}
        counts[action] += 1
        if args.verbose:
            verb = "would install" if args.dry_run else action
            messages.append(f"  {verb:<10} {name} ({actual_mode})")

    if args.prune:
        prune_destination(destination_root, set(selected), entries, args, counts, messages)

    save_state(destination_root, state, args.dry_run)
    return counts, messages


def list_platforms() -> None:
    print("Supported platforms:")
    for name, platform in PLATFORMS.items():
        print(f"  {name:12} {platform.description:18} user={platform.user_dir()} project={platform.project_dir}")
    print("  all          " + ", ".join(ALL_PLATFORMS))
    print("Aliases: " + ", ".join(f"{alias}={target}" for alias, target in sorted(ALIASES.items())))


def list_profiles(profiles: dict[str, dict[str, object]], all_names: set[str]) -> None:
    print(f"  {'full':18} {len(all_names):3} skills  Every skill in the repository")
    for name in sorted(profiles):
        resolved = resolve_profile(name, profiles, all_names)
        description = str(profiles[name].get("description", ""))
        print(f"  {name:18} {len(resolved):3} skills  {description}")


def main() -> int:
    args = parse_args()
    try:
        profiles = load_profiles()
        skills = available_skills()
        if args.list_platforms:
            list_platforms()
            return 0
        if args.list_profiles:
            list_profiles(profiles, set(skills))
            return 0
        selected = select_skills(args, profiles, skills)
        destinations = resolve_destinations(args)
    except InstallError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    profile_label = "+".join(args.profile) if args.profile else ("individual" if args.skill else "full")
    mode_label = args.mode if args.mode != "auto" else ("copy" if os.name == "nt" else "link (copy fallback)")
    prefix = "DRY RUN: " if args.dry_run else ""
    print(f"{prefix}installing {len(selected)} skills (profile: {profile_label}; mode: {mode_label})")

    has_problem = False
    for label, destination in destinations:
        try:
            counts, messages = install_destination(label, destination, selected, skills, args)
        except OSError as exc:
            print(f"[{label}] {destination} — failed: {exc}", file=sys.stderr)
            has_problem = True
            continue
        summary = ", ".join(f"{key}={value}" for key, value in counts.items() if value)
        print(f"[{label}] {destination} — {summary or 'no changes'}")
        for message in messages:
            print(message)
        has_problem = has_problem or bool(counts["conflict"] or counts["failed"])

    if has_problem:
        print("Completed with conflicts/failures. Re-run with --force only after reviewing backups and paths.", file=sys.stderr)
        return 2
    print("Done. Start a new agent session (or reload Skills) to discover the installation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
