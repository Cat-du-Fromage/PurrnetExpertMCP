#!/usr/bin/env python3
"""Context-aware, bilingual topic routing for PurrNet documents.

Heuristic discovery is NOT semantic understanding. Exact symbol names are stronger
than generic words; in ambiguous cases the tool includes multiple routes and
instructs the agent to verify via the complete documentation catalog.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
ROUTES=ROOT/'references/task-routes.json'
DOCS=ROOT/'references/cache/official-docs'
PRED_TERMS=('purrdiction','predicted','prediction','predictive','predict','prédit','prédite','predic','rollback','reconcil','lagcompensationtick','predictedtransform','predictedrigidbody','isverifiedview','sfloat')
CLASSIC_TERMS=('networktransform','networkrigidbody','networkanimator','networkreflection','networkaudiosource','networkownershiptoggle','synclist','syncvar','syncinput','validatedsyncvar','networkbones','syncdictionary','networkstatemachine','networkstate machine')

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
    return s.replace('_',' ')

def term_found(text,term):
    needle=norm(term).strip()
    return bool(re.search(r'(?<![\w])'+re.escape(needle).replace(r'\ ',r'\s+')+r'(?![\w])',text))

def context(task):
    t=norm(task)
    pred=any(term_found(t,s) for s in PRED_TERMS) or bool(re.search(r'(?<![\w])predicted[a-z][a-z0-9]*\b',t))
    classic=any(term_found(t,s) for s in CLASSIC_TERMS)
    # "without prediction" explicitly means the user doesn't want prediction.
    if re.search(r'\b(sans|without|no|pas de)\s+(?:la\s+)?(?:prediction|purrdiction|rollback)\b',t) and not any(term_found(t,s) for s in ('predictedtransform','predictedidentity','predictedrigidbody')):
        pred=False
    return 'mixed' if pred and classic else 'prediction' if pred else 'classic' if classic else 'unspecified'

def route(task,rules=None):
    if rules is None:rules=json.loads(ROUTES.read_text(encoding='utf8'))['rules']
    t=norm(task);ctx=context(task)
    scored=[]
    for r in rules:
        rc=r.get('context','any')
        if rc=='prediction' and ctx not in ('prediction','mixed'):continue
        if rc=='classic' and ctx=='prediction':continue
        hits=[s for s in r.get('keywords',[]) if term_found(t,s)]
        if not hits:continue
        # Avoid broad 'component' when stronger technical matches exist; retain as background.
        scored.append((r,hits))
    matching=[r for r,_ in scored]
    guides=list(dict.fromkeys(x for r in matching for x in r['guides']))
    official=list(dict.fromkeys(x for r in matching for x in r['docs']))
    return matching,guides,official

def detailed_route(task,rules=None):
    rules=rules or json.loads(ROUTES.read_text(encoding='utf8'))['rules']
    q=norm(task)
    matched,guides,docs=route(task,rules)
    return {'context':context(task),'routes':[{'id':r['id'],'matched_terms':[w for w in r['keywords'] if term_found(q,w)]} for r in matched],
            'guides':guides,'docs':docs,'needs_catalog_search':not bool(matched),
            'warning':'Routes are discovery hints, not a proof of completeness or API compatibility. Browse official-docs when available; inspect package source and version gates.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('task')
    p.add_argument('--docs',type=Path,default=DOCS)
    p.add_argument('--json',action='store_true')
    p.add_argument('--require-docs',action='store_true',help='exit 2 if needed official pages are not synced')
    a=p.parse_args()
    result=detailed_route(a.task)
    result['guides']=[{'path':'references/'+x,'exists':(ROOT/'references'/x).is_file()} for x in result['guides']]
    result['docs']=[{'path':x,'synced':(a.docs/x).is_file()} for x in result['docs']]
    if a.json:print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        print('Context:',result['context'],'| Routes:',','.join(r['id'] for r in result['routes']) or 'NONE -> SEARCH CATALOG')
        for g in result['guides']:print('GUIDE',g['path'],'OK' if g['exists'] else 'MISSING')
        for d in result['docs']:print('DOC',d['path'],'OK' if d['synced'] else 'UNSYNCED')
        print(result['warning'])
    if any(not x['exists'] for x in result['guides']):return 1
    if a.require_docs and any(not x['synced'] for x in result['docs']):return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
