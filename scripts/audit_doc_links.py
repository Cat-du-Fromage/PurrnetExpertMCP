#!/usr/bin/env python3
"""Audit relative Markdown links across a PurrDocs checkout (not just SUMMARY).

GitBook sometimes uses redirects or non-Markdown links; this tool reports
suspicions with source locations rather than claiming semantic completeness.
"""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

from purrnet_common import docs_checkout

ROOT=Path(__file__).resolve().parents[1]
DOCS=docs_checkout(ROOT)
MD_LINK=re.compile(r'(?<!!)\[[^\]]+\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)')

def inspect(docs:Path):
    broken=[];checked=0;ignored=Counter()
    for file in sorted(docs.rglob('*.md')):
        if '.git' in file.relative_to(docs).parts:continue
        try:lines=file.read_text(encoding='utf-8-sig',errors='replace').splitlines()
        except OSError:continue
        in_fence=False
        for n,line in enumerate(lines,1):
            if re.match(r'^\s*(```|~~~)',line):in_fence=not in_fence;continue
            if in_fence:continue
            for m in MD_LINK.finditer(line):
                raw=m.group(1).strip('<>');u=urlsplit(raw);link=unquote(u.path)
                if not link:ignored['anchor-only']+=1;continue
                if u.scheme or u.netloc or raw.startswith(('mailto:','//')):ignored['external']+=1;continue
                if link.startswith('/'):ignored['root-absolute']+=1;continue
                base=(file.parent/link).resolve()
                # Don't allow path escaping; GitBook sometimes uses out-of-tree URLs
                if not base.is_relative_to(docs.resolve()):ignored['out-of-tree']+=1;continue
                targets=[base]
                if base.suffix=='':targets += [base.with_suffix('.md'),base/'README.md']
                checked+=1
                if not any(t.is_file() for t in targets):
                    broken.append({'source':str(file.relative_to(docs)),'line':n,'link':raw})
    return {'checked_links':checked,'suspicious_broken_links':broken,'ignored':dict(ignored),
            'note':'Broken links may involve upstream GitBook redirects; inspect manually before fixing. This does not validate API accuracy.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--docs',type=Path,default=DOCS)
    p.add_argument('--strict',action='store_true',help='Return nonzero if suspicious broken links exist')
    p.add_argument('--json',action='store_true')
    p.add_argument('--limit',type=int,default=60)
    a=p.parse_args();docs=a.docs.resolve()
    if not docs.is_dir() or not (docs/'SUMMARY.md').is_file():
        print('Full docs absent: run sync_sources.py first',file=sys.stderr);return 2
    result=inspect(docs)
    if a.json:print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        print('Links checked:',result['checked_links'],'| Suspicious missing:',len(result['suspicious_broken_links']))
        for issue in result['suspicious_broken_links'][:a.limit]:print(f"{issue['source']}:{issue['line']}: {issue['link']}")
        print(result['note'])
    return 1 if a.strict and result['suspicious_broken_links'] else 0
if __name__=='__main__':raise SystemExit(main())
