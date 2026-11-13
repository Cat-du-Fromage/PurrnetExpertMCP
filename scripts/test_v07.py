#!/usr/bin/env python3
"""v0.7 regression tests for the archived issue triage + safe opt-in retrieval.

All tests are local; no Discord exchange is treated as authoritative.
"""
from __future__ import annotations
from pathlib import Path
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import historical_issues as history
import route_docs
import search_stray_archive
import sync_stray_archive
import trigger_probe


def git(*args,cwd=None):
    return subprocess.run(['git',*args],cwd=cwd,check=True,text=True,capture_output=True).stdout.strip()

class StrayRegression(unittest.TestCase):
    def test_catalog_fixed_source_and_coverage(self):
        obj=history.read_catalog()
        self.assertEqual(obj['snapshot'],history.PIN)
        self.assertGreaterEqual(len(obj['issues']),30)
        ids=[x['id'] for x in obj['issues']]
        self.assertEqual(len(ids),len(set(ids)))
        types={x['classification'] for x in obj['issues']}
        self.assertTrue({'historical_fixed','expected_behavior','stale_guidance','feature_milestone','historical_workaround','current_pattern'}.issubset(types))
        for issue in obj['issues']:
            self.assertTrue(issue['verify'])
            self.assertTrue(issue['official_docs'])
            self.assertTrue(issue['historical_url'].startswith('https://github.com/nmban/Purrnet-Stray_Help/blob/'+history.PIN))
            self.assertTrue(all(x.endswith('.md') for x in issue['official_docs']))
            self.assertTrue(issue['search_terms'])

    def test_historical_fixed_never_implies_live_bug(self):
        obj=history.read_catalog();issue=next(x for x in obj['issues'] if x['id']=='HOST_OBSERVERS_RPC_TWICE')
        a=history.analyze(issue,version='1.25.0')
        self.assertEqual(a['assessment'],'at_or_after_claimed_fix')
        self.assertIn('Do NOT presume',a['warning'])
        b=history.analyze(issue,version='1.1.0')
        self.assertEqual(b['assessment'],'older_than_claimed_fix')
        self.assertEqual(history.analyze(issue)['assessment'],'unknown_version')

    def test_stale_and_expected_behavior_not_reported_as_patch(self):
        obj=history.read_catalog()
        for tag in ('DISSONANCE_NO_INTEGRATION','LEGACY_SCENE_EVENT','OWNER_FALSE_DESPAWN','TRANSFORM_NOT_SERIALIZABLE'):
            issue=next(x for x in obj['issues'] if x['id']==tag)
            self.assertEqual(history.analyze(issue,version='1.25.0')['assessment'],'not_a_fix_claim')

    def test_project_versions_core_and_prediction_are_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'Packages').mkdir();(p/'Assets/PurrDiction').mkdir(parents=True)
            (p/'Packages/packages-lock.json').write_text(json.dumps({'dependencies':{'dev.purrnet.purrnet':{'version':'1.25.0'},'dev.purrnet.purrdiction':{'version':'1.2.3'}}}))
            (p/'Assets/PurrDiction/package.json').write_text(json.dumps({'name':'dev.purrnet.purrdiction','version':'1.2.3'}))
            obj=history.read_catalog();issue=next(x for x in obj['issues'] if x['id']=='PREDICTION_ROLLBACK_LATE_JOIN')
            result=history.analyze(issue,project=p)
            self.assertEqual(result['package'],'dev.purrnet.purrdiction')
            self.assertEqual(result['assessment'],'older_than_claimed_fix')
            self.assertEqual(history.project_package_version(p,'dev.purrnet.purrnet')[0],'1.25.0')
            self.assertEqual(history.analyze(issue,project=p,version='1.25.0')['assessment'],'conflicting_override')
            (p/'Assets/PurrDiction/package.json').write_text(json.dumps({'name':'dev.purrnet.purrdiction','version':'1.5.0'}))
            self.assertIn('CONFLICTING',history.project_package_version(p,'dev.purrnet.purrdiction')[1])

    def test_avoid_old_absolute_facts(self):
        obj=history.read_catalog()
        stale=[x for x in obj['issues'] if x['classification']=='stale_guidance']
        self.assertGreaterEqual(len(stale),4)
        s=' '.join(x['historical_hypothesis']+x['note'] for x in stale)
        self.assertIn('Dissonance',s)
        self.assertIn('OnPlayer',s) if 'OnPlayer' in s else self.assertIn('scene',s)

    def test_queries_yield_relevant_cases(self):
        obj=history.read_catalog()
        cases={'syncvar null':'SYNCVAR_NULL_OLD','RPC twice host':'RPC_DUPLICATE_HOST',
               'getclientplayload':'AUTH_API_TYPO','bitpacker array size':'BITPACKER_ARRAY_SIZE',
               'steamworks cs1061':'STEAM_CS1061','late join empty list':'LATE_JOIN_LIST',
               'dissonance missing':'DISSONANCE_NO_INTEGRATION'}
        for query,expected in cases.items():
            with self.subTest(query=query):
                ids={x['id'] for x in history.matches(query,obj,limit=12)}
                self.assertIn(expected,ids)

    def test_routes_to_historical_guides(self):
        cases=['rpc double host','onPlayerJoinedScene triggers before loading',
               'steamworks cs1061','syncvar null','duplicate spawn',
               'networktransform bizarre','bufferlast missing client',
               'purrdiction late join','isOwner false despawn']
        for prompt in cases:
            with self.subTest(prompt=prompt):
                data=route_docs.detailed_route(prompt)
                self.assertTrue(any(r['id'].startswith('historical-') for r in data['routes']),data)
                self.assertIn('historical/triage-playbook.md',data['guides'])

    def test_activation_intended_not_actual_agent(self):
        positives=['PurrNet SyncVar null exception','PurrDiction pooled projectile disappears',
                   'NetworkTransform non controller frozen','Steamworks CS1061 dans mon projet PurrNet',
                   'OnSpawned twice on my Unity multiplayer player','Un nouveau joueur reçoit une liste vide au late join']
        for q in positives:
            self.assertTrue(trigger_probe.detect(q,True)['should_suggest_skill'],q)
        self.assertFalse(trigger_probe.detect('Mon widget UI local Unity clignote',False)['should_suggest_skill'])
        self.assertFalse(trigger_probe.detect('My Mirror networking RPC fails',False)['should_suggest_skill'])

    def test_bounded_search_and_redaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'docs').mkdir();(p/'docs/FAQ.md').write_text('No issue\nproblem with SyncVar token=abcdefg\nproblem with SyncVar password: foo\n')
            res=search_stray_archive.search(p,'SyncVar',limit=1)
            self.assertEqual(len(res),1)
            self.assertEqual(res[0]['line'],2)
            self.assertIn('[REDACTED]',res[0]['snippet'])
            self.assertNotIn('abcdefg',res[0]['snippet'])
            with self.assertRaises(ValueError):search_stray_archive.search(p,'',limit=5)
            with self.assertRaises(ValueError):search_stray_archive.search(p,'SyncVar',limit=999)

    def test_pinned_clone_mechanics_on_mock_local_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);remote=root/'historical-upstream';remote.mkdir()
            git('init','-b','main',str(remote))
            git('config','user.email','test@example.invalid',cwd=remote)
            git('config','user.name','Test Author',cwd=remote)
            (remote/'docs').mkdir();(remote/'docs/FAQ.md').write_text('## FAQ\nSyncVar null historical test')
            (remote/'README.md').write_text('# mock archive')
            git('add','.',cwd=remote);git('-c','commit.gpgsign=false','commit','-m','mock',cwd=remote)
            sha=git('rev-parse','HEAD',cwd=remote)
            target=root/'cache'/'historical-stray-help'
            with patch.object(sync_stray_archive,'SOURCE_URL',str(remote)):
                with contextlib.redirect_stdout(io.StringIO()):
                    rc=sync_stray_archive.main(['--output',str(target),'--revision',sha])
            self.assertEqual(rc,0)
            self.assertEqual(git('rev-parse','HEAD',cwd=target),sha)
            self.assertTrue(json.loads((target.parent/'stray-index.json').read_text())['files'])
            (target/'README.md').write_text('tampered')
            with patch.object(sync_stray_archive,'SOURCE_URL',str(remote)):
                with contextlib.redirect_stderr(io.StringIO()):
                    rc=sync_stray_archive.main(['--output',str(target),'--revision',sha])
            self.assertEqual(rc,2,'modified checkout must be refused')

    def test_version_gate_does_not_elevate_old_legacy_claims(self):
        o=history.read_catalog();x=next(z for z in o['issues'] if z['id']=='LEGACY_LATEST')
        r=history.analyze(x,version='1.25.0')
        self.assertEqual(r['assessment'],'not_a_fix_claim')
        self.assertIn('docs/CONTEXT_REFERENCE.md',r['historical_url'])

    def test_cli_json(self):
        stdout=io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(history.main(['--id','HOST_OBSERVERS_RPC_TWICE','--version','1.25.0','--json']),0)
        result=json.loads(stdout.getvalue())
        self.assertEqual(result['results'][0]['assessment'],'at_or_after_claimed_fix')

if __name__=='__main__':unittest.main(verbosity=2)
