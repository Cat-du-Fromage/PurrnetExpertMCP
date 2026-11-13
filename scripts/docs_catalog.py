#!/usr/bin/env python3
"""Search/validate ALL Markdown in the local complete PurrDocs clone (no network).

Examples:
  python scripts/docs_catalog.py coverage
  python scripts/docs_catalog.py list --section client-side-prediction
  python scripts/docs_catalog.py search 'SanitizeInput' --section client-side-prediction
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

from purrnet_common import docs_checkout

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = docs_checkout(ROOT)
INDEX = DEFAULT.parent / "docs-index.json"
CRITICAL = [
    "SUMMARY.md", "README.md",
    "client-side-prediction/README.md",
    "client-side-prediction/best-practices.md",
    "client-side-prediction/input-handling.md",
    "client-side-prediction/state-handling.md",
    "client-side-prediction/flow.md",
    "client-side-prediction/security.md",
    "client-side-prediction/prediction-policies.md",
    "client-side-prediction/views-and-interpolation.md",
    "client-side-prediction/predicted-hierarchy.md",
    "client-side-prediction/predicted-object-references.md",
    "client-side-prediction/disposable-collections.md",
    "client-side-prediction/deterministic-identity.md",
    "client-side-prediction/predicted-modules/README.md",
    "client-side-prediction/built-in-components/predicted-identity-spawner.md",
    "client-side-prediction/built-in-components/predicted-physics-callbacks.md",
    "client-side-prediction/lag-compensation.md",
    "systems-and-modules/network-modules/common-pitfalls.md",
    "systems-and-modules/network-modules/sync-types/syncvar.md",
    "systems-and-modules/network-manager/network-rules.md",
    "systems-and-modules/network-identity/spawning-and-despawning/README.md",
    "systems-and-modules/network-manager/authentication.md",
    "systems-and-modules/network-manager/connection-and-player-events.md",
    "systems-and-modules/network-manager/network-visibility/README.md",
    "systems-and-modules/network-manager/network-visibility/visibility-rules.md",
    "systems-and-modules/network-modules/owner-only.md",
    "systems-and-modules/network-modules/sync-types/syncinput.md",
    "systems-and-modules/network-modules/sync-types/validated-syncvar.md",
    "systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types.md",
    "systems-and-modules/broadcast.md",
    "systems-and-modules/scene-module.md",
    "systems-and-modules/addressables/README.md",
    "client-side-prediction/built-in-components/predicted-parent.md",
    "client-side-prediction/built-in-components/predicted-projectile-3d.md",
    "client-side-prediction/built-in-components/predicted-rigidbody-2d-and-3d.md",
    "client-side-prediction/predicted-visibility.md",
    "client-side-prediction/multi-identity-interactions.md",
    "client-side-prediction/predicted-state-machine/README.md",
    "systems-and-modules/remote-procedure-call-rpc/README.md",
    "plug-n-play-components/network-transform.md",
    "plug-n-play-components/network-transform/adaptive-sync.md",
    "plug-n-play-components/network-rigidbody.md",
    "plug-n-play-components/network-rigidbody-2d.md",
    "plug-n-play-components/network-animator.md",
    "plug-n-play-components/network-audio-source.md",
    "plug-n-play-components/network-bones.md",
    "plug-n-play-components/network-ownership-toggle.md",
    "plug-n-play-components/network-reflection-auto-sync.md",
    "plug-n-play-components/state-machine-auto-networked.md",
    "systems-and-modules/network-manager/network-assets.md",
    "systems-and-modules/network-manager/network-prefabs.md",
    "systems-and-modules/network-manager/scene-scoped-prefabs-and-assets.md",
    "systems-and-modules/addressables/addressable-spawning-and-despawning.md",
    "systems-and-modules/addressables/addressable-scene-handling.md",
    "systems-and-modules/code-stripping.md",
    "systems-and-modules/bitpacker-serialization/async-serialization-packing.md",
    "systems-and-modules/network-modules/syncbigdata/README.md",
 "systems-and-modules/network-modules/syncbigdata/synctexturefile.md",
 "tools/type-hash-resolver.md",

]


def md_files(docs: Path) -> list[Path]:
    return sorted(p for p in docs.rglob('*.md') if '.git' not in p.relative_to(docs).parts and p.is_file() and not p.is_symlink())


def summary_refs(md: str) -> set[str]:
    # Relative links in GitBook SUMMARY.md; ignore HTTP, anchors, data files.
    result = set()
    for ref in re.findall(r'\]\(([^)]+)\)', md):
        target = ref.split('#')[0].split('?')[0].replace('%20', ' ')
        if target.lower().endswith('.md') and not target.startswith(('http:', 'https:', '../', '/')):
            result.add(target.removeprefix('./'))
    return result


def read_index(index: Path):
    try:
        return json.loads(index.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def coverage(docs: Path, index: Path) -> int:
    files = md_files(docs)
    rel = {p.relative_to(docs).as_posix() for p in files}
    missing = sorted(set(CRITICAL) - rel)
    summary = docs / 'SUMMARY.md'
    referenced = summary_refs(summary.read_text(encoding='utf-8', errors='replace')) if summary.is_file() else set()
    missing_summary = sorted(referenced - rel)
    counts = Counter(p.relative_to(docs).parts[0] for p in files)
    snapshot = read_index(index)
    missing_index = snapshot is None
    stale_index = bool(snapshot and set(f['path'] for f in snapshot.get('files', [])) != rel)
    wrong_hashes = []
    if snapshot:
        indexed = {item['path']: item.get('sha256') for item in snapshot.get('files', [])}
        for f in files:
            key = f.relative_to(docs).as_posix()
            if indexed.get(key) and hashlib.sha256(f.read_bytes()).hexdigest() != indexed[key]:
                wrong_hashes.append(key)
    print('Documentation directory:', docs)
    print('Total Markdown files:', len(files))
    print('Markdown entries in SUMMARY.md:', len(referenced))
    print('Breakdown:', json.dumps(dict(sorted(counts.items())), ensure_ascii=False))
    print('Missing critical docs:', missing or 'none')
    print('Missing SUMMARY.md targets:', missing_summary or 'none')
    print('Index present:', bool(snapshot), '; index mismatch:', stale_index)
    print('Files whose hash changed after index:', wrong_hashes or 'none')
    if snapshot:
        print('Index git commit:', snapshot.get('git_commit', '?'))
        print('Indexed files:', snapshot.get('markdown_count', '?'))
    # Hard quality gate: all linked pages must exist and required docs must exist
    return 1 if missing or missing_summary or missing_index or stale_index or wrong_hashes else 0


def search(docs: Path, term: str, section: str, maxhits: int):
    matches = 0
    term_lower = term.casefold()
    for p in md_files(docs):
        rel = p.relative_to(docs).as_posix()
        if section and not rel.startswith(section.rstrip('/') + '/') and rel != section:
            continue
        try:
            content = p.read_text(encoding='utf-8-sig', errors='replace')
        except OSError:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            if term_lower in line.casefold() or (i == 1 and term_lower in rel.casefold()):
                snippet = line.strip().replace('|', '\\|')[:250]
                print(f"{rel}:{i}: {snippet}")
                matches += 1
                if matches >= maxhits:
                    print(f'(limited to {maxhits} matches)')
                    return 0
    print(f'{matches} match(es).')
    return 0 if matches else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--docs', type=Path, default=DEFAULT, help='Local PurrDocs clone')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('coverage')
    l = sub.add_parser('list')
    l.add_argument('--section', default='')
    s = sub.add_parser('search')
    s.add_argument('term')
    s.add_argument('--section', default='')
    s.add_argument('--limit', type=int, default=50)
    args = p.parse_args()
    docs = args.docs.expanduser().resolve()
    if not docs.is_dir() or not (docs / 'SUMMARY.md').is_file():
        print('FULL DOCUMENTATION NOT SYNCED. Run: python scripts/sync_sources.py', file=sys.stderr)
        return 2
    if args.cmd == 'coverage':
        index = (docs.parent / 'docs-index.json')
        return coverage(docs, index)
    if args.cmd == 'list':
        for path in md_files(docs):
            rel = path.relative_to(docs).as_posix()
            if not args.section or rel.startswith(args.section.rstrip('/') + '/'):
                print(rel)
        return 0
    if not args.term.strip() or not (1 <= args.limit <= 1000):
        p.error('Search term must be non-empty, limit 1..1000')
    return search(docs, args.term, args.section, args.limit)


if __name__ == '__main__':
    raise SystemExit(main())
