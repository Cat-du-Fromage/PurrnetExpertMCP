#!/usr/bin/env python3
"""Safely add/remove project-level auto-activation hints for Codex/Claude.

The hints cannot force a model to call a skill; they make the trigger explicit in
repo instructions. Requires explicit --apply, never silently overwrites projects.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '<!-- PURRNET-EXPERT AUTO-ACTIVATION BEGIN -->'
END = '<!-- PURRNET-EXPERT AUTO-ACTIVATION END -->'
MANIFEST_SIGNS = ('dev.purrnet.purrnet', 'purrnet/purrnet', 'purrnet.git', 'dev.purrnet.purrdiction', 'purrdiction.git')


def is_purrnet_project(project: Path) -> bool:
    for rel in ('Packages/manifest.json', 'Packages/packages-lock.json'):
        p = project / rel
        if p.is_file():
            s = p.read_text(encoding='utf-8', errors='replace').lower()
            if any(x in s for x in MANIFEST_SIGNS):
                return True
    if (project/'Assets/PurrNet').is_dir() or (project/'Assets/PurrDiction').is_dir():
        return True
    return False


def instruction(skill_path: str, agent: str) -> str:
    return f'''{BEGIN}
### PurrNet Expert — automatic activation ({agent})
This is a Unity project using PurrNet and/or PurrDiction. **Before designing,
writing, refactoring or debugging any multiplayer/networked gameplay**, load
`{skill_path}`. This applies even if the user says only "my player jitters",
"my shots don't sync", "remote inventory", "host works but client doesn't",
"late join is broken", "desync", "rollback", "lag compensation", "lobby",
"ownership", "scene loading" or "I need co-op / dedicated servers".
Apply the same triggers when users describe these symptoms in another language.
For symptoms that resemble known historical bugs (duplicate host RPC, late-join empty
SyncList, SyncVar null, ILPP build crash, SteamWorks errors, WebGL jitter), read
`references/historical/triage-playbook.md` from the installed skill and run
`historical_issues.py` with the actual Unity project version. The archived
Stray Help notes are dated hypotheses, never automatically current fixes.
Also load when editing or reviewing C# that imports `PurrNet`, subclasses
`NetworkIdentity`, `NetworkBehaviour`, `PredictedIdentity` or `PredictedModule`,
or refers to `NetworkManager`, `SyncVar`, `ObserversRpc`, `ServerRpc`,
`NetworkTransform` or `PredictionManager` in this project.
When PurrNet Expert MCP is available, call `get_purrnet_project_context`
first. Use the loaded skill to select the documentation, API and version checks.
Do **not** load for wholly offline UI, shaders, editor cosmetics or ordinary
Unity problems unrelated to network behavior. For Edgegap-specific deployment,
load `edgegap-purrnet` as the primary cloud engineer when available, then
consult `purrnet-expert` for PurrNet gameplay and authority changes only. If the skill path is absent, report the missing install; do not claim
that its docs or checks were applied.
{END}'''


def replace_block(content: str, replacement: str | None) -> str:
    if content.count(BEGIN) > 1 or content.count(END) > 1 or content.count(BEGIN) != content.count(END):
        raise ValueError('Malformed/multiple managed activation markers; manual review required')
    if BEGIN in content:
        first=content.index(BEGIN)
        last=content.index(END, first)+len(END)
        content=content[:first].rstrip() + content[last:]
    content=content.rstrip()
    if replacement:
        content += ('\n\n' if content else '') + replacement
    return content + ('\n' if content else '')


def plan(project: Path, agent: str, action: str):
    name = 'AGENTS.md' if agent == 'codex' else 'CLAUDE.md'
    skill_path = '.agents/skills/purrnet-expert/SKILL.md' if agent == 'codex' else '.claude/skills/purrnet-expert/SKILL.md'
    p=project/name
    old=p.read_text(encoding='utf-8') if p.exists() else ''
    new=replace_block(old, instruction(skill_path,agent) if action=='install' else None)
    return p, old, new, project/skill_path


def main(argv=None) -> int:
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('project', type=Path,help='Unity project root')
    a.add_argument('--target',choices=('codex','claude','both'),default='both')
    a.add_argument('--remove',action='store_true',help='remove only the managed block')
    a.add_argument('--apply',action='store_true',help='make changes; otherwise dry run')
    a.add_argument('--force',action='store_true',help='permit project without detectable PurrNet')
    a.add_argument('--allow-missing-skill',action='store_true',help='allow writing hints even when the chosen skill location is absent')
    opt=a.parse_args(argv)
    project=opt.project.resolve()
    if not (project/'ProjectSettings/ProjectVersion.txt').is_file() and not opt.force:
        print('Not a Unity project (ProjectVersion.txt missing). Use --force to override.',file=sys.stderr)
        return 2
    if not opt.remove and not opt.force and not is_purrnet_project(project):
        print('PurrNet not detected in manifest/lock/Assets. Use --force to override.',file=sys.stderr)
        return 2
    agents=['codex','claude'] if opt.target=='both' else [opt.target]
    changes=[]
    try:
        for agent in agents:changes.append((agent,*plan(project,agent,'remove' if opt.remove else 'install')))
    except (OSError, ValueError) as e:
        print(f'Refusing to change project: {e}',file=sys.stderr); return 3
    if opt.apply and not opt.remove and not opt.allow_missing_skill:
        missing=[str(skill) for _,_,_,_,skill in changes if not skill.is_file()]
        if missing:
            print('Install the skill at each requested location before --apply: '+', '.join(missing), file=sys.stderr)
            return 4
    for agent,path,old,new,skill in changes:
        print(f"{ 'WRITE' if opt.apply else 'DRY RUN'} {path}: {'unchanged' if old==new else 'updating'}")
        if not opt.remove and not skill.is_file():print(f'  NOTICE: {skill} is not installed yet; hints alone cannot load it')
    if opt.apply:
        for _,path,old,new,_ in changes:
            if old!=new:
                if new:
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_text(new,encoding='utf-8')
                elif path.exists():
                    path.unlink()
    return 0

if __name__ == '__main__':raise SystemExit(main())
