#!/usr/bin/env python3
"""Additional offline regression tests for 0.4.0 rules, routing and version gates."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
import guard_predicted_code as guard
import route_docs
import check_doc_versions as versions
import audit_doc_links
import audit_project_assets
import docs_drift

class V04Tests(unittest.TestCase):
    def write(self,root,name,value):
        f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(value,encoding='utf8');return f

    def inspect(self,code):
        with tempfile.TemporaryDirectory() as tmp:
            f=self.write(Path(tmp),'Predicted.cs',code)
            return guard.inspect(f)

    def test_instance_audio_play(self):
        issues=self.inspect('''class Pawn : PredictedIdentity<I,S> {
          private AudioSource _audio;
          protected override void Simulate(I input, ref S state, float dt) { _audio.Play(); }
        }''')
        self.assertTrue(any('audio' in x[2].lower() for x in issues),issues)

    def test_audio_playone_shot(self):
        issues=self.inspect('''class Pawn : PredictedIdentity<I,S> {
          AudioSource clip; protected override void Simulate(I i, ref S s, float delta){clip.PlayOneShot(hit);}
        }''')
        self.assertTrue(any('audio' in x[2].lower() for x in issues))

    def test_particle_play(self):
        issues=self.inspect('''class Pawn: PredictedIdentity<I,S>{
          ParticleSystem fx; protected override void Simulate(I i,ref S s,float dt){fx.Play();}
        }''')
        self.assertTrue(any('particle' in x[2].lower() for x in issues))

    def test_no_false_from_comments_strings(self):
        issues=self.inspect('''class Pawn : PredictedIdentity<I,S> {
          protected override void Simulate(I i,ref S s,float dt) {
          // _audio.Play();
          var message = "Time.deltaTime / * Input.GetKeyDown";
          /* UnityEngine.Random.value; */
          s.hp += 1;
        }}''')
        self.assertEqual(issues,[])

    def test_input_getkeydown(self):
        issues=self.inspect('''class Pawn: PredictedIdentity<I,S>{protected override void Simulate(I i,ref S s,float dt){if (Input.GetKeyDown(KeyCode.Space))s.jump=1;}}''')
        self.assertTrue(any('Live input' in x[2] for x in issues))

    def test_predicted_method_only(self):
        issues=self.inspect('''class Pawn: PredictedIdentity<I,S>{
          void Update(){_audio.Play();}
          protected override void Simulate(I i,ref S s,float dt){s.hp++;}
        }''')
        self.assertEqual(issues,[])

    def test_method_body_nested_braces(self):
        issues=self.inspect('''class Pawn: PredictedIdentity<I,S>{protected override void Simulate(I i,ref S s,float dt){if(s.ok){_audio.Play();}s.hp++;}}''')
        self.assertTrue(issues)

    def test_rpc_called_in_simulate(self):
        issues=self.inspect('''class Pawn: PredictedIdentity<I,S>{
          [ServerRpc] private void FireServer() { }
          protected override void Simulate(I i,ref S s,float dt){FireServer();}
        }''')
        self.assertTrue(any('RPC method' in x[2] for x in issues),issues)

    def test_route_inventory(self):
        matches,guides,docs=route_docs.route('Créer un inventaire / inventory multijoueur sécurisé')
        self.assertIn('inventory',[m['id'] for m in matches]);self.assertIn('core/sync-types.md',guides)
        self.assertIn('systems-and-modules/network-modules/owner-only.md',docs)

    def test_route_projectile_has_bp(self):
        _,guides,docs=route_docs.route('Créer un projectile de combat predicted')
        self.assertIn('prediction/best-practices.md',guides)
        self.assertIn('client-side-prediction/best-practices.md',docs)

    def test_route_unknown_fallback(self):
        matched,guides,docs=route_docs.route('cryptographie quantique pour pots de fleurs')
        self.assertEqual((matched,guides,docs),([],[],[]))

    def test_every_route_file_exists(self):
        manifest=json.loads((ROOT/'references/task-routes.json').read_text())
        for rule in manifest['rules']:
            for guide in rule['guides']:
                self.assertTrue((ROOT/'references'/guide).is_file(),f"{rule['id']} guide missing: {guide}")
            for doc in rule['docs']:
                self.assertNotIn('..',Path(doc).parts)

    def test_semver_basic(self):
        self.assertTrue(versions.satisfies(versions.parse_version('1.4.0'),'>=1.4.0'))
        self.assertFalse(versions.satisfies(versions.parse_version('1.3.9'),'>=1.4.0'))
        self.assertFalse(versions.satisfies(versions.parse_version('1.4.0-beta.5'),'>=1.4.0'))
        self.assertTrue(versions.satisfies(versions.parse_version('1.5.0-beta.17'),'>=1.4.0'))
        self.assertTrue(versions.satisfies(versions.parse_version('1.3.0'),'>=1.3.0 <1.4.0'))
        self.assertIsNone(versions.satisfies(None,'>=1.4.0'))

    def test_gate_extract(self):
        page='''---\nversion: ">=1.3.0"\n---\n# Test\n{% version range=">=1.4.0" %}\nhello\n{% endversion %}\n{% version range="<1.4.0" %}\nold\n{% endversion %}'''
        g=versions.gate_ranges(page)
        self.assertEqual([x['range'] for x in g],['>=1.3.0','>=1.4.0','<1.4.0'])

    def test_installed_package_from_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.write(root,'Assets/PurrDiction/package.json','{"name":"dev.purrnet.purrdiction","version":"1.4.0"}')
            self.assertEqual(versions.detect(root,'prediction')[0],'1.4.0')
            self.assertEqual(versions.detect(root,'core'),(None,None))

    def test_link_audit_reports_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.write(root,'SUMMARY.md','[legit](x.md) [bad](missing.md) [external](https://purrnet.dev/docs)\n')
            self.write(root,'x.md','# ok')
            data=audit_doc_links.inspect(root)
            self.assertEqual(data['checked_links'],2)
            self.assertEqual(len(data['suspicious_broken_links']),1)

    def test_asset_audit_is_text_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.write(root,'Assets/Test.unity','NetworkManager UDPTransport')
            d=audit_project_assets.inventory(root)
            self.assertEqual(d['term_file_counts']['NetworkManager'],1)
            self.assertIn('GUIDs',d['warning'])

    def test_docs_drift_flags_guide(self):
        a={'git_commit':'before','files':[{'path':'systems-and-modules/network-modules/owner-only.md','sha256':'abc'}]}
        b={'git_commit':'after','files':[{'path':'systems-and-modules/network-modules/owner-only.md','sha256':'changed'}]}
        diff=docs_drift.drift(a,b)
        self.assertIn('references/core/sync-types.md',diff['guides_to_review'])
        self.assertEqual(diff['modified'],['systems-and-modules/network-modules/owner-only.md'])

    def test_docs_drift_unmapped_is_reported(self):
        diff=docs_drift.drift({'files':[]},{'files':[{'path':'new-module/feature.md','sha256':'a'}]})
        self.assertEqual(diff['unmapped_changes_require_manual_classification'],['new-module/feature.md'])

    def test_system_rng_is_found(self):
        issues=self.inspect("class Player:PredictedIdentity<I,S>{protected override void Simulate(I i,ref S s,float dt){var r = new System.Random();}}")
        self.assertTrue(any('RNG' in x[2] for x in issues),issues)

    def test_evals_have_assertions(self):
        data=json.loads((ROOT/'evals/v0.4-hardcases.json').read_text())
        self.assertGreaterEqual(len(data),25)
        self.assertTrue(all(len(d['assertions'])>=3 for d in data))

if __name__=='__main__':unittest.main(verbosity=2)
