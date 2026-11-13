#!/usr/bin/env python3
"""Check version-gated PurrDocs sections against installed package versions.

Does not rewrite docs or claim that PurrDocs/main matches the package API. A
moving Git ref is NOT an exact version. Exact source signatures win over docs.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parents[1]
CACHE=HERE/'references/cache/official-docs'
GATE=re.compile(r'(?P<op>>=|<=|==|!=|>|<)\s*(?P<v>\d+\.\d+(?:\.\d+)?(?:-[\w.-]+)?)')
FRONT=re.compile(r'^---\s*\n([\s\S]*?)\n---',re.M)
MARKER=re.compile(r'{%\s*version\s+range=["\']([^"\']+)["\']\s*%}')
ENDMARKER=re.compile(r'{%\s*endversion\s*%}')

def parse_version(x):
    if not x:return None
    m=re.fullmatch(r'(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?',str(x).strip())
    if not m:return None
    return (int(m[1]),int(m[2]),int(m[3] or 0),m[4] or '')

def compare(a,b):
    # Stable semver release ranks after its prerelease with identical numbers.
    x=a[:3];y=b[:3]
    if x!=y:return (x>y)-(x<y)
    if a[3]==b[3]:return 0
    if not a[3]:return 1
    if not b[3]:return -1
    def parts(s):
        return tuple((0,int(p)) if p.isdigit() else (1,p) for p in s.split('.'))
    pa,pb=parts(a[3]),parts(b[3]);return (pa>pb)-(pa<pb)

def satisfies(version,expression):
    if version is None:return None
    tests=GATE.findall(expression)
    if not tests:return None
    for op,raw in tests:
        other=parse_version(raw)
        if other is None:return None
        c=compare(version,other)
        if not {'>':c>0,'>=':c>=0,'<':c<0,'<=':c<=0,'==':c==0,'!=':c!=0}[op]:return False
    return True

def detect(project:Path,package):
    """Fail closed when installed sources disagree without an exact lock version.

    Unity may retain stale PackageCache and example Assets packages simultaneously;
    picking the first package.json would silently bless the wrong API version.
    """
    name='dev.purrnet.purrdiction' if package=='prediction' else 'dev.purrnet.purrnet'
    paths=[project/'Assets'/('PurrDiction' if package=='prediction' else 'PurrNet')/'package.json']
    for root in (project/'Packages',project/'Library'/'PackageCache'):
        if root.is_dir():paths.extend(root.glob('*/package.json'))
    found=[]
    for path in sorted(set(paths)):
        try:data=json.loads(path.read_text(encoding='utf8'))
        except (OSError,ValueError):continue
        if data.get('name')==name and parse_version(data.get('version')):
            found.append((data['version'],str(path.relative_to(project))))
    lock=project/'Packages'/'packages-lock.json';locked=None
    try:
        data=json.loads(lock.read_text(encoding='utf8'))['dependencies'].get(name,{})
        if parse_version(data.get('version')):locked=data['version']
    except (OSError,ValueError,KeyError,TypeError):pass
    if locked:
        agreeing=[x for x in found if x[0]==locked]
        if agreeing:return agreeing[0][0],agreeing[0][1]+' (lock matched)'
        if found:return None,'AMBIGUOUS: lock version '+locked+' conflicts with local sources '+','.join(sorted(set(v for v,_ in found)))
        return locked,'Packages/packages-lock.json (source not available: verify SHA)'
    unique=sorted(set(v for v,_ in found))
    if len(unique)==1:return found[0]
    if len(unique)>1:return None,'AMBIGUOUS: multiple local source versions '+','.join(unique)
    return None,None

def gate_ranges(md):
    found=[]
    front=FRONT.match(md)
    if front:
        f=re.search(r'^version:\s*["\']?([^\n"\']+)',front[1],re.M)
        if f:found.append({'scope':'page','line':1,'range':f[1].strip()})
    for m in MARKER.finditer(md):
        remainder=md[m.end():]
        end=ENDMARKER.search(remainder)
        end_offset=m.end()+end.end() if end else len(md)
        found.append({'scope':'block','line':md.count('\n',0,m.start())+1,
                      'end_line':md.count('\n',0,end_offset)+1,'range':m[1]})
    return found

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('page',type=Path,help='Page path relative to PurrDocs clone or an absolute Markdown file')
    p.add_argument('--docs',type=Path,default=CACHE)
    p.add_argument('--project',type=Path)
    p.add_argument('--package',choices=['prediction','core'])
    p.add_argument('--version',help='Exact installed package version, overrides --project')
    p.add_argument('--json',action='store_true')
    p.add_argument('--strict',action='store_true',help='exit 2 for unknown version/gate, 3 for excluded scope')
    p.add_argument('--at-line',type=int,help='Check only a chosen documentation line and its enclosing gates (recommended for mixed-version pages)')
    a=p.parse_args();filepath=a.page if a.page.is_absolute() else a.docs/a.page
    if not filepath.is_file():p.error(f'Page not found: {filepath}')
    pkg=a.package or ('prediction' if 'client-side-prediction' in filepath.parts else 'core')
    ver=a.version;source='--version'
    if not ver and a.project:ver,source=detect(a.project.resolve(),pkg)
    version=parse_version(ver)
    if ver and version is None:p.error('Version must be exact SemVer (e.g. 1.4.0 or 1.5.0-beta.17)')
    gates=gate_ranges(filepath.read_text(encoding='utf-8-sig',errors='replace'))
    if a.at_line is not None and a.at_line < 1:
        p.error('--at-line must be >= 1')
    enriched=[]
    for g in gates:
        ok=satisfies(version,g['range'])
        match='unknown' if ok is None else 'applicable' if ok else 'excluded'
        affects=(g['scope']=='page' or a.at_line is None or g['line']<=a.at_line<=g['end_line'])
        enriched.append(dict(g,status=match,relevant_to_selected_scope=affects))
    selected=[g for g in enriched if g['relevant_to_selected_scope']]
    unknown=not version or any(g['status']=='unknown' for g in selected)
    excluded=any(g['status']=='excluded' for g in selected)
    verdict='UNKNOWN' if unknown else 'EXCLUDED' if excluded else 'ALLOWED_BY_DOCUMENT_GATES_ONLY'
    result={'page':str(filepath),'package':pkg,'version':ver,'version_source':source,'version_exact':bool(version),
            'checked_line':a.at_line,'verdict':verdict,'gates':enriched,
            'note':'This is only a documentation range check. Even ALLOWED requires inspection of installed C# API and a Unity build.'}
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('Page:',filepath,'| Package:',pkg,'| Exact version:',ver or 'UNKNOWN','| Verdict:',verdict)
        for g in enriched:print(f"  {g['scope']} line {g['line']}: {g['range']} => {g['status']} ({'relevant' if g['relevant_to_selected_scope'] else 'other version block'})")
        print(result['note'])
    if a.strict and unknown:return 2
    if a.strict and excluded:return 3
    return 0
if __name__=='__main__':raise SystemExit(main())
