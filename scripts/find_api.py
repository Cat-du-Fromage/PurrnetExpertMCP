#!/usr/bin/env python3
"""Find literal symbols in the resolved PurrNet, PurrDiction and addon Unity C# sources."""
import argparse
from pathlib import Path
import sys

ASSETS = ['PurrNet', 'PurrDiction', 'PurrLobby', 'PurrUI', 'PurrServices', 'PurrLay']


def roots(project: Path):
    candidates = [project / 'Assets' / name for name in ASSETS]
    pkg = project / 'Packages'
    if pkg.is_dir():
        candidates.extend(x for x in pkg.iterdir() if x.is_dir() and x.name.startswith('dev.purrnet.'))
    cache = project / 'Library' / 'PackageCache'
    if cache.is_dir():
        candidates.extend(x for x in cache.iterdir() if x.is_dir() and x.name.startswith('dev.purrnet.'))
    unique = set()
    for folder in candidates:
        if folder.is_dir() and folder.resolve() not in unique:
            unique.add(folder.resolve())
            yield folder


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('project', type=Path)
    p.add_argument('symbol')
    p.add_argument('--limit', type=int, default=80)
    args = p.parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir(): p.error('Unity project not found')
    if not args.symbol.strip(): p.error('Empty symbol')
    if not 1 <= args.limit <= 1000: p.error('Limit must be 1..1000')
    matched = 0
    folders = list(roots(project))
    if not folders:
        print('No installed PurrNet/PurrDiction C# package found. Resolve Unity packages.', file=sys.stderr)
        return 2
    checked = set()
    for root in folders:
        for file in sorted(root.rglob('*.cs')):
            if file in checked: continue
            checked.add(file)
            try:
                if file.stat().st_size > 2_000_000: continue
                for n, line in enumerate(file.read_text(encoding='utf-8-sig', errors='replace').splitlines(), 1):
                    if args.symbol in line:
                        print(f'{file.relative_to(project)}:{n}: {line.strip()[:250]}')
                        matched += 1
                        if matched >= args.limit:
                            print(f'Limit reached ({args.limit}).')
                            return 0
            except OSError:
                continue
    print(f'{matched} occurrence(s); packages searched: {len(folders)}')
    return 0 if matched else 1


if __name__ == '__main__':
    raise SystemExit(main())
