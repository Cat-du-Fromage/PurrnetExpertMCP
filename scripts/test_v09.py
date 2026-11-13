#!/usr/bin/env python3
"""v0.9 regression suite: official API decision paths + Anthropic skill authoring.

No Unity, Claude models, Docker, network, or real agent is exercised here.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_skill_authoring
import route_docs
import doc_coverage_matrix
import cross_skill_selector
import trigger_probe


class V09Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads((ROOT/'evals/v0.9-hardcases.json').read_text(encoding='utf-8'))['cases']

    def test_metadata_and_anthropic_authoring(self):
        out=audit_skill_authoring.audit(ROOT)
        self.assertEqual([],out['errors'])
        self.assertLess(out['checks']['skill_lines'],500)
        self.assertLessEqual(out['checks']['description_chars'],1024)
        self.assertGreaterEqual(out['checks']['direct_reference_links'],12)

    def test_anthropic_audit_fails_too_long_description(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            s=(ROOT/'SKILL.md').read_text(encoding='utf-8')
            s=s.replace('description: "', 'description: "'+('x'*1025),1)
            (p/'SKILL.md').write_text(s,encoding='utf-8')
            errors=audit_skill_authoring.audit(p)['errors']
            self.assertTrue(any('1024' in e for e in errors))

    def test_anthropic_audit_detects_broken_direct_link(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            (p/'SKILL.md').write_text((ROOT/'SKILL.md').read_text(encoding='utf-8'))
            errors=audit_skill_authoring.audit(p)['errors']
            self.assertTrue(any('cassé' in e for e in errors))

    def test_eval_cases_have_assertions_and_context(self):
        self.assertGreaterEqual(len(self.cases),12)
        for c in self.cases:
            self.assertGreater(len(c['prompt']),20,c['id'])
            self.assertTrue(c['assertions'],c['id'])
            if c['required_reference']:
                self.assertTrue((ROOT/c['required_reference']).is_file(),c['id'])

    def test_explicit_not_purrnet_exclusion(self):
        for phrase in ('Notre projet utilise uniquement FishNet et Mirror, pas PurrNet : configure NetworkTransform.',
                       'Not PurrNet: we are on Mirror with NetworkTransform.',
                       'I am not using PurrNet, I use FishNet.'):
            self.assertFalse(trigger_probe.detect(phrase, False)['should_suggest_skill'], phrase)
            self.assertIsNone(cross_skill_selector.choose(phrase, False)['choice'], phrase)

    def test_new_technical_routes_reachable(self):
        for c in self.cases:
            if c['required_route'] is None:continue
            route_ids=[x['id'] for x in route_docs.detailed_route(c['prompt'])['routes']]
            self.assertIn(c['required_route'],route_ids,c['id']+' '+repr(route_ids))

    def test_new_guides_are_selected_in_routes(self):
        for c in self.cases:
            if not c['required_route']:continue
            selection=route_docs.detailed_route(c['prompt'])
            self.assertIn(c['required_reference'].removeprefix('references/'), selection['guides'],c['id'])

    def test_version_gate_mirror(self):
        p=(ROOT/'references/prediction/mirror-and-visibility.md').read_text()
        for keyword in ('>= 1.4.0','< 1.4.0','PredictedIdentitySpawner','HideFrom','NetworkIdentity'):
            self.assertIn(keyword,p)

    def test_official_visibility_priority(self):
        doc=(ROOT/'references/core/visibility-priority.md').read_text()
        for needle in ('whitelist','blacklist','Parent','OU','composant','réévaluation'):
            self.assertIn(needle.lower(),doc.lower())

    def test_security_spawn_gate_refuses_all_by_default(self):
        doc=(ROOT/'references/core/spawn-security-and-persistence.md').read_text()
        self.assertIn('return false;',doc)
        self.assertNotIn('return true;',doc)
        self.assertIn('TryGetRawPrefab',doc)

    def test_doc_coverage_audits_new_pages(self):
        rules=json.loads((ROOT/'references/task-routes.json').read_text())['rules']
        pages={'systems-and-modules/network-identity/dont-destroy-on-load.md','systems-and-modules/collider-rollback.md','client-side-prediction/predicted-visibility.md','tools/example-unknown.md'}
        result=doc_coverage_matrix.classify(pages,rules)
        self.assertEqual(result['total'],4)
        self.assertIn('tools/example-unknown.md',result['unrouted_technical'])
        self.assertNotIn('systems-and-modules/collider-rollback.md',result['unrouted_technical'])
        self.assertEqual([],result['critical_unrouted'])

    def test_examples_declared_not_compiled(self):
        for path in ('core/spawn-security-and-persistence.md','core/player-identity-and-lazy-refs.md',
                     'prediction/one-shot-input-and-events.md','prediction/mirror-and-visibility.md'):
            txt=(ROOT/'references'/path).read_text(encoding='utf-8')
            self.assertTrue(any(needle in txt.lower() for needle in ('non compil','non compilé','non compilés','pas de prefab unity compilé')),path)

    def test_document_version_not_hardcoded_as_latest(self):
        head=(ROOT/'SKILL.md').read_text()
        self.assertNotIn('PurrNet version latest: 1.25.0',head)
        self.assertIn('package installé',head)

if __name__ == '__main__':
    unittest.main()
