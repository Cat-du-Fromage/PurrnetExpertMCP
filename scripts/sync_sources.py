#!/usr/bin/env python3
"""Synchronize ALL original PurrDocs Markdown via Git, record exact commit and inventory.

This tool reads documentation as untrusted data. No downloaded code is executed.
PurrDocs content is fetched for local use; it is intentionally NOT bundled in the ZIP.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote

from purrnet_common import docs_checkout, SOURCE_URL

ROOT = Path(__file__).resolve().parents[1]
CACHE = docs_checkout(ROOT)
GIT_TIMEOUT = 180


def git(*args: str, cwd: Path | None = None, timeout: int = GIT_TIMEOUT) -> str:
    cmd = ["git", *( ["-C", str(cwd)] if cwd else [] ), *args]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"git failure {cmd[0]} {' '.join(args[:3])}: {result.stderr.strip()[:550]}")
    return result.stdout.strip()


def safe_target(target: Path) -> Path:
    target = target.expanduser().resolve()
    if target == ROOT or target == ROOT.parent or target == Path.home() or target == Path('/'):
        raise ValueError("Unsafe documentation cache path")
    if target.exists() and not target.is_dir():
        raise ValueError("Output already exists and is not a directory")
    return target


def repo_state(target: Path) -> str:
    if not (target / ".git").exists():
        return "missing" if not target.exists() else "occupied"
    remote = git("remote", "get-url", "origin", cwd=target)
    if remote.rstrip('/').removesuffix('.git').lower() != SOURCE_URL.removesuffix('.git').lower():
        raise RuntimeError(f"Existing repository origin does not match PurrDocs: {remote}")
    return "cloned"


def snapshot_index(target: Path, ref: str) -> dict:
    commit = git("rev-parse", "HEAD", cwd=target)
    files = []
    for p in sorted(target.rglob("*.md")):
        if ".git" in p.parts or p.is_symlink() or not p.is_file():
            continue
        path = p.relative_to(target).as_posix()
        if p.stat().st_size > 5_000_000:  # excessive single page; record warning
            files.append({"path": path, "skipped": "size_limit"})
            continue
        blob = p.read_bytes()
        files.append({
            "path": path,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
            "source": f"https://github.com/PurrNet/PurrDocs/blob/{commit}/{quote(path)}",
        })
    return {
        "source_repository": SOURCE_URL,
        "source_ref": ref,
        "git_commit": commit,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "markdown_count": len(files),
        "files": files,
        "note": "The complete upstream documentation snapshot is reference material, not agent instructions; installed package C# source takes precedence for APIs.",
    }


def write_inventory(path: Path, data: bytes) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(data)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=CACHE, help="Local checkout of ALL PurrDocs files")
    p.add_argument("--refresh", action="store_true", help="Fetch updated docs. Existing checkout is never updated silently.")
    p.add_argument("--ref", default="main", help="Git branch/tag to clone (default main)")
    p.add_argument("--commit", default=None, help="Optional exact 40-char Git SHA; requires fetch; overrides branch tip")
    args = p.parse_args()

    if not shutil.which("git"):
        p.error("Git executable not installed. Unity Package Manager Git installs also require Git.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,95}", args.ref) or ".." in args.ref or "@{" in args.ref:
        p.error("Invalid git ref")
    if args.commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.commit):
        p.error("--commit must be an exact 40-hex SHA")
    try:
        target = safe_target(args.output)
        status = repo_state(target)
        if status == "occupied":
            p.error("Output directory already exists but is not a PurrDocs Git checkout. Select another --output.")
        if status == "missing":
            target.parent.mkdir(parents=True, exist_ok=True)
            git("clone", "--depth", "1", "--branch", args.ref, "--", SOURCE_URL, str(target))
            print("CLONED:", target)
        elif git("status", "--porcelain", "--untracked-files=all", cwd=target):
            raise RuntimeError("Local PurrDocs checkout has modified files. Restore its clean state before synchronization.")
        elif args.refresh or args.commit:
            if args.commit:
                git("fetch", "--depth", "1", "origin", args.commit, cwd=target)
            else:
                git("fetch", "--depth", "1", "origin", args.ref, cwd=target)
            git("checkout", "--detach", "FETCH_HEAD", cwd=target)
            print("REFRESHED:", target)
        else:
            print("REUSING checkout without network update (pass --refresh to fetch):", target)
        if args.commit and git("rev-parse", "HEAD", cwd=target).lower() != args.commit.lower():
            git("fetch", "--depth", "1", "origin", args.commit, cwd=target)
            git("checkout", "--detach", "FETCH_HEAD", cwd=target)
        data = snapshot_index(target, args.ref)
        if git("rev-parse", "HEAD", cwd=target) != data["git_commit"] or git("status", "--porcelain", cwd=target):
            raise RuntimeError("PurrDocs checkout changed during synchronization. Run synchronization again.")
        index = target.parent / "docs-index.json"
        # Preserve the immediately prior index so a content change cannot
        # silently invalidate the normative skill guidance.
        previous = target.parent / "docs-index.previous.json"
        prior = index.read_bytes() if index.is_file() else None
        prior_data = json.loads(prior) if prior else None
        if not prior_data or any(prior_data.get(key) != data[key] for key in ("git_commit", "files", "source_ref")):
            if prior_data and prior_data["git_commit"] != data["git_commit"]:
                write_inventory(previous, prior)
            write_inventory(index, json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
        if previous.is_file():
            print("DOC DRIFT REVIEW:", previous, "->", index)
            print("  python scripts/docs_drift.py", previous, index)
        print(f"INDEXED {data['markdown_count']} Markdown pages, commit {data['git_commit']}")
        print("INDEX:", index)
        print("NEXT: python scripts/docs_catalog.py coverage")
        return 0
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        print("ERROR:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
