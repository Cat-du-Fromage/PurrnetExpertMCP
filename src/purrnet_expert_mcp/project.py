"""Read Unity project and package metadata without running Unity or Git."""

import json
import os
import re
from collections import defaultdict
from pathlib import Path

from purrnet_common import parse_version

from .paths import plain, read_file, walk, within

CORE = "dev.purrnet.purrnet"
PREDICTION = "dev.purrnet.purrdiction"
PREFIX = "dev.purrnet."
ASSET_NAMES = {
    "PurrNet": CORE, "PurrDiction": PREDICTION, "PurrLobby": "dev.purrnet.purrlobby",
    "PurrVoice": "dev.purrnet.purrvoice", "PurrUI": "dev.purrnet.purrui",
    "PurrServices": "dev.purrnet.purrservices", "PurrLay": "dev.purrnet.purrlay",
}
SHA = re.compile(r"[0-9a-fA-F]{40}")


def project_root(project: str | Path) -> Path:
    path = Path(project).expanduser()
    if not path.is_absolute() or (os.name == "nt" and path.drive.startswith("\\\\")):
        raise ValueError("Provide an absolute local Unity project path.")
    root = path.resolve(strict=True)
    allowed = os.environ.get("PURRNET_PROJECT_ROOTS")
    if allowed and not any(
        root.is_relative_to(Path(base).expanduser().resolve())
        for base in allowed.split(os.pathsep) if base
    ):
        raise ValueError("Unity project is outside PURRNET_PROJECT_ROOTS.")
    if not all(within(root, root / name, directory=True) for name in ("Assets", "ProjectSettings", "Packages")):
        raise ValueError("Expected a Unity project with regular Assets, Packages and ProjectSettings directories.")
    return root


def package_name(value) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"dev\.purrnet\.[a-z0-9_.-]{1,100}", value))


def load_json(root, path, warnings):
    try:
        data = json.loads(read_file(root, path, 1_000_000).decode("utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        return data
    except (OSError, ValueError, RecursionError):
        warnings.append(f"Missing or invalid metadata: {path.relative_to(root)}")
        return {}


def dependencies(root, name, warnings):
    data = load_json(root, root / "Packages" / name, warnings)
    result = data.get("dependencies")
    if not isinstance(result, dict):
        if data:
            warnings.append(f"Missing or invalid dependencies: Packages/{name}")
        return {}
    return {key: value for key, value in result.items() if package_name(key)}


def exact_version(value):
    return value if isinstance(value, str) and len(value) <= 80 and parse_version(value) else None


def inventory(root, warnings):
    found = defaultdict(list)
    scans = (("Packages", "embedded", 0), ("Assets", "assets", 6), ("Library/PackageCache", "cache", 0))
    for relative, origin, depth in scans:
        directory = root / relative
        try:
            for path in walk(root, directory, depth=depth + 1, budget=35_000, exclude=frozenset({".git"})):
                if path.name != "package.json":
                    continue
                if origin != "assets" and path.parent.parent != directory:
                    continue
                if origin == "cache" and not path.parent.name.startswith(PREFIX):
                    continue
                data = load_json(root, path, warnings)
                name = data.get("name")
                if package_name(name):
                    found[name].append({
                        "path": path.parent.relative_to(root).as_posix(),
                        "metadata": path.relative_to(root).as_posix(),
                        "version": exact_version(data.get("version")),
                        "origin": origin,
                    })
        except ValueError as error:
            warnings.append(str(error))
    for folder, name in ASSET_NAMES.items():
        path = root / "Assets" / folder
        if within(root, path, directory=True) and not any(
            item["path"] == f"Assets/{folder}" for entries in found.values() for item in entries
        ):
            found[name].append({"path": f"Assets/{folder}", "metadata": None, "version": None, "origin": "assets"})
    return found


def resolve_package(name, requested, locked, candidates, warnings):
    lock = locked if isinstance(locked, dict) else {}
    lock_kind = lock.get("source")
    lock_kind = lock_kind if lock_kind in ("git", "registry", "local", "embedded", "builtin") else None
    lock_version = exact_version(lock.get("version")) if lock_kind != "git" else None
    lock_hash = lock.get("hash")
    revision = lock_hash.lower() if lock_kind == "git" and isinstance(lock_hash, str) and SHA.fullmatch(lock_hash) else None
    requested_ref = requested.rpartition("#")[2] if isinstance(requested, str) and "#" in requested else None
    requested_git = isinstance(requested, str) and (
        ".git" in requested.partition("#")[0] or requested.startswith(("git+", "git:", "ssh:"))
    )
    if requested_ref and not re.fullmatch(r"[A-Za-z0-9._/-]{1,100}", requested_ref):
        requested_ref = None
    if requested_ref and not SHA.fullmatch(requested_ref) and revision is None:
        warnings.append(f"{name}: requested Git ref has no resolved commit in the lockfile.")
    if requested_ref and SHA.fullmatch(requested_ref) and revision and requested_ref.lower() != revision:
        warnings.append(f"{name}: requested Git commit differs from the resolved lockfile commit.")
    if exact_version(requested) and lock_version and requested != lock_version:
        warnings.append(f"{name}: manifest version differs from the lockfile version.")

    embedded = [item for item in candidates if item["origin"] == "embedded"]
    cached = [item for item in candidates if item["origin"] == "cache"]
    assets = [item for item in candidates if item["origin"] == "assets"]
    if embedded:
        selected = embedded + assets
    elif lock_kind in ("local", "embedded") or (isinstance(requested, str) and requested.startswith("file:")):
        selected = assets
        warnings.append(f"{name}: local dependency paths are only inspected in supported project directories.")
    else:
        matching = [item for item in cached if item["version"] == lock_version] if lock_version else cached
        if revision:
            tagged = {
                item["path"]: suffix for item in matching
                if re.fullmatch(r"[0-9a-f]{7,40}", suffix := item["path"].rpartition("@")[2].lower())
            }
            by_revision = [item for item in matching if revision.startswith(tagged.get(item["path"], "unmatched"))]
            matching = by_revision or [item for item in matching if item["path"] not in tagged]
            if tagged and not matching:
                warnings.append(f"{name}: cached source suffixes conflict with the resolved Git revision.")
        selected = (matching if revision else matching or cached) + assets
    active = selected[0] if len(selected) == 1 else None
    version = active["version"] if active else None
    version_source = active["metadata"] if version else None
    if len(selected) > 1:
        warnings.append(f"{name}: ambiguous installed sources; inspect Unity Package Manager.")
    elif not active:
        warnings.append(f"{name}: installed C# source directory unavailable.")
        version = lock_version
        version_source = "Packages/packages-lock.json" if version else None
    elif lock_version and version and lock_version != version:
        warnings.append(f"{name}: installed version {version} conflicts with lockfile {lock_version}.")
        if active["origin"] != "embedded":
            version = version_source = None
    elif active["origin"] == "cache" and (lock_kind == "git" or requested_git) and not revision:
        warnings.append(f"{name}: the cache candidate cannot be tied to a resolved Git revision.")
        version = version_source = None
    if not version:
        warnings.append(f"{name}: installed version could not be determined.")
    if active and active["origin"] != "cache" and revision:
        warnings.append(f"{name}: the Git lockfile revision is not evidence for the {active['origin']} sources.")
    return {
        "package": name, "version": version, "version_source": version_source,
        "manifest_version": exact_version(requested), "requested_git_ref": requested_ref,
        "lock_source": lock_kind, "lock_version": lock_version, "lock_revision": revision,
        "revision_source": "Packages/packages-lock.json" if revision else None,
        "active_source": active, "source_candidates": candidates[:8],
        "csharp_source_roots": [active["path"]] if active else [],
    }


def inspect_project(project: str | Path) -> dict:
    root = project_root(project)
    warnings = []
    unity = None
    try:
        version = read_file(root, root / "ProjectSettings/ProjectVersion.txt", 16_000).decode("utf-8-sig")
        match = re.search(r"^m_EditorVersion:[ \t]*(\d[\w.]{1,40})[ \t]*$", version.replace("\r", ""), re.M)
        unity = match[1] if match else None
    except (OSError, ValueError):
        pass
    if not unity:
        warnings.append("Unity version unavailable in ProjectSettings/ProjectVersion.txt.")
    manifest = dependencies(root, "manifest.json", warnings)
    locked = dependencies(root, "packages-lock.json", warnings)
    sources = inventory(root, warnings)
    names = sorted(manifest.keys() | locked.keys() | sources.keys() | {CORE, PREDICTION})
    if len(names) > 50:
        warnings.append("Associated package list capped at 48.")
    packages = {}
    for name in [CORE, PREDICTION, *(name for name in names if name not in (CORE, PREDICTION))][:50]:
        known = name in manifest or name in locked or name in sources
        packages[name] = resolve_package(name, manifest.get(name), locked.get(name), sources.get(name, []), warnings) if known else None
        if not known:
            warnings.append(f"{name}: no manifest, lockfile or installed package evidence.")
    return {
        "project": str(root), "unity_version": unity,
        "unity_version_source": "ProjectSettings/ProjectVersion.txt" if unity else None,
        "purrnet": packages.pop(CORE), "purrdiction": packages.pop(PREDICTION),
        "associated_packages": list(packages.values()), "warnings": warnings[:40],
    }
