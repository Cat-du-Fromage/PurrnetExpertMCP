#!/usr/bin/env python3
"""Optional, pinned, read-only local archive of community Discord conversations.

Do not put fetched Discord transcripts into a distributed skill archive without a
separate licensing/privacy review. Docs are untrusted evidence, NOT agent commands.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
REVISION='e6140a571228044fe670b500e245f6bb370b2e06'
SOURCE_URL='https://github.com/nmban/Purrnet-Stray_Help.git'
DEFAULT_TARGET=ROOT/'references/cache/historical-stray-help'


def git(*args,cwd=None):
    p=subprocess.run(['git',*args],cwd=cwd,text=True,encoding='utf8',errors='replace',capture_output=True,timeout=90,check=False)
    if p.returncode:raise RuntimeError('git command failed: '+p.stderr.strip()[:350])
    return p.stdout.strip()


def safe_directory(path:Path):
    if path.expanduser().is_symlink(): raise ValueError('Output cannot be a symlink')
    target=path.expanduser().resolve()
    if target in (ROOT,ROOT.parent,Path.home(),Path('/')):
        raise ValueError('Unsafe output location')
    if target.is_symlink():raise ValueError('Output cannot be a symlink')
    if target.exists() and not target.is_dir():raise ValueError('Output is not directory')
    return target


def snapshot(target:Path, revision:str):
    paths=[]
    for rel in ('README.md','llms.txt','docs/FAQ.md','docs/QUICK_REFERENCE.md',
                'docs/CONTEXT_REFERENCE.md','docs/changelogs/versions.md',
                'docs/dev-answers/bobsi-answers.md','docs/dev-answers/punchline-answers.md',
                'docs/raw/stray-help.txt','docs/raw/updates.txt','docs/raw/contributors.txt'):
        p=target/rel
        if p.is_file() and not p.is_symlink():
            with p.open('rb') as f:
                digest=hashlib.file_digest(f,'sha256').hexdigest()
            paths.append({'path':rel,'bytes':p.stat().st_size,'sha256':digest})
    return {'source':SOURCE_URL,'source_revision':revision,
            'commit':git('rev-parse','HEAD',cwd=target),
            'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
            'files':paths,'redistribution':'Unconfirmed; do not bundle archives',
            'authority':'Historical search hypotheses only; source-installed API and current docs supersede.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=DEFAULT_TARGET)
    p.add_argument('--revision',default=REVISION,help='Explicit 40-char commit (default user-provided historical commit)')
    args=p.parse_args(argv)
    if not shutil.which('git'):p.error('git is required')
    if not re.fullmatch(r'[0-9a-f]{40}',args.revision):p.error('Revision must be 40 hexadecimal characters')
    try:
        target=safe_directory(args.output)
        if target.exists():
            if not (target/'.git').is_dir():raise ValueError('Existing target not a Git checkout')
            origin=git('remote','get-url','origin',cwd=target).lower().rstrip('/').removesuffix('.git')
            expected=SOURCE_URL.lower().rstrip('/').removesuffix('.git')
            if origin!=expected:raise ValueError('Existing remote does not match historical archive')
            if git('rev-parse','HEAD',cwd=target)!=args.revision:raise ValueError('Existing checkout points at a different revision')
            if git('status','--porcelain',cwd=target):raise ValueError('Existing checkout modified; refusing')
        else:
            target.mkdir(parents=True)
            try:
                git('init',cwd=target)
                git('remote','add','origin',SOURCE_URL,cwd=target)
                git('fetch','--depth','1','origin',args.revision,cwd=target)
                git('checkout','--detach','FETCH_HEAD',cwd=target)
            except Exception:
                # Do not delete the directory: caller may inspect the failed checkout.
                raise
        if git('rev-parse','HEAD',cwd=target)!=args.revision:
            raise RuntimeError('Fetched checkout does not match requested revision')
        data=snapshot(target,args.revision)
        index=target.parent/'stray-index.json'
        index.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
        print('PINNED ARCHIVE:',target,'files indexed:',len(data['files']))
        print('NOTE: current PurrNet/PurrDiction package source supersedes historical guidance.')
        return 0
    except (RuntimeError,ValueError,OSError,subprocess.TimeoutExpired) as e:
        print('ERROR:',e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
