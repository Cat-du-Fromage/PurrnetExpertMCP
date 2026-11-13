#!/usr/bin/env python3
"""Audit the portable Agent Skill against Anthropic authoring recommendations.

Static structure checks only. This script cannot establish spontaneous agent activation,
model quality, Unity compilation or the correctness of installed PurrNet APIs.
Uses Python standard library, no network, no writes unless --json-out specified.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
MD_LINK = re.compile(r'\[[^\]]+\]\((references/[A-Za-z0-9_./-]+\.md)(?:#[^)]*)?\)')


def audit(root: Path) -> dict:
    errors, warnings = [], []
    path = root / 'SKILL.md'
    if not path.is_file():
        return {'errors': ['SKILL.md absent'], 'warnings': [], 'checks': {}}
    data = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', data, re.S)
    if not match:
        return {'errors': ['frontmatter YAML absent ou mal formé'], 'warnings': [], 'checks': {}}
    fm, body = match.group(1), data[match.end():]
    n = re.search(r'^name:\s*([\w-]+)\s*$', fm, re.M)
    d = re.search(r'^description:\s*(.+)\s*$', fm, re.M)
    name = n.group(1) if n else ''
    if not name or len(name) > 64 or not NAME.fullmatch(name):
        errors.append('Nom Agent Skills non conforme (minuscules/tirets, 64 caractères max)')
    desc = ''
    if d:
        raw = d.group(1).strip()
        try:
            desc = json.loads(raw) if raw.startswith('"') else raw.strip("'")
        except json.JSONDecodeError:
            errors.append('description YAML double-quoted invalide')
    if not desc or len(desc) > 1024:
        errors.append('description absente ou trop longue (maximum 1024 caractères)')
    if re.search(r'(?i)\b(?:I can|you can|je peux|tu peux|vous pouvez)\b', desc):
        errors.append('description non rédigée à la troisième personne')
    if not re.search(r'\b(?:Use when|Used when|Triggered by|Use for)\b', desc):
        warnings.append('description : déclencheurs/conditions d’usage peu explicites')
    if not any(term in desc.lower() for term in ('purrnet', 'purrdiction', 'networktransform')):
        errors.append('description sans signal technique PurrNet/PurrDiction')
    if len(body.splitlines()) >= 500:
        errors.append('SKILL.md atteint >=500 lignes : subdiviser')

    links = sorted(set(MD_LINK.findall(body)))
    for p in links:
        if not (root / p).is_file():
            errors.append(f'Lien direct SKILL.md cassé : {p}')
    expected = ('references/purrdiction-best-practices.md', 'references/workflows/feature.md',
                'references/workflows/bug.md', 'references/workflows/dedicated.md',
                'references/core/spawn-security-and-persistence.md',
                'references/prediction/mirror-and-visibility.md',
                'references/anthropic-skill-authoring.md')
    for p in expected:
        if p not in links:
            errors.append(f'Guide critique non directement lié depuis SKILL.md : {p}')

    long_refs = []
    for f in (root / 'references').rglob('*.md'):
        lines = f.read_text(encoding='utf-8').splitlines()
        if len(lines) > 100:
            long_refs.append(f.relative_to(root).as_posix())
            if not any('Table des matières' in ln or 'Contents' in ln or 'Sommaire' in ln for ln in lines[:24]):
                warnings.append(f'Référence >100 lignes sans sommaire : {f.relative_to(root)}')
    route = root / 'references/task-routes.json'
    if not route.exists():
        errors.append('Fichier de routage absent')
    else:
        try:
            rules = json.loads(route.read_text(encoding='utf-8'))['rules']
            routed = {path for rule in rules for path in rule['guides']}
            for p in ('core/spawn-security-and-persistence.md', 'core/player-identity-and-lazy-refs.md',
                      'core/visibility-priority.md', 'core/collider-rollback-classic.md',
                      'prediction/mirror-and-visibility.md', 'prediction/one-shot-input-and-events.md'):
                if p not in routed:
                    errors.append('Guide v0.9 non routé : ' + p)
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'Routes invalides: {exc}')

    # Make visibility of a non-performed agent evaluation part of static audit output.
    warnings.append('Non vérifié : activation spontanée Haiku/Sonnet/Opus, compilation Unity et tests E2E')
    return {'errors': errors, 'warnings': warnings,
            'checks': {'skill_lines': len(body.splitlines()), 'description_chars': len(desc),
                       'direct_reference_links': len(links), 'long_references': long_refs}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--json-out', type=Path)
    args = ap.parse_args()
    report = audit(args.root)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report['errors'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
