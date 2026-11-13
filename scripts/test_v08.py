#!/usr/bin/env python3
"""v0.8 unit tests: Edgegap structural comparison fixes, route boundary, evidence, dedicated audit.

These tests do NOT run Unity, Docker, Edgegap, or an agent model.
"""
from __future__ import annotations
from contextlib import redirect_stdout
from io import StringIO
import json
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_dedicated_readiness
import check_evidence
import cross_skill_selector
import route_docs
import unity_compile_check
import subprocess


class V08Tests(unittest.TestCase):
    def test_frontmatter_version_and_progressive_disclosure(self):
        s = (ROOT / 'SKILL.md').read_text()
        self.assertRegex(s, r'version: "0\.(?:[89]|[1-9][0-9])\.[0-9]+"')
        self.assertLess(len(s), 13000)
        for p in ('workflows/feature.md', 'workflows/bug.md', 'workflows/dedicated.md', 'workflows/prediction.md', 'workflows/edgegap-handoff.md'):
            self.assertIn(p, s)

    def test_comparison_uses_verified_edgegap_evals_root(self):
        s = (ROOT / 'references/edgegap-comparison.md').read_text()
        self.assertIn('evals/purrnet-evals.json', s)
        self.assertIn('fd510ba826ea29ab359e70e185d2e650ef6827de', s)

    def test_workflows_have_actionable_gate(self):
        for name in ('feature','bug','dedicated','prediction','edgegap-handoff'):
            txt = (ROOT / 'references/workflows' / (name+'.md')).read_text()
            self.assertGreater(len(txt), 1000)
            self.assertIn('##', txt)
        self.assertIn('D3', (ROOT/'references/validation/acceptance.md').read_text())

    def test_edgegap_boundary_routing_cases(self):
        records = json.loads((ROOT / 'evals/v0.8-routing.json').read_text())
        self.assertGreaterEqual(len(records), 20)
        for item in records:
            actual = cross_skill_selector.choose(item['prompt'], item['purrnet_project'])['choice']
            self.assertEqual(item['expected_skill'], actual, item['prompt'])

    def test_doc_routes_include_dedicated_and_cloud(self):
        for phrase, expected in (
            ('PurrNet host to dedicated server', 'workflow-dedicated-readiness'),
            ('PurrNet edgegap matchmaker', 'workflow-edgegap-handoff')):
            routes = route_docs.detailed_route(phrase)['routes']
            self.assertIn(expected, [r['id'] for r in routes])

    def test_existing_route_no_cloud_capture_for_sync(self):
        routes = route_docs.detailed_route('SyncVar health not synchronizing')['routes']
        self.assertNotIn('workflow-edgegap-handoff', [r['id'] for r in routes])

    def test_fixture_detects_host_only_and_rpc(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td);(root/'Assets').mkdir()
            for s in ('HostOnlyWorld','ConnectLoop','ServerBoot'):
                (root/'Assets'/f'{s}.cs').write_text((ROOT/'evals/fixtures/v08'/f'{s}.cs.txt').read_text())
            (root/'Assets/Scene.unity').write_text((ROOT/'evals/fixtures/v08/Scene.unity.txt').read_text())
            audit = audit_dedicated_readiness.analyze_project(root)
            codes = [x['code'] for x in audit['findings']]
            self.assertIn('HOST_DEPENDENCY', codes)
            self.assertIn('OBSERVER_RPC_SERVER_INIT', codes)
            self.assertIn('ASYNC_CLIENT_START', codes)
            self.assertIn('MULTIPLE_STARTERS', codes)
            self.assertIn('AUTO_START_CONFIG', codes)

    def test_rpc_runlocally_does_not_flag(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'Assets').mkdir()
            (root/'Assets/A.cs').write_text('[ObserversRpc(runLocally:true)] void InitSeed() {}')
            r=audit_dedicated_readiness.analyze_project(root)
            self.assertNotIn('OBSERVER_RPC_SERVER_INIT',[x['code'] for x in r['findings']])

    def test_comments_not_misparsed_as_starters(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'Assets').mkdir()
            (root/'Assets/Comment.cs').write_text('// isHost();\n// StartHost();\n/* [ObserversRpc] void Init() {} */')
            r=audit_dedicated_readiness.analyze_project(root)
            self.assertEqual(r['count'],0)

    def test_bad_unity_path_fails(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                audit_dedicated_readiness.analyze_project(Path(td))

    def test_evidence_example_is_not_claiming_test(self):
        p=ROOT/'assets/validation/evidence.example.json'
        self.assertEqual(check_evidence.verify(json.loads(p.read_text()),p.parent),[])

    def test_evidence_no_pass_without_trace(self):
        p=ROOT/'assets/validation/evidence.example.json'
        x=json.loads(p.read_text());x['gates']['D3']['status']='pass'
        self.assertTrue(any('without evidence D3' in e for e in check_evidence.verify(x,p.parent)))

    def test_evidence_bad_path_and_invalid_gate(self):
        p=ROOT/'assets/validation/evidence.example.json'
        x=json.loads(p.read_text());x['gates']['D2']={'status':'pass','evidence':['../../etc/passwd']}
        self.assertTrue(any('unsafe' in e for e in check_evidence.verify(x,p.parent)))
        x['gates']['D5']['status']='what'
        self.assertTrue(any('Invalid status D5' in e for e in check_evidence.verify(x,p.parent)))

    def test_evidence_higher_gate_depends_on_compilation(self):
        p=ROOT/'assets/validation/evidence.example.json'
        x=json.loads(p.read_text())
        with tempfile.TemporaryDirectory() as td:
            q=Path(td);(q/'test.log').write_text('Unity test output: pretend; not real proof')
            x['gates']['D5']={'status':'pass','evidence':['test.log']}
            errors=check_evidence.verify(x,q)
            self.assertTrue(any('D5 cannot pass without D3' in e for e in errors))

    def test_evidence_path_backed_when_present(self):
        p=ROOT/'assets/validation/evidence.example.json'
        x=json.loads(p.read_text())
        with tempfile.TemporaryDirectory() as td:
            q=Path(td);(q/'api-evidence.log').write_text('Example static-only signature proof')
            x['gates']['D2']={'status':'pass','evidence':['api-evidence.log']}
            self.assertEqual(check_evidence.verify(x,q),[])

    def test_eval_scenarios_have_assertions(self):
        obj=json.loads((ROOT/'evals/v0.8-end-to-end.json').read_text())
        self.assertGreaterEqual(len(obj['scenarios']),8)
        for s in obj['scenarios']:
            self.assertTrue(s['assertions'])
            for path in s['required_references']:
                self.assertTrue((ROOT/path).is_file(),path)

    def test_unity_compile_check_command_is_opt_in(self):
        cmd=unity_compile_check.build_command(Path('/opt/Unity'),Path('/tmp/Proj'),Path('/tmp/unity.log'))
        self.assertIn('-batchmode',cmd)
        self.assertIn('-nographics',cmd)
        self.assertNotIn('-executeMethod',cmd)

    def test_unity_compile_check_logs_detect_errors(self):
        bad='warning CS1234 ignored\nAssets/A.cs(1,2): error CS0246: type missing\nCompilation failed\n'
        found=unity_compile_check.has_errors(bad)
        self.assertEqual(len(found),2)
        self.assertEqual(unity_compile_check.has_errors('Clean exit 0'),[])

    def test_unity_compile_check_dry_run_does_not_launch(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'Assets').mkdir();(root/'ProjectSettings').mkdir()
            result=subprocess.run([sys.executable,str(ROOT/'scripts/unity_compile_check.py'),str(root),
                                  '--unity-exe',str(root/'not-real-Unity'), '--log-file',str(root/'out.log'), '--json'],
                                  capture_output=True,text=True)
            self.assertEqual(result.returncode,0)
            self.assertFalse(json.loads(result.stdout)['ran'])
            self.assertFalse((root/'out.log').exists())

    def test_mock_unity_error_is_not_passed_as_compile(self):
        # Stub the editor subprocess so the fixture behaves identically on Windows and POSIX.
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'Assets').mkdir();(root/'ProjectSettings').mkdir()
            fake=root/'mock-editor'
            fake.touch()
            log = root / 'out.log'

            def run_editor(command, **kwargs):
                self.assertEqual(command[command.index('-logFile') + 1], str(log))
                log.write_text('Assets/Bad.cs(1,2): error CS0246: fake compilation error\n')
                return subprocess.CompletedProcess(command, 0)

            output = StringIO()
            with patch.object(unity_compile_check.subprocess, 'run', side_effect=run_editor), redirect_stdout(output):
                result = unity_compile_check.main([
                    str(root), '--unity-exe', str(fake), '--log-file', str(log), '--run', '--json',
                ])
            self.assertEqual(result, 1)
            obj=json.loads(output.getvalue())
            self.assertTrue(obj['ran'])
            self.assertFalse(obj['success'])
            self.assertTrue(obj['compiler_errors'])

    def test_no_distributed_purrdocs_dump(self):
        import install_project
        self.assertIn('cache', install_project.ignore(ROOT / 'references', ['cache']))


if __name__=='__main__': unittest.main()
