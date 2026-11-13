#!/usr/bin/env python3
"""Audit every synced PurrDocs Markdown page, not just a handpicked allowlist.

A routed page is not necessarily understood or compatible. Unrouted technical
pages are candidates for adding a guide/route. Marketing/example pages are
kept searchable but not treated as required core technical references.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
ROUTES=ROOT/'references/task-routes.json'
DOCS=ROOT/'references/cache/official-docs'
TECH=('systems-and-modules/','client-side-prediction/','plug-n-play-components/','tools/','integrations/','addons/','guides/','getting-started/','game-server-hosting/','terminology/')
# High-risk pages checked for a *mandatory topical route* when docs are synced.
# This is NOT the complete official documentation; all other files remain in the inventory.
CRITICAL_DOCS = (
    'client-side-prediction/best-practices.md',
    'client-side-prediction/input-handling.md',
    'client-side-prediction/state-handling.md',
    'client-side-prediction/security.md',
    'client-side-prediction/predicted-visibility.md',
    'client-side-prediction/multi-identity-interactions.md',
    'client-side-prediction/predicted-hierarchy.md',
    'client-side-prediction/built-in-components/predicted-identity-spawner.md',
    'client-side-prediction/built-in-components/predicted-physics-callbacks.md',
    'client-side-prediction/disposable-collections.md',
    'systems-and-modules/network-identity/spawning-and-despawning/client-spawning-validation.md',
    'systems-and-modules/network-identity/dont-destroy-on-load.md',
    'systems-and-modules/network-identity/playeridentity.md',
    'systems-and-modules/network-modules/sync-types/synclazyref.md',
    'systems-and-modules/network-manager/network-visibility/README.md',
    'systems-and-modules/network-manager/scene-scoped-prefabs-and-assets.md',
    'systems-and-modules/collider-rollback.md',
    'systems-and-modules/network-modules/syncbigdata/README.md',
    'systems-and-modules/code-stripping.md',
    'systems-and-modules/bitpacker-serialization/async-serialization-packing.md',
    'systems-and-modules/transports/simulating-latency.md',
    'plug-n-play-components/network-transform/adaptive-sync.md',
)

NONTECH=('made-with-purrnet/','full-game-guides/','community-guides/','readme/','introduction/')

def classify(files,rules):
    routed={p for r in rules for p in r['docs']}
    entries=[]
    for path in sorted(files):
        if path in routed:status='mandatory-on-routed-task'
        elif path.startswith(TECH):status='technical-searchable-not-mandatory'
        elif path.startswith(NONTECH):status='examples-or-background-searchable'
        else:status='general-searchable'
        entries.append({'page':path,'status':status,'explicitly_routed':path in routed})
    listed={x['page'] for x in entries}
    missing=sorted(routed-listed)
    critical_unrouted=sorted(set(CRITICAL_DOCS)&listed-routed)
    return {'total':len(entries),'routed':sum(e['explicitly_routed'] for e in entries),
            'unrouted_technical':[e['page'] for e in entries if e['status']=='technical-searchable-not-mandatory'],
            'missing_routed_pages':missing,'critical_unrouted':critical_unrouted,'entries':entries}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--docs',type=Path,default=DOCS)
    p.add_argument('--json-out',type=Path)
    p.add_argument('--fail-missing-routed',action='store_true')
    p.add_argument('--fail-unrouted-technical',action='store_true')
    p.add_argument('--fail-unrouted-critical',action='store_true')
    a=p.parse_args();docs=a.docs.resolve()
    if not docs.is_dir() or not (docs/'SUMMARY.md').is_file():
        print('Official PurrDocs not synchronized; use sync_sources.py. No total coverage claim.',file=sys.stderr);return 2
    files={x.relative_to(docs).as_posix() for x in docs.rglob('*.md') if x.is_file() and '.git' not in x.parts}
    rules=json.loads(ROUTES.read_text(encoding='utf8'))['rules']
    report=classify(files,rules)
    if a.json_out:
        a.json_out.parent.mkdir(parents=True,exist_ok=True)
        a.json_out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f"PurrDocs {report['total']} pages; {report['routed']} required on a route; {len(report['unrouted_technical'])} technical pages searchable but not forced; {len(report['missing_routed_pages'])} expected routed docs missing; {len(report['critical_unrouted'])} critical pages not mandatory")
    for q in report['missing_routed_pages'][:20]:print('MISSING',q)
    for q in report['unrouted_technical'][:15]:print('UNROUTED TECH',q)
    for q in report['critical_unrouted']:print('CRITICAL UNROUTED',q)
    print('Interpretation: mapped != audited, missing != absent from upstream. Review important un-routed technical pages.')
    if a.fail_missing_routed and report['missing_routed_pages']:return 3
    if a.fail_unrouted_critical and report['critical_unrouted']:return 5
    if a.fail_unrouted_technical and report['unrouted_technical']:return 4
    return 0
if __name__=='__main__':raise SystemExit(main())
