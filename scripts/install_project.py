#!/usr/bin/env python3
"""Install/update this Agent Skill in a Unity project and opt-in project hooks.

Dry-run by default. With --apply, it copies the local skill to standard Codex/
Claude paths. Existing installations require --upgrade and are backed up. Never
writes a project without an explicit user command.
"""
from __future__ import annotations
import argparse
import datetime
import os
from pathlib import Path
import shutil
import sys
from install_activation import is_purrnet_project, instruction, replace_block

ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={'__pycache__','.git','.pytest_cache','cache','official-docs','skill-backups'}
SKILL_ENTRIES={'SKILL.md','README.md','QUALITY_REPORT.md','RELEASE_MANIFEST.json','LICENSE',
               '.gitignore','references','scripts','assets','evals'}

def ignore(directory,names):
    return [n for n in names if n in EXCLUDE or n.endswith(('.pyc','.pyo','.zip'))
            or (Path(directory)==ROOT and n not in SKILL_ENTRIES)]

def main(argv=None):
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('project',type=Path)
    a.add_argument('--target',choices=('codex','claude','both'),default='both')
    a.add_argument('--apply',action='store_true',help='execute; otherwise dry run')
    a.add_argument('--upgrade',action='store_true',help='backup and replace existing skill')
    a.add_argument('--skip-hooks',action='store_true',help='do not edit AGENTS.md/CLAUDE.md')
    a.add_argument('--force',action='store_true',help='allow project without detected PurrNet')
    opt=a.parse_args(argv)
    project=opt.project.resolve()
    if not opt.force and not (project/'ProjectSettings/ProjectVersion.txt').is_file():
        print('Not a Unity project; use --force to override.',file=sys.stderr); return 2
    if not opt.force and not is_purrnet_project(project):
        print('No PurrNet package detected; use --force for an intended migration.',file=sys.stderr);return 2
    agents=['codex','claude'] if opt.target=='both' else [opt.target]
    plan=[]
    try:
        for agent in agents:
            relative=Path('.agents/skills/purrnet-expert' if agent=='codex' else '.claude/skills/purrnet-expert')
            dest=project/relative
            same=dest.resolve()==ROOT.resolve() if dest.exists() else False
            if dest.is_symlink():raise ValueError(f'Symlink destination refused: {dest}')
            if dest.exists() and not same and not opt.upgrade:
                raise ValueError(f'{dest} exists; rerun with --upgrade to back up and replace it')
            guidance=None
            if not opt.skip_hooks:
                guidance=project/('AGENTS.md' if agent=='codex' else 'CLAUDE.md')
                old=guidance.read_text(encoding='utf-8') if guidance.exists() else ''
                new=replace_block(old,instruction(relative.as_posix()+'/SKILL.md',agent))
            else:old=new=''
            plan.append((agent,dest,same,guidance,old,new))
    except (ValueError,OSError) as e:
        print('Refusing changes:',e,file=sys.stderr);return 3
    for agent,dest,same,guidance,_,_ in plan:
        print(f"{'INSTALL' if opt.apply else 'DRY RUN'} {agent}: {dest}"+(' (already source)' if same else ''))
        if guidance:print(f"{'UPDATE' if opt.apply else 'DRY RUN'} project activation: {guidance}")
    if not opt.apply:return 0
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for agent,dest,same,guidance,old,new in plan:
        if not same:
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():
                backups=dest.parents[1]/'skill-backups'
                backups.mkdir(parents=True,exist_ok=True)
                backup=backups/('purrnet-expert-'+stamp)
                suffix=0
                while backup.exists():suffix+=1;backup=backups/('purrnet-expert-'+stamp+f'-{suffix}')
                shutil.move(str(dest),str(backup))
                print(f'Backup preserved at {backup}')
            shutil.copytree(ROOT,dest,ignore=ignore)
        if guidance is not None and old!=new:
            guidance.parent.mkdir(parents=True,exist_ok=True)
            guidance.write_text(new,encoding='utf-8')
    return 0

if __name__=='__main__':raise SystemExit(main())
