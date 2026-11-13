#!/usr/bin/env python3
"""v0.6 tests: trigger heuristics, user-project opt-in hooks, routes and guide depth.

These are local regressions, NOT actual autonomous skill-selection tests in an LLM.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import trigger_probe
import install_activation
import route_docs

class ActivationTests(unittest.TestCase):
    def test_skill_metadata_conforms(self):
        s=(ROOT/'SKILL.md').read_text()
        head=s.split('---',2)[1]
        name=re.search(r'^name:\s*(.*)$',head,re.M).group(1).strip()
        desc=re.search(r'^description:\s*(.*)$',head,re.M).group(1).strip()
        self.assertEqual(name,"purrnet-expert")
        self.assertTrue(1<=len(desc)<=1024,(len(desc),desc))
        self.assertIn('Unity',desc);self.assertIn('PurrNet',desc)
        self.assertIn('In a PurrNet project',desc)
        self.assertIn('late join',desc)
        self.assertTrue('Do NOT' in desc or 'Excludes' in desc, 'Trigger description must explicitly exclude unrelated projects')
        self.assertIn('get_purrnet_project_context',s)

    def test_activation_case_matrix(self):
        data=json.loads((ROOT/'evals/activation-cases.json').read_text())
        self.assertGreaterEqual(len(data),55)
        for x in data:
            with self.subTest(x=x['query']):
                result=trigger_probe.detect(x['query'],x['project_is_purrnet'])
                self.assertEqual(result['should_suggest_skill'],x['expected'],result)

    def test_install_safe_idempotent_and_reversible(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp);(project/'ProjectSettings').mkdir();(project/'Packages').mkdir()
            (project/'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.1.0f1')
            (project/'Packages/manifest.json').write_text('{"dependencies":{"dev.purrnet.purrnet":"1.25.0"}}')
            for rel in ('.agents/skills/purrnet-expert/SKILL.md','.claude/skills/purrnet-expert/SKILL.md'):
                f=project/rel;f.parent.mkdir(parents=True);f.write_text('---\nname: purrnet-expert\n---\n')
            (project/'AGENTS.md').write_text('# Existing project rules\n\nDo not touch our data.\n')
            cli=ROOT/'scripts/install_activation.py'
            def run(*args):return subprocess.run([sys.executable,str(cli),str(project),*args],capture_output=True,text=True)
            self.assertEqual(run('--target','both').returncode,0)
            self.assertNotIn(install_activation.BEGIN,(project/'AGENTS.md').read_text())
            self.assertEqual(run('--target','both','--apply').returncode,0)
            a=(project/'AGENTS.md').read_text();self.assertIn('Do not touch our data.',a)
            self.assertEqual(a.count(install_activation.BEGIN),1)
            self.assertEqual(run('--target','both','--apply').returncode,0)
            self.assertEqual((project/'AGENTS.md').read_text(),a)
            self.assertEqual(run('--target','both','--remove','--apply').returncode,0)
            self.assertNotIn(install_activation.BEGIN,(project/'AGENTS.md').read_text())
            self.assertIn('Do not touch our data.',(project/'AGENTS.md').read_text())
            self.assertFalse((project/'CLAUDE.md').exists())

    def test_reject_nonpurrnet_and_missing_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp);(project/'ProjectSettings').mkdir();(project/'Packages').mkdir()
            (project/'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.1.0f1')
            (project/'Packages/manifest.json').write_text('{}')
            cli=ROOT/'scripts/install_activation.py'
            def run(*args):return subprocess.run([sys.executable,str(cli),str(project),*args],capture_output=True)
            self.assertEqual(run('--apply','--target','codex').returncode,2)
            self.assertEqual(run('--apply','--force','--target','codex').returncode,4)
            self.assertFalse((project/'AGENTS.md').exists())

    def test_install_project_full_and_upgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'ProjectSettings').mkdir();(p/'Packages').mkdir()
            (p/'ProjectSettings/ProjectVersion.txt').write_text('version')
            (p/'Packages/manifest.json').write_text('{"dependencies":{"dev.purrnet.purrnet":"1.25.0"}}')
            script=ROOT/'scripts/install_project.py'
            def run(*args):return subprocess.run([sys.executable,str(script),str(p),*args],capture_output=True,text=True)
            self.assertEqual(run('--target','both').returncode,0)
            self.assertFalse((p/'AGENTS.md').exists())
            self.assertEqual(run('--target','both','--apply').returncode,0)
            self.assertTrue((p/'.agents/skills/purrnet-expert/SKILL.md').is_file())
            self.assertTrue((p/'.claude/skills/purrnet-expert/SKILL.md').is_file())
            self.assertEqual((p/'AGENTS.md').read_text().count(install_activation.BEGIN),1)
            self.assertEqual(run('--target','both','--apply').returncode,3)
            self.assertEqual(run('--target','both','--apply','--upgrade').returncode,0)
            backups=list((p/'.agents/skill-backups').glob('purrnet-expert-*'))
            self.assertEqual(len(backups),1)
            self.assertEqual((p/'CLAUDE.md').read_text().count(install_activation.BEGIN),1)

    def test_refuse_malformed_existing_hook(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp);(project/'ProjectSettings').mkdir()
            (project/'ProjectSettings/ProjectVersion.txt').write_text('x')
            (project/'AGENTS.md').write_text(install_activation.BEGIN+'\nmissing end')
            ret=subprocess.run([sys.executable,str(ROOT/'scripts/install_activation.py'),str(project),'--target','codex','--force','--apply'],capture_output=True)
            self.assertEqual(ret.returncode,3)
            self.assertIn(install_activation.BEGIN,(project/'AGENTS.md').read_text())

    def test_new_routes_and_references(self):
        cases=[
            ('Mon joueur tremble sur le deuxième PC','jitter-network-classic','components/network-transform.md'),
            ('PurrDiction mon personnage jitter pendant rollback','jitter-predicted','prediction/real-world-recipes.md'),
            ('Mes joueurs en coop sont désynchronisés','general-multiplayer','core/scene-playbook.md'),
            ('PurrNet SyncVar santé pour 2 clients','health-events-recipes','core/sync-recipes.md'),
            ('PurrNet NetworkBones pour les bras','network-bones-ownership','components/network-bones-ownership.md'),
            ('PurrNet problèmes MTU fragments','mtu-and-network-messages','core/messaging-and-mtu.md'),
            ('PurrDiction PredictedStateNode transitions','predicted-state-machine-guide','prediction/state-machine-playbook.md'),
            ('Configurer NetworkSceneAssets en scene additive','assets-scene-workflow','core/scene-playbook.md'),
            ('PurrNet IAsyncPackable serializer','large-data-serialization','core/serialization-playbook.md')]
        for task,rid,guide in cases:
            with self.subTest(task=task):
                routes,guides,_=route_docs.route(task)
                self.assertIn(rid,[r['id'] for r in routes])
                self.assertIn(guide,guides)
        r,_,_=route_docs.route('NetworkTransform fluide avec interpolation')
        self.assertNotIn('predicted-policy',{x['id'] for x in r})

    def test_guide_depth_and_references(self):
        guides=['core/sync-recipes.md','core/messaging-and-mtu.md','core/scene-playbook.md','core/serialization-playbook.md','prediction/real-world-recipes.md','prediction/state-machine-playbook.md','tools/troubleshooting-playbook.md','build/build-release-checklist.md','components/network-bones-ownership.md']
        for name in guides:
            with self.subTest(path=name):
                text=(ROOT/'references'/name).read_text()
                self.assertGreater(len(text),900)
                self.assertIn('http',text)
        rules=json.loads((ROOT/'references/task-routes.json').read_text())['rules']
        self.assertGreaterEqual(len(rules),45)
        for item in rules:
            for rel in item['guides']:
                self.assertTrue((ROOT/'references'/rel).is_file(),(item['id'],rel))

    def test_transparent_test_limits(self):
        self.assertIn('NOT actual LLM',(ROOT/'scripts/trigger_probe.py').read_text())
        self.assertIn('Non exécuté',(ROOT/'QUALITY_REPORT.md').read_text())

if __name__=='__main__':unittest.main(verbosity=2)
