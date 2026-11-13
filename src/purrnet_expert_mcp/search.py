"""Rank commit-pinned documentation passages and retrieve exact references."""

import json
import re
from pathlib import Path
from urllib.parse import quote

from purrnet_common import parse_version, satisfies

from .indexer import cache_state, markdown_path, read_index

WORDS = re.compile(r"[^\W_]+", re.UNICODE)
STOP = frozenset("a an and are can do does for how in is of on the to what when with à au avec comment de des du en est et la le les pour qui un une".split())


def document_compatibility(product: str, conditions: list[str], context: dict | None) -> dict:
    package = (context or {}).get(product) or {}
    version = parse_version(package.get("version"))
    checks = [{"range": gate, "matches": satisfies(version, gate)} for gate in conditions]
    if any(check["matches"] is False for check in checks):
        status = "verified_incompatible"
    elif not conditions:
        status = "requires_source_inspection"
    elif any(check["matches"] is None for check in checks):
        status = "unknown"
    else:
        status = "verified_compatible"
    return {
        "status": status, "scope": "documented_version_conditions", "product": product,
        "version": package.get("version"), "version_source": package.get("version_source"),
        "conditions": checks,
    }


def evidence(row, commit: str, context: dict | None, excerpt: str) -> dict:
    path = row["path"]
    start, end = row["line_start"], row["line_end"]
    product = row["product"]
    conditions = json.loads(row["conditions"])
    return {
        "path": path, "title": row["title"], "section": row["section"], "product": product,
        "line_start": start, "line_end": end, "reference": f"{path}:{start}",
        "source": "official_purrdocs", "commit": commit, "sha256": row["sha256"],
        "url": f"https://github.com/PurrNet/PurrDocs/blob/{commit}/{quote(path)}#L{start}-L{end}",
        "excerpt": excerpt, "version_conditions": conditions,
        "compatibility": document_compatibility(product, conditions, context) if context else None,
    }


def search_docs(docs: Path, query: str, product: str, limit: int, context: dict | None) -> dict:
    terms = WORDS.findall(query)[:20]
    if not terms:
        raise ValueError("Search requires at least one letter or digit.")
    preferred = [term for term in terms if term.casefold() not in STOP] or terms
    exact = '"' + " ".join(terms) + '"'
    fallback = " OR ".join(f'"{word}"' for word in dict.fromkeys(preferred))
    with read_index(docs) as (connection, metadata):
        rows = {}
        for match in dict.fromkeys((exact, fallback)):
            if len(rows) >= limit:
                break
            candidates = connection.execute("""
                SELECT p.*, snippet(fulltext, 3, '', '', ' … ', 36) AS excerpt
                FROM fulltext JOIN passages p ON p.id = fulltext.rowid
                WHERE fulltext MATCH ? AND (? = 'all' OR p.product = ?)
                ORDER BY bm25(fulltext, 4.0, 5.0, 3.0, 1.0), p.id LIMIT ?
            """, (match, product, product, limit))
            for row in candidates:
                rows.setdefault(row["id"], row)
                if len(rows) >= limit:
                    break
        commit = metadata["commit_sha"]
        return {
            "status": "ok", "cache_status": cache_state(docs, metadata), "commit": commit,
            "results": [evidence(row, commit, context, row["excerpt"][:550]) for row in rows.values()],
        }


def lookup_document(docs: Path, reference: str, context: dict) -> dict:
    match = re.fullmatch(r"(.+\.md)(?::([1-9]\d{0,6}))?", reference)
    if not match:
        raise ValueError("Use a PurrDocs path ending in .md, optionally followed by :line.")
    path, line = markdown_path(match[1]).as_posix(), int(match[2]) if match[2] else None
    with read_index(docs) as (connection, metadata):
        commit = metadata["commit_sha"]
        base = {"reference": reference, "commit": commit, "cache_status": cache_state(docs, metadata)}
        if line is not None:
            rows = connection.execute(
                "SELECT * FROM passages WHERE path = ? AND line_start <= ? AND line_end >= ?",
                (path, line, line),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM passages WHERE path = ? ORDER BY line_start LIMIT 101", (path,),
            ).fetchall()
        if not rows:
            return {**base, "status": "unknown", "reason": "No indexed passage covers this reference."}
        if line is not None:
            row = rows[0]
            item = evidence(row, commit, context, row["body"])
            return {**base, **item["compatibility"], "evidence": item}
        scopes = {}
        for row in rows:
            gates = row["conditions"]
            if gates not in scopes:
                item = evidence(row, commit, context, row["body"][:350])
                scopes[gates] = item
        if len(scopes) > 1 or len(rows) > 100:
            return {
                **base, "status": "requires_source_inspection",
                "reason": "The page has different version scopes or exceeds the page inspection limit. Pass path.md:line.",
                "scopes": list(scopes.values())[:8],
            }
        item = next(iter(scopes.values()))
        return {**base, **item["compatibility"], "evidence": item}
