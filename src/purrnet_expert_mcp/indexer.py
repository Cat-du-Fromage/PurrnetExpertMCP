"""Build a commit-pinned FTS5 index from the skill's PurrDocs inventory."""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing, contextmanager
from pathlib import Path, PurePosixPath

from purrnet_common import SOURCE_URL, docs_checkout

from .paths import plain, read_file

SCHEMA = 1
INVENTORY_LIMIT = 3_000_000
PAGE_LIMIT = 5_000_000
MAX_PASSAGE = 3500
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
OPEN_GATE = re.compile(r"""^\s*{%\s*version\s+range\s*=\s*(['"])([^'"]+)\1\s*%}\s*$""")
CLOSE_GATE = re.compile(r"^\s*{%\s*endversion\s*%}\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class CacheError(ValueError):
    pass


def database(docs: Path) -> Path:
    return docs.parent / "purrdocs.sqlite3"


def inventory_bytes(docs: Path) -> bytes:
    return read_file(docs.parent, docs.parent / "docs-index.json", INVENTORY_LIMIT)


def inventory(docs: Path) -> tuple[dict, str]:
    raw = inventory_bytes(docs)
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get("source_repository") != SOURCE_URL:
        raise CacheError("Expected the official PurrDocs inventory from scripts/sync_sources.py.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("git_commit"))) or not isinstance(data.get("files"), list):
        raise CacheError("Invalid PurrDocs commit or file inventory.")
    return data, hashlib.sha256(raw).hexdigest()


def markdown_path(relative: str) -> PurePosixPath:
    if not isinstance(relative, str) or len(relative) > 500 or any(char in relative for char in "\\:\x00"):
        raise CacheError("Use a Markdown path relative to the PurrDocs checkout.")
    parts = relative.split("/")
    path = PurePosixPath(relative)
    if any(part in {"", ".", "..", ".git"} for part in parts) or path.suffix.lower() != ".md":
        raise CacheError("Use a Markdown path relative to the PurrDocs checkout.")
    return path


def passages(markdown: str, default_title: str):
    lines = markdown.splitlines()
    title = default_title
    stack = []
    gates = []
    first_line = 1
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:100], 1):
            if line.strip() == "---":
                first_line = index + 2
                break
        if first_line > 1:
            for line in lines[1:first_line - 2]:
                if match := re.fullmatch(r"""version:\s*(.*?)\s*""", line):
                    gates.append(match[1].strip().strip("'\""))

    page_gates = len(gates)
    fence = ""
    buffer = []
    start = first_line
    length = 0
    found_title = False

    def result(end):
        if buffer and (body := "\n".join(buffer).strip()):
            return title, " / ".join(name for _, name in stack)[:500], start, end, body, list(gates)
        return None

    for number, line in enumerate(lines[first_line - 1:], first_line):
        heading = HEADING.match(line) if not fence else None
        opening = OPEN_GATE.match(line) if not fence else None
        closing_gate = not fence and CLOSE_GATE.match(line)
        marker = opening or closing_gate
        if heading or marker or length + len(line) > MAX_PASSAGE:
            if row := result(number - 1):
                yield row
            buffer = []
            start = number
            length = 0
        if heading:
            level, name = len(heading[1]), heading[2][:250]
            if level == 1 and not found_title:
                title = name
                found_title = True
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, name))
        if marker:
            if opening:
                gates.append(opening[2][:250])
            elif len(gates) > page_gates:
                gates.pop()
            start = number + 1
            continue
        if match := FENCE.match(line):
            ticks = match[1]
            if not fence:
                fence = ticks
            elif ticks[0] == fence[0] and len(ticks) >= len(fence) and not match[2].strip():
                fence = ""
        if not buffer and not line.strip():
            start = number + 1
            continue
        buffer.append(line[:MAX_PASSAGE])
        length += len(buffer[-1]) + 1
    if row := result(len(lines)):
        yield row


def build(docs: Path) -> dict:
    docs = docs.resolve(strict=True)
    data, fingerprint = inventory(docs)
    commit = data["git_commit"]
    if len(data["files"]) > 5000:
        raise CacheError("PurrDocs inventory exceeds 5000 entries.")
    descriptor, temporary = tempfile.mkstemp(prefix=".purrdocs-", suffix=".sqlite3", dir=docs.parent)
    os.close(descriptor)
    temp = Path(temporary)
    pages = rows = total_bytes = 0
    try:
        with closing(sqlite3.connect(temp)) as connection, connection:
            connection.executescript("""
                CREATE TABLE metadata (schema INTEGER, commit_sha TEXT, inventory_sha TEXT, pages INTEGER, passages INTEGER);
                CREATE TABLE passages (
                    id INTEGER PRIMARY KEY, path TEXT, title TEXT, section TEXT,
                    line_start INTEGER, line_end INTEGER, body TEXT, conditions TEXT, product TEXT, sha256 TEXT
                );
                CREATE INDEX passage_path ON passages(path, line_start);
                CREATE VIRTUAL TABLE fulltext USING fts5(
                    path, title, section, body, content='passages', content_rowid='id',
                    tokenize='unicode61 remove_diacritics 2'
                );
            """)
            seen = set()
            for entry in data["files"]:
                if not isinstance(entry, dict):
                    raise CacheError("Invalid entry in PurrDocs inventory.")
                relative = markdown_path(entry.get("path"))
                if relative in seen:
                    raise CacheError(f"Duplicate PurrDocs inventory entry: {relative}")
                seen.add(relative)
                if entry.get("skipped") == "size_limit":
                    continue
                raw = read_file(docs, docs.joinpath(*relative.parts), PAGE_LIMIT)
                total_bytes += len(raw)
                if total_bytes > 30_000_000:
                    raise CacheError("PurrDocs checkout exceeds 30 MB of Markdown.")
                checksum = hashlib.sha256(raw).hexdigest()
                if checksum != entry.get("sha256"):
                    raise CacheError(f"Inventory hash mismatch: {relative}. Synchronize the checkout again.")
                if relative.name in {"SUMMARY.md", "LICENSE.md"}:
                    continue
                product = "purrdiction" if relative.parts[0] == "client-side-prediction" else "purrnet"
                for title, section, start, end, body, gates in passages(raw.decode("utf-8-sig"), relative.stem):
                    connection.execute(
                        "INSERT INTO passages VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (relative.as_posix(), title, section, start, end, body, json.dumps(gates), product, checksum),
                    )
                    rows += 1
                pages += 1
            connection.execute("INSERT INTO fulltext(fulltext) VALUES ('rebuild')")
            connection.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?)", (SCHEMA, commit, fingerprint, pages, rows))
        if hashlib.sha256(inventory_bytes(docs)).hexdigest() != fingerprint:
            raise CacheError("PurrDocs inventory changed during indexing. Run index again.")
        temp.replace(database(docs))
    finally:
        temp.unlink(missing_ok=True)
    return {"status": "ready", "commit": commit, "pages": pages, "passages": rows}


@contextmanager
def read_index(docs: Path):
    path = database(docs)
    try:
        if not plain(path):
            raise sqlite3.OperationalError("Index is missing or not a regular file")
        with closing(sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)) as connection:
            connection.row_factory = sqlite3.Row
            metadata = connection.execute("SELECT * FROM metadata").fetchone()
            if not metadata or metadata["schema"] != SCHEMA:
                raise CacheError("Unsupported cache schema. Run purrnet-expert-cache index.")
            yield connection, metadata
    except sqlite3.Error as error:
        raise CacheError("PurrDocs cache absent or unreadable. Run scripts/sync_sources.py, then purrnet-expert-cache index.") from error


def cache_state(docs: Path, metadata) -> str:
    if not plain(docs, directory=True):
        return "snapshot_only"
    try:
        fingerprint = hashlib.sha256(inventory_bytes(docs)).hexdigest()
    except (OSError, ValueError):
        return "snapshot_only"
    return "ready" if fingerprint == metadata["inventory_sha"] else "stale"


def diagnose(docs: Path, verify: bool = False) -> dict:
    try:
        with read_index(docs) as (_, metadata):
            result = {"status": cache_state(docs, metadata), **dict(metadata)}
    except CacheError as error:
        result = {"status": "missing" if not database(docs).is_file() else "invalid", "message": str(error)}
    result["database"] = str(database(docs))
    result["checkout"] = str(docs)
    try:
        data, _ = inventory(docs)
        result["checkout_inventory_commit"] = data["git_commit"]
        if verify:
            total_bytes = 0
            if len(data["files"]) > 5000:
                raise CacheError("PurrDocs inventory exceeds 5000 entries.")
            for entry in data["files"]:
                if not isinstance(entry, dict):
                    raise CacheError("Invalid entry in PurrDocs inventory.")
                if entry.get("skipped"):
                    continue
                relative = markdown_path(entry["path"])
                raw = read_file(docs, docs.joinpath(*relative.parts), PAGE_LIMIT)
                total_bytes += len(raw)
                if total_bytes > 30_000_000:
                    raise CacheError("PurrDocs checkout exceeds 30 MB of Markdown.")
                if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
                    raise CacheError(f"Inventory hash mismatch: {relative}")
            result["checkout_hashes_verified"] = True
    except (OSError, ValueError, KeyError, TypeError) as error:
        result["checkout_error"] = str(error)
        if result["status"] == "ready":
            result["status"] = "stale"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, default=docs_checkout(), help="PurrDocs checkout with adjacent docs-index.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("index", help="Rebuild locally from the synchronized inventory")
    diagnostic = commands.add_parser("status", help="Diagnose the cache without using the network")
    diagnostic.add_argument("--verify", action="store_true", help="Verify current checkout file hashes")
    args = parser.parse_args()
    try:
        docs = args.docs.expanduser().resolve()
        result = build(docs) if args.command == "index" else diagnose(docs, args.verify)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"Cache error: {error}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
