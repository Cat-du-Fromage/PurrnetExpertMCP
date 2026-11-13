#!/usr/bin/env python3
"""Heuristic host->dedicated readiness triage for PurrNet Unity projects.

Scans project Assets/**/*.cs and relevant Unity scene text, not package caches or secrets.
Only finds candidates for human review; does not establish whether code is buggy.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

CODES = {
    "HOST_DEPENDENCY": ("review", "Check whether gameplay gated by isHost must also execute on a dedicated server (isServer)."),
    "HOST_START": ("review", "Audit StartHost on dedicated; a dedicated process should start server only."),
    "OBSERVER_RPC_SERVER_INIT": ("review", "Verify whether this ObserversRpc must also initialize server state; prefer explicit server logic or runLocally when justified."),
    "ASYNC_CLIENT_START": ("review", "Check that the connect loop waits for asynchronous StartClient to leave initial Disconnected before retry/failure."),
    "HEADLESS_CLIENT_API": ("review", "Check client-only Camera/Input/audio/UI usage on a headless server path; guard or move to client/view path."),
    "MULTIPLE_STARTERS": ("review", "Multiple StartServer/StartClient sites: inspect runtime ownership and auto-start flags to avoid duplicate starts."),
    "AUTO_START_CONFIG": ("info", "Found possible NetworkManager start flags; verify Editor, server and client build behavior in Inspector."),
    "PORT_OVERRIDE": ("info", "Port/address assignment; ensure internal listener and external client port use correct mapping."),
}

PATTERNS = [
    ("HOST_DEPENDENCY", re.compile(r"\b(?:isHost|\.isHost)\b")),
    ("HOST_START", re.compile(r"\bStartHost\s*\(")),
    ("PORT_OVERRIDE", re.compile(r"\b(?:serverPort|\.address|ListenPort)\s*=")),
]


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _report(path: Path, root: Path, text: str, pos: int, code: str) -> dict:
    line = _line(text, pos)
    lines = text.splitlines()
    # Do not include unbounded potentially secret-bearing lines in the report.
    excerpt = (lines[line - 1].strip() if line - 1 < len(lines) else "")[:150]
    if re.search(r"token|password|secret|api.?key|authorization", excerpt, re.I):
        excerpt = "[redacted: may contain a credential]"
    return {"code": code, "severity": CODES[code][0], "file": path.relative_to(root).as_posix(),
            "line": line, "excerpt": excerpt, "check": CODES[code][1]}


def analyze_project(root: Path) -> dict:
    root = root.resolve()
    if not (root / "Assets").exists():
        raise ValueError("Unity Assets directory not found")
    findings = []
    reads = 0
    sites = []
    for path in sorted((root / "Assets").rglob("*.cs")):
        if not path.is_file() or path.stat().st_size > 1_500_000:
            continue
        try:
            source = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        reads += 1
        # Approximate, line-preserving comment removal: do not treat commented-out code as evidence.
        source = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group()), source, flags=re.S)
        source = re.sub(r"//[^\n]*", lambda m: " " * len(m.group()), source)
        network_related = bool(re.search(r"\b(?:NetworkBehaviour|NetworkIdentity|NetworkManager|PurrNet|ObserversRpc|ServerRpc)\b", source))
        for code, regex in PATTERNS:
            for m in regex.finditer(source):
                findings.append(_report(path, root, source, m.start(), code))
        for m in re.finditer(r"\[\s*ObserversRpc\b[^\]]*\]", source):
            if "runLocally" not in m.group():
                findings.append(_report(path, root, source, m.start(), "OBSERVER_RPC_SERVER_INIT"))
        # Potential error: StartClient followed by polling `Disconnected` in same small block.
        for m in re.finditer(r"\bStartClient\s*\([^)]*\)\s*;", source):
            block = source[m.end():m.end() + 420]
            if re.search(r"(?:clientState|ClientState|\.state)\s*(?:==|!=)\s*(?:\w+\.)?Disconnected", block):
                findings.append(_report(path, root, source, m.start(), "ASYNC_CLIENT_START"))
        if network_related:
            for m in re.finditer(r"\b(?:Camera\.main|Input\.(?:GetKey|GetAxis|GetButton|mousePosition)|\.PlayOneShot\s*\(|\.Play\s*\()", source):
                findings.append(_report(path, root, source, m.start(), "HEADLESS_CLIENT_API"))
        for m in re.finditer(r"\b(?:StartServer|StartClient)\s*\(", source):
            sites.append((path, m.start(), source))
    if len(sites) > 1:
        for path, pos, source in sites[:20]:
            findings.append(_report(path, root, source, pos, "MULTIPLE_STARTERS"))
    for path in sorted((root / "Assets").rglob("*.unity")):
        try:
            if path.stat().st_size > 1_500_000:
                continue
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        for m in re.finditer(r"(?im)^\s*(?:_?start(?:Server|Client)Flags|_?autoStart(?:Server|Client))\s*:", text):
            findings.append(_report(path, root, text, m.start(), "AUTO_START_CONFIG"))
    findings.sort(key=lambda x: (x["file"], x["line"], x["code"]))
    return {"schema": "purrnet-dedicated-readiness-v1", "project": str(root), "cs_files_scanned": reads,
            "findings": findings, "count": len(findings),
            "disclaimer": "Heuristic candidates only. Findings do not prove a defect; zero findings does not prove dedicated readiness."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project", type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    try:
        report = analyze_project(args.project)
    except (OSError, ValueError) as e:
        p.error(str(e))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Scanned {report['cs_files_scanned']} .cs; {report['count']} items for manual review")
        for f in report["findings"]:
            print(f"{f['severity']}: {f['file']}:{f['line']} [{f['code']}] {f['check']}")
        print(report["disclaimer"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
