#!/usr/bin/env python3
"""Validate Agent Skills portability, package metadata, profiles, and local links."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    print("error: PyYAML is required (python3 -m pip install -r requirements-dev.txt)", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MAX_SKILL_LINES = 500
EXPECTED_VERSION = "1.22.0"
PACKAGE_NAME = "metagenomics-skills"
PLUGIN_ID = "metagenomics"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


class DuplicateJsonKeyError(ValueError):
    pass


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key: {key}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.skill_data: dict[str, dict[str, Any]] = {}
        self.description_chars = 0
        self.agent_ui_count = 0

    def error(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: Path | str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")

    def parse_yaml(self, text: str, path: Path) -> Any:
        try:
            return yaml.load(text, Loader=UniqueKeyLoader)
        except yaml.YAMLError as exc:
            self.error(path.relative_to(ROOT), f"invalid YAML: {exc}")
            return None

    def validate_skill(self, skill_dir: Path) -> None:
        relative_dir = skill_dir.relative_to(ROOT)
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            self.error(relative_dir, "missing SKILL.md")
            return
        text = skill_md.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            self.error(skill_md.relative_to(ROOT), "missing or malformed YAML frontmatter")
            return
        frontmatter, body = match.groups()
        data = self.parse_yaml(frontmatter, skill_md)
        if not isinstance(data, dict):
            self.error(skill_md.relative_to(ROOT), "frontmatter must be a mapping")
            return

        unknown = set(data) - SPEC_FIELDS
        if unknown:
            self.error(
                skill_md.relative_to(ROOT),
                "non-portable top-level fields (move custom data under metadata): " + ", ".join(sorted(unknown)),
            )

        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name) or not 1 <= len(name) <= 64:
            self.error(skill_md.relative_to(ROOT), f"invalid Agent Skills name: {name!r}")
            return
        if name != skill_dir.name:
            self.error(skill_md.relative_to(ROOT), f"name '{name}' does not match directory '{skill_dir.name}'")
        if name in self.skill_data:
            self.error(skill_md.relative_to(ROOT), f"duplicate skill name '{name}'")
        if not isinstance(description, str) or not description.strip():
            self.error(skill_md.relative_to(ROOT), "description must be a non-empty string")
        elif len(description) > 1024:
            self.error(skill_md.relative_to(ROOT), f"description is {len(description)} characters (max 1024)")
        else:
            self.description_chars += len(description)
        if data.get("license") is not None and not isinstance(data["license"], str):
            self.error(skill_md.relative_to(ROOT), "license must be a string")
        compatibility = data.get("compatibility")
        if compatibility is not None and (not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500):
            self.error(skill_md.relative_to(ROOT), "compatibility must be a 1-500 character string")
        metadata = data.get("metadata")
        if not isinstance(metadata, dict):
            self.error(skill_md.relative_to(ROOT), "metadata must be a string-to-string mapping")
        elif not all(isinstance(key, str) and isinstance(value, str) for key, value in metadata.items()):
            self.error(skill_md.relative_to(ROOT), "every metadata key and value must be a string")
        else:
            unnamespaced = sorted(key for key in metadata if not key.startswith("metagenomics."))
            if unnamespaced:
                self.error(skill_md.relative_to(ROOT), "metadata keys must use the metagenomics.* namespace")
            for key in ("metagenomics.category", "metagenomics.tags"):
                if not metadata.get(key, "").strip():
                    self.error(skill_md.relative_to(ROOT), f"metadata key '{key}' is required")
            allowed_categories = {"analysis-tools", "evaluation", "orchestration", "utilities"}
            category = metadata.get("metagenomics.category")
            if category not in allowed_categories:
                self.error(skill_md.relative_to(ROOT), f"unknown metagenomics.category: {category!r}")
        allowed_tools = data.get("allowed-tools")
        if allowed_tools is not None and not isinstance(allowed_tools, str):
            self.error(skill_md.relative_to(ROOT), "allowed-tools must be a space-separated string")
        if not body.strip():
            self.error(skill_md.relative_to(ROOT), "Markdown body is empty")
        line_count = len(text.splitlines())
        if line_count > MAX_SKILL_LINES:
            self.error(skill_md.relative_to(ROOT), f"{line_count} lines (max {MAX_SKILL_LINES})")

        for resource_dir_name in ("references", "scripts", "assets"):
            resource_dir = skill_dir / resource_dir_name
            if resource_dir.is_dir():
                for resource in resource_dir.rglob("*"):
                    if resource.is_file():
                        rel = resource.relative_to(skill_dir).as_posix()
                        if rel not in body:
                            self.error(skill_md.relative_to(ROOT), f"bundled resource is not disclosed in SKILL.md: {rel}")

        self.skill_data[name] = data

    def validate_skills(self) -> None:
        for path in sorted(SKILLS_DIR.iterdir()):
            if path.is_dir() and path.name != "_shared":
                self.validate_skill(path)
        if not self.skill_data:
            self.error("skills", "no valid skills found")

    def validate_agent_ui(self) -> None:
        for path in sorted(SKILLS_DIR.glob("*/agents/openai.yaml")):
            self.agent_ui_count += 1
            data = self.parse_yaml(path.read_text(encoding="utf-8"), path)
            relative = path.relative_to(ROOT)
            if not isinstance(data, dict):
                self.error(relative, "OpenAI UI metadata must be a mapping")
                continue
            interface = data.get("interface")
            policy = data.get("policy")
            if not isinstance(interface, dict):
                self.error(relative, "interface mapping is required")
                continue
            for key in ("display_name", "short_description", "default_prompt"):
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    self.error(relative, f"interface.{key} must be a non-empty string")
            display_name = interface.get("display_name", "")
            short_description = interface.get("short_description", "")
            default_prompt = interface.get("default_prompt", "")
            if isinstance(display_name, str) and not 3 <= len(display_name) <= 30:
                self.error(relative, "interface.display_name must be 3-30 characters")
            if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
                self.error(relative, "interface.short_description must be 25-64 characters")
            if isinstance(default_prompt, str):
                skill_name = path.parent.parent.name
                if len(default_prompt) > 200:
                    self.error(relative, "interface.default_prompt must not exceed 200 characters")
                if f"${skill_name}" not in default_prompt:
                    self.error(relative, f"interface.default_prompt must mention ${skill_name}")
            if not isinstance(policy, dict) or not isinstance(policy.get("allow_implicit_invocation"), bool):
                self.error(relative, "policy.allow_implicit_invocation must be a boolean")

    def validate_markdown_links(self) -> None:
        markdown_files = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md")) + sorted(SKILLS_DIR.rglob("*.md"))
        for path in markdown_files:
            text = path.read_text(encoding="utf-8")
            for raw_target in LINK_RE.findall(text):
                target = raw_target.strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                target = target.split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith(("mailto:", "data:")):
                    continue
                # Optional Markdown link titles are not used in this repository.
                target_path = (path.parent / unquote(target)).resolve()
                if not target_path.exists():
                    self.error(path.relative_to(ROOT), f"broken local link: {raw_target}")
                try:
                    skill_relative = path.relative_to(SKILLS_DIR)
                except ValueError:
                    continue
                if skill_relative.parts and skill_relative.parts[0] != "_shared":
                    skill_root = SKILLS_DIR / skill_relative.parts[0]
                    try:
                        target_path.relative_to(skill_root.resolve())
                    except ValueError:
                        self.error(path.relative_to(ROOT), f"skill link escapes its bundle: {raw_target}")

    def read_json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_json_object)
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            self.error(path.relative_to(ROOT), f"invalid JSON: {exc}")
            return None

    @staticmethod
    def nested(data: Any, *keys: Any) -> Any:
        value = data
        for key in keys:
            try:
                value = value[key]
            except (KeyError, IndexError, TypeError):
                return None
        return value

    def validate_manifests(self) -> None:
        locations: list[tuple[str, tuple[Any, ...]]] = [
            ("plugin-manifest.json", ("version",)),
            ("plugin.json", ("version",)),
            ("qwen-extension.json", ("version",)),
            ("marketplace.json", ("plugins", 0, "version")),
            (".claude-plugin/marketplace.json", ("version",)),
            (".claude-plugin/plugin.json", ("version",)),
            (".codex-plugin/plugin.json", ("version",)),
            (".cursor-plugin/plugin.json", ("version",)),
            (".zcode-plugin/plugin.json", ("version",)),
        ]
        loaded: dict[str, Any] = {}
        for filename, keys in locations:
            path = ROOT / filename
            data = self.read_json(path)
            loaded[filename] = data
            if not isinstance(data, dict):
                self.error(filename, "manifest root must be an object")
                continue
            if self.nested(data, *keys) != EXPECTED_VERSION:
                self.error(filename, f"version must be {EXPECTED_VERSION}")
            if not isinstance(data.get("name"), str) or not data["name"].strip():
                self.error(filename, "non-empty name is required")

        marketplace_name_files = ("marketplace.json", ".claude-plugin/marketplace.json")
        for filename in marketplace_name_files:
            data = loaded.get(filename)
            if isinstance(data, dict) and data.get("name") != PACKAGE_NAME:
                self.error(filename, f"name must be {PACKAGE_NAME!r}")

        plugin_id_files = (
            "plugin.json",
            "qwen-extension.json",
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            ".cursor-plugin/plugin.json",
            ".zcode-plugin/plugin.json",
        )
        for filename in plugin_id_files:
            data = loaded.get(filename)
            if isinstance(data, dict) and data.get("name") != PLUGIN_ID:
                self.error(filename, f"name must be {PLUGIN_ID!r}")

        for filename in ("qwen-extension.json", ".zcode-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
            data = loaded.get(filename)
            if not isinstance(data, dict):
                continue
            skill_path = data.get("skills")
            resolved = (ROOT / skill_path).resolve() if isinstance(skill_path, str) else None
            try:
                if resolved is None or not resolved.is_dir():
                    raise ValueError
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                self.error(filename, f"skills path must resolve inside the package: {skill_path!r}")

        root_marketplace = loaded.get("marketplace.json")
        if isinstance(root_marketplace, dict):
            entry = self.nested(root_marketplace, "plugins", 0)
            if not isinstance(entry, dict) or entry.get("name") != PLUGIN_ID or entry.get("source") != "./":
                self.error("marketplace.json", "first plugin must reference metagenomics from './'")

        claude_marketplace = loaded.get(".claude-plugin/marketplace.json")
        claude_plugin = loaded.get(".claude-plugin/plugin.json")
        if isinstance(claude_marketplace, dict) and isinstance(claude_plugin, dict):
            entry = self.nested(claude_marketplace, "plugins", 0)
            if not isinstance(entry, dict) or entry.get("name") != PLUGIN_ID or entry.get("source") != "./":
                self.error(".claude-plugin/marketplace.json", "first plugin must match plugin ID and source './'")

        manifest = loaded.get("plugin-manifest.json")
        if isinstance(manifest, dict):
            actual_count = len(self.skill_data)
            if manifest.get("skills_count") != actual_count:
                self.error("plugin-manifest.json", f"skills_count is {manifest.get('skills_count')}; expected {actual_count}")
            featured = manifest.get("featured_skills", [])
            missing = set(featured) - set(self.skill_data) if isinstance(featured, list) else {"<invalid featured_skills>"}
            if missing:
                self.error("plugin-manifest.json", "missing featured skills: " + ", ".join(sorted(missing)))
            categories = Counter(
                data.get("metadata", {}).get("metagenomics.category")
                for data in self.skill_data.values()
            )
            if manifest.get("skill_categories") != dict(categories):
                self.error("plugin-manifest.json", f"skill_categories does not match {dict(categories)}")

        generic = loaded.get("plugin.json")
        if isinstance(generic, dict):
            expected_schema = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
            if generic.get("$schema") != expected_schema:
                self.error("plugin.json", f"$schema must be {expected_schema}")
            allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
            extra = set(generic) - allowed
            if extra:
                self.error("plugin.json", "fields not allowed by Agent Plugins v1: " + ", ".join(sorted(extra)))
            plugin_name = generic.get("name")
            plugin_name_re = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
            if not isinstance(plugin_name, str) or len(plugin_name) > 64 or not plugin_name_re.fullmatch(plugin_name):
                self.error("plugin.json", "invalid Agent Plugins v1 name")
            for key in ("version", "description", "homepage", "repository", "license"):
                if key in generic and not isinstance(generic[key], str):
                    self.error("plugin.json", f"{key} must be a string")
            author = generic.get("author")
            if author is not None:
                if not isinstance(author, dict) or set(author) - {"name", "email", "url"} or not all(isinstance(value, str) for value in author.values()):
                    self.error("plugin.json", "author must contain only string name/email/url fields")
            keywords = generic.get("keywords")
            if keywords is not None and (not isinstance(keywords, list) or not all(isinstance(value, str) for value in keywords)):
                self.error("plugin.json", "keywords must be an array of strings")
            extensions = generic.get("extensions")
            if extensions is not None and (not isinstance(extensions, dict) or not all(isinstance(value, dict) for value in extensions.values())):
                self.error("plugin.json", "extensions must map namespaces to objects")

    def resolve_profile(self, name: str, profiles: dict[str, Any], stack: tuple[str, ...] = ()) -> set[str]:
        if name in stack:
            self.error("config/skill-profiles.json", f"profile cycle: {' -> '.join((*stack, name))}")
            return set()
        entry = profiles.get(name)
        if not isinstance(entry, dict):
            self.error("config/skill-profiles.json", f"profile '{name}' must be an object")
            return set()
        skill_names = entry.get("skills", [])
        includes = entry.get("include", [])
        if not isinstance(skill_names, list) or not all(isinstance(skill, str) for skill in skill_names):
            self.error("config/skill-profiles.json", f"profile '{name}'.skills must be a list of strings")
            skill_names = []
        if not isinstance(includes, list) or not all(isinstance(parent, str) for parent in includes):
            self.error("config/skill-profiles.json", f"profile '{name}'.include must be a list of strings")
            includes = []
        if len(skill_names) != len(set(skill_names)):
            self.error("config/skill-profiles.json", f"profile '{name}'.skills contains duplicates")
        if len(includes) != len(set(includes)):
            self.error("config/skill-profiles.json", f"profile '{name}'.include contains duplicates")
        selected = set(skill_names)
        for parent in includes:
            if parent not in profiles:
                self.error("config/skill-profiles.json", f"profile '{name}' includes unknown profile '{parent}'")
            else:
                selected.update(self.resolve_profile(parent, profiles, (*stack, name)))
        missing = selected - set(self.skill_data)
        if missing:
            self.error("config/skill-profiles.json", f"profile '{name}' has missing skills: {', '.join(sorted(missing))}")
        return selected

    def validate_profiles(self) -> None:
        path = ROOT / "config" / "skill-profiles.json"
        data = self.read_json(path)
        if not isinstance(data, dict) or not isinstance(data.get("profiles"), dict):
            self.error(path.relative_to(ROOT), "profiles object is required")
            return
        profiles = data["profiles"]
        for name in profiles:
            self.resolve_profile(name, profiles)
        manifest = self.read_json(ROOT / "plugin-manifest.json")
        if isinstance(manifest, dict):
            expected = {"full", *profiles.keys()}
            declared = set(manifest.get("skill_profiles", []))
            if declared != expected:
                self.error("plugin-manifest.json", f"skill_profiles must be {sorted(expected)}")

    def validate_docs_count(self) -> None:
        path = ROOT / "docs" / "skills.md"
        text = path.read_text(encoding="utf-8")
        match = re.search(r"Total: \*\*(\d+)\*\* skills", text)
        if not match or int(match.group(1)) != len(self.skill_data):
            self.error(path.relative_to(ROOT), f"catalog total must be {len(self.skill_data)}")

    def run(self) -> int:
        self.validate_skills()
        self.validate_agent_ui()
        self.validate_markdown_links()
        self.validate_manifests()
        self.validate_profiles()
        self.validate_docs_count()

        for warning in self.warnings:
            print(f"warning: {warning}")
        for error in self.errors:
            print(f"error: {error}", file=sys.stderr)
        print(
            f"Validated {len(self.skill_data)} skills and {self.agent_ui_count} UI manifests; "
            f"catalog descriptions={self.description_chars} characters; "
            f"warnings={len(self.warnings)}; errors={len(self.errors)}"
        )
        return 1 if self.errors else 0


if __name__ == "__main__":
    raise SystemExit(Validator().run())
