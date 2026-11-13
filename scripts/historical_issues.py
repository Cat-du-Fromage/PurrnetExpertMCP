#!/usr/bin/env python3
"""Search version-scoped, archived PurrNet incident hypotheses.

This is a *historical* aid, not a current issue tracker or API reference.
Every result must be verified in the actual installed PurrNet/PurrDiction source.
No network calls, third-party libraries or remote commands.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references' / 'historical' / 'incident-catalog.json'
PIN = 'e6140a571228044fe670b500e245f6bb370b2e06'


def normalize(value: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if not unicodedata.combining(c))


def read_catalog(path: Path = CATALOG) -> dict:
    obj = json.loads(path.read_text(encoding='utf-8'))
    if obj.get('snapshot') != PIN or not isinstance(obj.get('issues'), list):
        raise ValueError('Catalog must have exact pinned source and issues')
    return obj


def semver(s: str | None):
    if not isinstance(s, str):return None
    m = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?', s.strip(), re.IGNORECASE)
    return tuple(int(x) for x in m.groups()) if m else None


def project_package_version(project: Path | None, package: str):
    """Return (version, evidence). Refuse contradictory installed and lock versions.

    Manifest git branches cannot be treated as exact package versions. Prefer actual
    package.json and lockfile when they agree, but report conflicting evidence.
    """
    if not project:return None, 'No project provided'
    if not project.is_dir():return None,'Unity project directory not found'
    sources=[]
    lock=project/'Packages/packages-lock.json'
    try:
        if lock.is_file():
            val=json.loads(lock.read_text(encoding='utf-8-sig')).get('dependencies',{}).get(package,{})
            if isinstance(val,dict) and semver(val.get('version')):
                sources.append(('packages-lock.json',val['version']))
    except (ValueError,OSError,AttributeError) as e:return None,f'Could not inspect lockfile: {e}'
    roots=[project/'Packages',project/'Library/PackageCache',project/'Assets/PurrNet',project/'Assets/PurrDiction']
    for parent in roots:
        if parent.is_file():continue
        if parent.name in ('PurrNet','PurrDiction'):
            locations=[parent/'package.json']
        else:
            locations=list(parent.glob('*/package.json')) if parent.is_dir() else []
        for p in locations:
            try:
                if p.is_file():
                    pkg=json.loads(p.read_text(encoding='utf-8-sig'))
                    if pkg.get('name')==package and semver(pkg.get('version')):
                        sources.append((str(p.relative_to(project)),pkg['version']))
            except (ValueError,OSError,AttributeError):continue
    distinct={semver(v) for _,v in sources}
    if len(distinct)>1:return None,'CONFLICTING version evidence: '+repr(sources)
    if not sources:return None,'No resolved package version; git branch/manifest spec alone is insufficient'
    return sources[0][1],'; '.join(f'{src}={ver}' for src,ver in sources)


def version_assessment(issue: dict, version: str | None):
    fixed=semver(issue.get('claimed_fixed_in'))
    current=semver(version)
    if issue['classification'] != 'historical_fixed':
        return 'not_a_fix_claim', 'Entry is not a historical bug-fix verdict; check official docs.'
    if fixed is None:
        return 'fix_version_unspecified', 'Archived account has no validated version boundary.'
    if current is None:
        return 'unknown_version', 'Cannot compare: resolve installed package.json or lockfile.'
    if current < fixed:
        return 'older_than_claimed_fix', f'Installed {version} predates claimed historical {issue["claimed_fixed_in"]}; verify applicability before upgrading.'
    return 'at_or_after_claimed_fix', f'Installed {version} is >= claimed historical {issue["claimed_fixed_in"]}. Do NOT presume this old bug explains a new failure.'


def analyze(issue: dict, project:Path|None=None, version:str|None=None):
    kind='dev.purrnet.purrdiction' if issue['id'].startswith('PREDICTION_') else 'dev.purrnet.purrnet'
    found, why=project_package_version(project,kind) if project else (None,'No Unity project provided')
    if version and found and semver(version)!=semver(found):
        label='conflicting_override'; detail=f'CLI version {version} conflicts with resolved {kind} {found}; refusing comparison.'
        used=None
    else:
        used=version or found
        label,detail=version_assessment(issue,used)
    return dict(id=issue['id'],title=issue['title'],classification=issue['classification'],
        package=kind,installed_version=used,version_evidence=why,assessment=label,
        warning=detail,historical_hypothesis=issue['historical_hypothesis'],
        verify=issue['verify'],official_docs=issue['official_docs'],
        historical_url=issue['historical_url'],source_revision=PIN)


def matches(query: str, obj: dict, limit: int = 12):
    needle=normalize(query)
    bits=[s for s in re.findall(r'[\w]+',needle) if len(s)>2]
    scored=[]
    for issue in obj['issues']:
        haystack=normalize(' '.join([issue['id'].replace('_',' '),issue['title'],*issue.get('search_terms',[]),issue['historical_hypothesis']]))
        score=sum(2 if normalize(tok) in normalize(' '.join(issue['search_terms'])) else 1 for tok in bits if tok in haystack)
        if needle in haystack:score+=5
        if score:scored.append((score,issue))
    return [x for _,x in sorted(scored,key=lambda z:(-z[0],z[1]['id']))[:limit]]


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default=None,help='Symptom/symbol search; omit with --id to inspect one incident')
    p.add_argument('--id',help='Exact incident id')
    p.add_argument('--project',type=Path,help='Unity project for package version evidence')
    p.add_argument('--version',help='Exact PurrNet or PurrDiction version as override')
    p.add_argument('--limit',type=int,default=8)
    p.add_argument('--json',action='store_true')
    args=p.parse_args(argv)
    if args.limit<1 or args.limit>35:p.error('--limit must be between 1 and 35')
    if not args.query and not args.id:p.error('Provide a query or --id')
    if args.version and semver(args.version) is None:p.error('--version must be a semver (1.20.0)')
    try:
        obj=read_catalog()
        if args.id:
            issues=[x for x in obj['issues'] if x['id']==args.id]
            if not issues:
                print('Unknown incident id',file=sys.stderr);return 2
        else:issues=matches(args.query,obj,args.limit)
        result={'source_revision':PIN,'archived':True,'note':'Archived claims ONLY; verify in current official docs and installed C#.',
                'results':[analyze(issue,args.project,args.version) for issue in issues]}
        if args.json:print(json.dumps(result,ensure_ascii=False,indent=2))
        else:
            print('ARCHIVED INCIDENTS — not current bug reports. Source:',PIN)
            if not issues:print('No matching curated case: search official docs and optional Stray archive.')
            for x in result['results']:
                print(f"\n{x['id']} | {x['classification']} | {x['assessment']}")
                print(' Historical hypothesis:',x['historical_hypothesis'])
                print(' Evidence to collect:',x['verify'])
                print(' Version:',x['installed_version'] or 'UNKNOWN',x['version_evidence'])
                print(' Warning:',x['warning'])
                print(' Source:',x['historical_url'])
        return 0
    except (OSError,ValueError) as e:
        print('ERROR:',e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
