#!/usr/bin/env python3
"""Advisory C# replay-side-effect scanner; NOT a Roslyn compiler/analyzer.

Finds methods named Simulate/LateSimulate and flags dangerous operations in their
bodies, including instance calls like `_audio.Play()`. Uses a lexical mask so
comments/string literals don't create false positives. Same-file helper call traversal is best-effort, but no cross-file semantic/dataflow
proof exists; a clean scan MUST NOT be reported as validation of gameplay.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

METHOD = re.compile(r'\b(?:protected|private|public|internal)\s+(?:override\s+|virtual\s+|sealed\s+|static\s+|async\s+)*[\w<>?,\[\]\s]+?\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{', re.M)
RULES = {
 'Unity/frame time': r'\b(?:Time\.(?:deltaTime|fixedDeltaTime|time|frameCount|realtimeSinceStartup|unscaledDeltaTime)|DateTime\.(?:Now|UtcNow)|Environment\.TickCount|Stopwatch\.GetTimestamp)\b',
 'Non-predicted RNG': r'\b(?:UnityEngine\.Random|Random\.(?:Range|value|insideUnitSphere)|System\.Random\s*\()',
 'Classic Unity spawning': r'\b(?:Instantiate|Destroy|Object\.Instantiate|Object\.Destroy)\s*\(',
 'Live input in replay': r'\b(?:Input\.(?:Get\w+|mouse\w+|touch\w+)|Keyboard\.current|Mouse\.current|Gamepad\.current|Touchscreen\.current)\b',
 'Persistent/external side effect': r'\b(?:PlayerPrefs\.(?:Set\w+|Save)|Application\.OpenURL|File\.(?:Write\w*|Append\w*)|Directory\.CreateDirectory|HttpClient\.|UnityWebRequest\.|Analytics\.|Debug\.Log\w*\s*\()',
 'Visual-only changes': r'\b(?:Animator\.(?:SetTrigger|Play|CrossFade)|ParticleSystem\.(?:Play|Emit)|AudioSource\.(?:Play|PlayOneShot)|VFX\.Play)\s*\(',
 'Possible audio/particle playback (review receiver type)': r'\b\w+\.(?:Play|PlayOneShot|Emit|Stop)\s*\(',
}
COMPILED = {k:re.compile(v) for k,v in RULES.items()}

def lexical_mask(src: str) -> str:
    """Mask strings/comments with spaces while preserving newlines and offsets."""
    out=list(src); i=0;n=len(src)
    def erase(a,b):
        for k in range(a,b):
            if src[k]!='\n':out[k]=' '
    while i<n:
        if src.startswith('//',i):
            j=src.find('\n',i);j=n if j<0 else j;erase(i,j);i=j
        elif src.startswith('/*',i):
            j=src.find('*/',i+2);j=n if j<0 else j+2;erase(i,j);i=j
        elif src.startswith('"""',i):  # C# raw string literal
            count=3
            while i+count<n and src[i+count]=='"':count+=1
            j=src.find('"'*count,i+count);j=n if j<0 else j+count;erase(i,j);i=j
        elif src[i]=='"' or (src[i]=='@' and i+1<n and src[i+1]=='"'):
            start=i;verb=src[i]=='@';i+=2 if verb else 1
            while i<n:
                if src[i]=='"':
                    if verb and i+1<n and src[i+1]=='"':i+=2;continue
                    i+=1;break
                if not verb and src[i]=='\\':i+=2;continue
                i+=1
            erase(start,i)
        elif src[i]=="'":
            start=i;i+=1
            while i<n:
                if src[i]=='\\':i+=2;continue
                if src[i]=="'":i+=1;break
                i+=1
            erase(start,i)
        else:i+=1
    return ''.join(out)

def blocks(src):
    for m in METHOD.finditer(src):
        start=m.end();depth=1;i=start
        while i<len(src) and depth:
            if src[i]=='{':depth+=1
            elif src[i]=='}':depth-=1
            i+=1
        if depth==0:yield m.group(1),src[start:i-1],start

def inspect(path:Path):
    original=path.read_text(encoding='utf-8-sig',errors='replace')
    if not any(word in original for word in ('PredictedIdentity','DeterministicIdentity','PredictedModule')):
        return []
    src=lexical_mask(original)
    typed=set(re.findall(r'\b(?:AudioSource|ParticleSystem|VisualEffect|VFXGraph)\s+(\w+)\s*(?:[;=,])',src))
    typed.update(re.findall(r'\b(\w+)\s*=\s*(?:GetComponent|GetComponentInChildren)\s*<\s*(?:AudioSource|ParticleSystem|VisualEffect)\s*>',src))
    rpc_names=set(re.findall(r'\[(?:ServerRpc|ObserversRpc|TargetRpc)[^\]]*\]\s*(?:(?:public|private|protected|internal|static|async|override)\s+)*[\w<>?,\[\]]+\s+(\w+)\s*\(',src))
    bodies={};entries={}
    for method,body,start in blocks(src):
        bodies.setdefault(method,[]).append((body,start))
        if method in ('Simulate','LateSimulate'):entries.setdefault(method,[]).append((body,start))
    problems=[]; seen=set()
    def follow(name,trail):
        if name in trail[:-1] or len(trail)>12:return
        for body,start in bodies.get(name,[]):
            # Same-file helper traversal only: overloaded methods may cause conservative extra alerts.
            findings=set()
            for label,pattern in COMPILED.items():
                for match in pattern.finditer(body):
                    findings.add((start+match.start(),label,match.group(0)))
            for field in typed:
                for match in re.finditer(r'\b'+re.escape(field)+r'\s*\.\s*(?:Play|PlayOneShot|Emit|Stop)\s*\(',body):
                    findings.add((start+match.start(),'Typed audio/particle side effect',match.group(0)))
            for rpc in rpc_names:
                for match in re.finditer(r'\b'+re.escape(rpc)+r'\s*\(',body):
                    findings.add((start+match.start(),'RPC method invoked inside replay',match.group(0)))
            for offset,label,token in sorted(findings):
                issue=(original.count('\n',0,offset)+1,trail[0],
                       ('Indirect via '+ ' -> '.join(trail[1:]) + ': ' if len(trail)>1 else '')+label,token)
                if issue not in seen:seen.add(issue);problems.append(issue)
            # Cannot resolve dynamically dispatched methods, lambda receivers or cross-file helpers.
            for called in set(re.findall(r'(?<![.\w])([A-Za-z_]\w*)\s*\(',body)):
                if called in bodies and called not in trail:
                    follow(called,trail+(called,))
    for name in entries:follow(name,(name,))
    if re.search(r'\bSyncVar\s*<',src):
        problems.append((0,'file','Classic SyncVar alongside predicted source: inspect whether outside predicted simulation','SyncVar'))
    return sorted(problems,key=lambda x:(x[0],x[1],x[2]))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project',type=Path)
    p.add_argument('--limit',type=int,default=150)
    a=p.parse_args();root=a.project.expanduser().resolve()
    if not root.is_dir():p.error('directory missing')
    count=0
    for f in sorted(root.rglob('*.cs')):
        if set(f.relative_to(root).parts)&{'Library','PackageCache','.git','.purrnet-sources'}:continue
        if f.stat().st_size>2_000_000:continue
        for line,method,reason,token in inspect(f):
            print(f'REVIEW {f.relative_to(root)}:{line}: {method}: {reason} [{token}]');count+=1
            if count>=a.limit:
                print('Scan truncated. No clean result can be claimed.');return 1
    print(f'Potential issues: {count}. Heuristic only; Roslyn + Unity + network tests remain mandatory.')
    return 1 if count else 0
if __name__=='__main__':raise SystemExit(main())
