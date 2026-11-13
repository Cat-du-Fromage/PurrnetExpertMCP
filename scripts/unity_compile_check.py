#!/usr/bin/env python3
"""Opt-in Unity batchmode *script compilation/import* check (not server build or E2E).

Default: dry-run and print command. --run starts Unity explicitly and parses log for errors.
Close the Unity Editor first; batch import can mutate Library and generated project data.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ERROR_PATTERNS = [re.compile(r"\berror CS\d{4}\b", re.I),
                  re.compile(r"Scripts have compiler errors", re.I),
                  re.compile(r"Compilation failed", re.I),
                  re.compile(r"error:.*(?:assembly|compil)", re.I)]


def build_command(unity: Path, project: Path, log: Path, execute_method: str | None = None) -> list[str]:
    cmd = [str(unity), '-batchmode', '-nographics', '-quit', '-projectPath', str(project), '-logFile', str(log)]
    if execute_method:
        cmd.extend(['-executeMethod', execute_method])
    return cmd


def has_errors(log_text: str) -> list[str]:
    findings = []
    for lineno, line in enumerate(log_text.splitlines(), 1):
        if any(pattern.search(line) for pattern in ERROR_PATTERNS):
            # Preserve only log line, never print secrets without redaction.
            findings.append(f"line {lineno}: " + ("[redacted]" if re.search(r"password|secret|token=|api.?key", line, re.I) else line[:240]))
    return findings[:40]


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project', type=Path)
    p.add_argument('--unity-exe', type=Path, required=True)
    p.add_argument('--log-file', type=Path, required=True)
    p.add_argument('--execute-method', default=None, help='Optional developer-provided static Unity Editor build method')
    p.add_argument('--run', action='store_true', help='Opt in to launching Unity; otherwise dry-run')
    p.add_argument('--json', action='store_true')
    a=p.parse_args(argv)
    project=a.project.resolve(); unity=a.unity_exe.resolve(); log=a.log_file.resolve()
    if not (project/'Assets').is_dir() or not (project/'ProjectSettings').is_dir():
        p.error('Project must have Assets/ and ProjectSettings/')
    cmd=build_command(unity,project,log,a.execute_method)
    result={'schema':'purrnet-unity-batch-compile-v1','ran':False,'command':cmd,'log':str(log),
            'caveat':'Unity script compile/import check only. No dedicated build, two-client or E2E test.'}
    if a.run:
        if not unity.is_file():
            p.error('Unity executable not found')
        if (project/'Temp/UnityLockfile').exists():
            p.error('Unity project appears open (Temp/UnityLockfile). Close Editor before --run.')
        log.parent.mkdir(parents=True,exist_ok=True)
        try:
            out=subprocess.run(cmd, cwd=str(project), capture_output=True, text=True, timeout=1200)
        except (OSError, subprocess.TimeoutExpired) as e:
            result['error']=str(e)
            print(json.dumps(result,ensure_ascii=False,indent=2) if a.json else str(e))
            return 2
        result['ran']=True
        result['exit_code']=out.returncode
        text=log.read_text(encoding='utf-8',errors='replace') if log.exists() else ''
        result['compiler_errors']=has_errors(text)
        result['success']=bool(out.returncode==0 and log.exists() and not result['compiler_errors'])
        if not log.exists():
            result['error']='Unity did not produce the required log'
    if a.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('Command:', ' '.join(cmd))
        print('Ran:',result['ran'],'| Success:',result.get('success','unknown (dry-run)'))
        if result.get('compiler_errors'):
            print('Compilation errors:\n'+'\n'.join(result['compiler_errors']))
        print(result['caveat'])
    if a.run and not result.get('success'):
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
