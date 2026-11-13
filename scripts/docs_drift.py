#!/usr/bin/env python3
"""Compare two full PurrDocs index snapshots and flag affected skill guides.

Only says the source has changed. A human/agent must review semantics and APIs
against installed packages. It does not auto-edit the normative rules.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
ROUTES=ROOT/'references/task-routes.json'

def drift(before,after,routes=None):
    old={x['path']:x.get('sha256') for x in before.get('files',[])}
    new={x['path']:x.get('sha256') for x in after.get('files',[])}
    added=sorted(set(new)-set(old));removed=sorted(set(old)-set(new))
    changed=sorted(x for x in new.keys()&old.keys() if new[x]!=old[x])
    affected=set(added+removed+changed)
    if routes is None:routes=json.loads(ROUTES.read_text(encoding='utf8'))['rules']
    guide_impacts={}
    for route in routes:
        touched=sorted(affected & set(route['docs']))
        if touched:
            for guide in route['guides']:
                guide_impacts.setdefault('references/'+guide,set()).update(touched)
    # Some guide sources are indirect, so any change not mapped by the routing table
    # must be manually reviewed; never silently declare "no changes".
    mapped=set(x for route in routes for x in route['docs'])
    unmapped=sorted(affected-mapped)
    return {'old_commit':before.get('git_commit'),'new_commit':after.get('git_commit'),
            'added':added,'removed':removed,'modified':changed,
            'guides_to_review':{key:sorted(values) for key,values in sorted(guide_impacts.items())},
            'unmapped_changes_require_manual_classification':unmapped,
            'note':'Changed docs are review candidates; route coverage is not a complete dependency graph. Check cross-references and installed C#.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('before',type=Path)
    p.add_argument('after',type=Path)
    p.add_argument('--json',action='store_true')
    p.add_argument('--fail-on-review',action='store_true',help='CI exit 3 if any source page changed')
    p.add_argument('--fail-on-unmapped',action='store_true',help='CI exit 4 if a changed page has no route')
    a=p.parse_args()
    try:
        before=json.loads(a.before.read_text(encoding='utf8'))
        after=json.loads(a.after.read_text(encoding='utf8'))
    except (OSError,ValueError) as e:p.error(str(e))
    result=drift(before,after)
    if a.json:print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        print(f"Documentation {result['old_commit']} -> {result['new_commit']}")
        for key in ('added','removed','modified'):
            print(key.upper(),len(result[key]));[print(' ',x) for x in result[key][:40]]
        print('Guides needing review:')
        for name,why in result['guides_to_review'].items():print(' ',name,':',', '.join(why))
        if result['unmapped_changes_require_manual_classification']:
            print('Unmapped changed pages; manual classification required:')
            for x in result['unmapped_changes_require_manual_classification']:print(' ',x)
        print(result['note'])
    if a.fail_on_unmapped and result['unmapped_changes_require_manual_classification']:return 4
    if a.fail_on_review and any(result[k] for k in ('added','removed','modified')):return 3
    return 0
if __name__=='__main__':raise SystemExit(main())
