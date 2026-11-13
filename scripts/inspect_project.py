#!/usr/bin/env python3
"""Inspect Unity version + all installed PurrNet family packages (source refs, hashes, local paths).

Purely observational, Python standard library, no network and no modifications.
"""
import argparse
import json
from pathlib import Path
import sys

PREFIX = "dev.purrnet."
KNOWN_ASSETS = {"PurrNet": "dev.purrnet.purrnet", "PurrDiction": "dev.purrnet.purrdiction"}


def read_json(path, warnings):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        warnings.append(f"Cannot read {path}: {exc}")
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        parser.error("Unity project directory not found")
    warnings = []
    manifest = read_json(project / "Packages" / "manifest.json", warnings) or {}
    lock = read_json(project / "Packages" / "packages-lock.json", warnings) or {}
    deps = manifest.get('dependencies', {})
    locked = lock.get('dependencies', {})
    if not isinstance(deps, dict): deps = {}
    if not isinstance(locked, dict): locked = {}

    unity = None
    verfile = project / "ProjectSettings" / "ProjectVersion.txt"
    if verfile.is_file():
        for line in verfile.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            if line.startswith('m_EditorVersion:'):
                unity = line.partition(':')[2].strip()
                break

    locations = []
    embedded = project / "Packages"
    if embedded.is_dir():
        locations.extend(embedded.glob("*/package.json"))
    cache = project / "Library" / "PackageCache"
    if cache.is_dir():
        locations.extend(cache.glob("*/package.json"))
    for folder in KNOWN_ASSETS:
        locations.append(project / 'Assets' / folder / 'package.json')
    # Additional packages nested in Assets, but limit scan to first three levels.
    if (project / 'Assets').is_dir():
        locations.extend((project / 'Assets').glob('*/package.json'))

    found = {}
    for path in sorted(set(locations)):
        if not path.is_file():
            continue
        obj = read_json(path, warnings)
        if isinstance(obj, dict) and obj.get('name', '').startswith(PREFIX):
            key = obj['name']
            found.setdefault(key, []).append({
                'path': str(path.relative_to(project)),
                'version': obj.get('version'),
                'unity_minimum': obj.get('unity'),
            })
    names = sorted(set(k for k in deps if k.startswith(PREFIX)) |
                   set(k for k in locked if k.startswith(PREFIX)) | set(found))
    packages = []
    for key in names:
        spec = deps.get(key)
        lockinfo = locked.get(key) or {}
        if not isinstance(lockinfo, dict): lockinfo = {}
        branch = spec.split('#', 1)[1] if isinstance(spec, str) and '#' in spec else None
        if isinstance(spec, str) and branch and branch in ('release', 'dev', 'main'):
            warnings.append(f"Moving branch for {key}: {branch}; inspect the lockfile hash.")
        if not found.get(key):
            warnings.append(f"Source for {key} not found in common local locations; API cannot be proven yet.")
        packages.append({
            'name': key,
            'manifest_spec': spec,
            'requested_git_ref': branch,
            'lock_version': lockinfo.get('version'),
            'lock_source': lockinfo.get('source'),
            'lock_hash': lockinfo.get('hash'),
            'local_packages': found.get(key, []),
        })
    if not packages:
        warnings.append('No dev.purrnet.* package found in manifest, lock or installed sources.')
    has_prediction = any(p['name'] == 'dev.purrnet.purrdiction' for p in packages)
    print(json.dumps({
        'project': str(project),
        'unity_version': unity,
        'packages': packages,
        'purrdiction_detected': has_prediction,
        'purrnet_core_detected': any(p['name'] == 'dev.purrnet.purrnet' for p in packages),
        'warnings': warnings,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
