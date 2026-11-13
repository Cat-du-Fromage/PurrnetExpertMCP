#!/usr/bin/env python3
"""Validate a *declaration* of PurrNet testing evidence; does not execute Unity tests.

Strictly distinguishes observed success, failure, not run, and not applicable.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

VALID_STATUS = {"pass", "fail", "not_run", "na"}
GATES = [f"D{i}" for i in range(7)]


def verify(document: dict, base: Path) -> list[str]:
    errors: list[str] = []
    if document.get("schema") != "purrnet-expert-evidence-v1":
        errors.append("Unsupported evidence schema")
    gates = document.get("gates")
    if not isinstance(gates, dict):
        return errors + ["Missing gates object"]
    for gate in GATES:
        entry = gates.get(gate)
        if not isinstance(entry, dict):
            errors.append(f"Missing gate {gate}")
            continue
        status = entry.get("status")
        evidence = entry.get("evidence")
        if status not in VALID_STATUS:
            errors.append(f"Invalid status {gate}: {status!r}")
        if not isinstance(evidence, list) or not all(isinstance(e, str) for e in evidence):
            errors.append(f"Invalid evidence list {gate}")
            continue
        if status in ("pass", "fail"):
            if not evidence:
                errors.append(f"Observed {status} without evidence {gate}")
            else:
                for item in evidence:
                    if item.startswith(("http://", "https://")):
                        errors.append(f"Evidence {gate} must use a local trace/log path, not unverified URL")
                    else:
                        candidate = (base / item).resolve()
                        if not candidate.is_relative_to(base.resolve()) or not candidate.is_file() or candidate.stat().st_size == 0:
                            errors.append(f"Missing, empty, or unsafe evidence file {gate}: {item}")
        elif evidence:
            errors.append(f"Unobserved {gate} cannot carry success/failure evidence")
    # Higher gates require the relevant lower gates (D4 implies compilation + working API).
    def passed(g):
        return isinstance(gates.get(g), dict) and gates[g].get("status") == "pass"
    for high, required in (("D4", ("D2", "D3")), ("D5", ("D2", "D3", "D4")), ("D6", ("D2", "D3", "D4"))):
        if passed(high):
            for lower in required:
                if not passed(lower):
                    errors.append(f"{high} cannot pass without {lower} passing")
    if not document.get("task"):
        errors.append("Task description is required")
    return errors


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("evidence_file", type=Path)
    p.add_argument("--project", type=Path, help="Optional project context; evidence paths remain relative to evidence manifest")
    args = p.parse_args(argv)
    path = args.evidence_file.resolve()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        errs = verify(doc, path.parent)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"ERROR: {e}")
        return 2
    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        return 1
    print("OK: evidence declaration structurally consistent. NOT independent verification of Unity results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
