#!/usr/bin/env python3
"""Generate Codex skill wrappers for the ai-config Claude skill corpus."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("sync-codex-skill-wrappers: PyYAML is required; run `pip install pyyaml`.")

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "skills"
WRAPPER_DIR = ROOT / "codex-skills"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
GENERATED_MARKER = "This is a generated Codex wrapper around the canonical ai-config Claude skill."


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"{skill_md.relative_to(ROOT)}: missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"{skill_md.relative_to(ROOT)}: frontmatter is not a mapping")
    return data


def collapse(text: object) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def yaml_string(value: str) -> str:
    # JSON strings are valid YAML double-quoted scalars and keep this generator
    # independent of PyYAML's formatting choices.
    return json.dumps(value)


def source_skills() -> list[tuple[str, str]]:
    skills: list[tuple[str, str]] = []
    for skill_dir in sorted(SOURCE_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = parse_frontmatter(skill_md)
        name = collapse(fm.get("name", ""))
        description = collapse(fm.get("description", ""))
        if name != skill_dir.name:
            raise ValueError(
                f"{skill_md.relative_to(ROOT)}: name {name!r} does not match directory {skill_dir.name!r}"
            )
        if not description:
            raise ValueError(f"{skill_md.relative_to(ROOT)}: missing description")
        skills.append((name, description))
    return skills


def wrapper_description(name: str, source_description: str) -> str:
    return (
        f"Codex wrapper for the ai-config Claude skill `{name}`. "
        f"{source_description} "
        f"Use when Codex is asked to use `{name}`, `/{name}`, or the corresponding "
        "ai-config/Claude skill workflow."
    )


def wrapper_text(name: str, source_description: str) -> str:
    description = wrapper_description(name, source_description)
    source_path = f"../../skills/{name}/SKILL.md"
    return f"""---
name: {yaml_string(name)}
description: {yaml_string(description)}
---

# {name} (Codex wrapper)

{GENERATED_MARKER}

Source: [skills/{name}/SKILL.md]({source_path})

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/{name}/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${{CODEX_HOME:-$HOME/.codex}}/skills/{name}`, resolve the symlink target for this wrapper directory first, then read `../../skills/{name}/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${{CODEX_HOME:-$HOME/.codex}}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
"""


def generated_wrapper_dir(path: Path) -> bool:
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return False
    return GENERATED_MARKER in skill_md.read_text(encoding="utf-8")


def expected_files() -> dict[Path, str]:
    return {
        WRAPPER_DIR / name / "SKILL.md": wrapper_text(name, description)
        for name, description in source_skills()
    }


def check() -> int:
    expected = expected_files()
    problems: list[str] = []
    for path, text in expected.items():
        if not path.is_file():
            problems.append(f"missing {path.relative_to(ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != text:
            problems.append(f"stale {path.relative_to(ROOT)}")

    if WRAPPER_DIR.is_dir():
        expected_dirs = {path.parent for path in expected}
        for child in sorted(WRAPPER_DIR.iterdir()):
            if child.is_dir() and child not in expected_dirs and generated_wrapper_dir(child):
                problems.append(f"stale generated wrapper {child.relative_to(ROOT)}")

    if problems:
        print("Codex skill wrappers are out of sync:")
        for problem in problems:
            print(f"  - {problem}")
        print("\nRun `python3 scripts/sync-codex-skill-wrappers.py` to regenerate them.")
        return 1

    print(f"Codex skill wrappers are in sync ({len(expected)} wrappers).")
    return 0


def write() -> int:
    expected = expected_files()
    WRAPPER_DIR.mkdir(exist_ok=True)
    for path, text in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    expected_dirs = {path.parent for path in expected}
    for child in sorted(WRAPPER_DIR.iterdir()):
        if child.is_dir() and child not in expected_dirs and generated_wrapper_dir(child):
            shutil.rmtree(child)

    print(f"Generated {len(expected)} Codex skill wrappers in {WRAPPER_DIR.relative_to(ROOT)}/.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify wrappers without writing")
    args = parser.parse_args()
    raise SystemExit(check() if args.check else write())


if __name__ == "__main__":
    main()
