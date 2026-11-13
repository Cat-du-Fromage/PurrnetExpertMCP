#!/usr/bin/env python3
"""Conservative text/YAML inventory of Unity scenes, prefabs and ScriptableObjects.

Unity binary-serialized assets cannot be parsed by this script. IDs are only
text occurrences: no proof that components are active or configured correctly.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
import json
import sys

TERMS=('NetworkManager','PredictionManager','UDPTransport','WebTransport','CompositeTransport',
       'NetworkIdentity','NetworkRules','NetworkVisibility','PredictedIdentity','PredictedTransform',
       'PredictedParent','PredictedRigidbody','NetworkTransform','PlayerSpawner','PurrLobby')

def inventory(project:Path):
    files=[];counts=defaultdict(int);limited=False
    for folder in (project/'Assets',project/'Packages'):
        if not folder.is_dir():continue
        for path in folder.rglob('*'):
            if not path.is_file() or path.suffix not in ('.unity','.prefab','.asset','.asmdef'):continue
            if 'Library' in path.parts:continue
            if len(files)>=15000:limited=True;break
            try:
                if path.stat().st_size>8_000_000:continue
                blob=path.read_bytes()
                if b'\0' in blob[:1024]:continue
                content=blob.decode('utf-8-sig',errors='replace')
            except OSError:continue
            matches=[name for name in TERMS if name in content]
            for name in matches:counts[name]+=1
            if matches:files.append({'path':str(path.relative_to(project)),'mentions':matches})
    return {'candidate_files':files,'term_file_counts':dict(counts), 'truncated':limited,
            'warning':'Text-only hints; Unity prefabs commonly store script GUIDs without class names. Absence of a term is not proof of missing component. Must open scenes/Inspector in Unity.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path)
    a=p.parse_args();project=a.project.resolve()
    if not project.is_dir():p.error('Unity project missing')
    print(json.dumps(inventory(project),indent=2,ensure_ascii=False))
if __name__=='__main__':raise SystemExit(main())
