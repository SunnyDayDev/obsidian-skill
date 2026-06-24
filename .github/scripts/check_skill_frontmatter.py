#!/usr/bin/env python3
"""Validate SKILL.md frontmatter for every skill in the plugin.

Checks that each skills/*/SKILL.md has YAML frontmatter with a `name` and a
`description`, and that `description` (combined with `when_to_use`, as Claude
Code does) stays within the 1,536-character budget. Exits non-zero on any
failure so it can gate CI.
"""
from __future__ import annotations

import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: pyyaml is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

MAX_DESCRIPTION = 1536
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def main() -> int:
    skills = sorted(pathlib.Path("skills").glob("*/SKILL.md"))
    if not skills:
        print("error: no skills/*/SKILL.md found", file=sys.stderr)
        return 1

    failed = False
    for path in skills:
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            print(f"{path}: missing YAML frontmatter")
            failed = True
            continue

        data = yaml.safe_load(match.group(1)) or {}
        name = data.get("name")
        description = data.get("description")

        if not name:
            print(f"{path}: frontmatter is missing 'name'")
            failed = True
        if not description:
            print(f"{path}: frontmatter is missing 'description'")
            failed = True

        combined = f"{description or ''}{data.get('when_to_use') or ''}"
        if len(combined) > MAX_DESCRIPTION:
            print(
                f"{path}: description+when_to_use is {len(combined)} chars "
                f"(max {MAX_DESCRIPTION})"
            )
            failed = True

        if name and description and len(combined) <= MAX_DESCRIPTION:
            print(f"{path}: OK (name={name}, description={len(combined)} chars)")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
