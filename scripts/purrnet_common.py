"""Shared cache paths and explicit version constraints for the skill and MCP."""

import os
import re
from pathlib import Path

SOURCE_URL = "https://github.com/PurrNet/PurrDocs.git"
GATE = re.compile(r"(>=|<=|==|!=|>|<)\s*(\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)")


def docs_checkout(skill_root=None):
    override = os.environ.get("PURRNET_DOCS_DIR")
    if override:
        return Path(override).expanduser().absolute()
    if skill_root is None:
        current = Path.cwd()
        skill_root = next(
            (path for path in (current, *current.parents) if (path / "SKILL.md").is_file()),
            current,
        )
    return skill_root / "references" / "cache" / "official-docs"


def parse_version(value):
    match = re.fullmatch(
        r"(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?",
        str(value).strip(),
    )
    if not match:
        return None
    pre = match[4]
    if pre and any(not part for part in pre.split(".")):
        return None
    return int(match[1]), int(match[2]), int(match[3] or 0), pre or ""


def compare(a, b):
    def precedence(version):
        pre = version[3]
        parts = tuple((0, int(p)) if p.isdigit() else (1, p) for p in pre.split("."))
        return (*version[:3], not pre, parts)

    left, right = precedence(a), precedence(b)
    return (left > right) - (left < right)


def satisfies(version, expression):
    if version is None:
        return None
    checks = list(GATE.finditer(expression))
    if not checks or GATE.sub("", expression).strip(" ,\t"):
        return None
    comparisons = []
    for check in checks:
        operator, raw = check.groups()
        other = parse_version(raw)
        if other is None:
            return None
        order = compare(version, other)
        comparisons.append({
            ">": order > 0, ">=": order >= 0, "<": order < 0,
            "<=": order <= 0, "==": order == 0, "!=": order != 0,
        }[operator])
    return all(comparisons)
