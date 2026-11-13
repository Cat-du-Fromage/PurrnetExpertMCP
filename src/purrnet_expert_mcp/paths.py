"""Bounded reads from a known tree, excluding links and Windows junctions."""

import os
import stat
from collections.abc import Iterator
from pathlib import Path


def plain(path: Path, *, directory: bool = False) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    return (
        not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
        and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode))
    )


def within(root: Path, path: Path, *, directory: bool = False) -> bool:
    parts = path.relative_to(root).parts
    if not parts or any(part in {".", ".."} for part in parts):
        return False
    parent = root
    for part in parts[:-1]:
        parent /= part
        if not plain(parent, directory=True):
            return False
    return plain(path, directory=directory)


def read_file(root: Path, path: Path, limit: int) -> bytes:
    if not within(root, path):
        raise OSError(f"Missing, linked, or non-regular file: {path.relative_to(root)}")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"File exceeds {limit} bytes: {path.relative_to(root)}")
    return data


def walk(
    root: Path, start: Path, *, depth: int, budget: int, exclude: frozenset[str] = frozenset(),
) -> Iterator[Path]:
    if not within(root, start, directory=True):
        return
    pending = [(start, 0)]
    while pending:
        directory, level = pending.pop()
        if not within(root, directory, directory=True):
            continue
        children = []
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    budget -= 1
                    if budget < 0:
                        raise ValueError(f"Scan limit reached in {start.relative_to(root)}")
                    children.append(entry.name)
        except OSError:
            continue
        for name in sorted(children, key=str.casefold):
            if name in exclude:
                continue
            path = directory / name
            if plain(path):
                yield path
            elif level < depth and plain(path, directory=True):
                pending.append((path, level + 1))
