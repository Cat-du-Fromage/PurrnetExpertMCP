#!/usr/bin/env python3
"""Offline regressions for the v0.5 routing, gates, guard and inventory."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import check_doc_versions as vers
import route_docs
import docs_drift
import doc_coverage_matrix as matrix
import guard_predicted_code as guard

class V05Tests(unittest.TestCase):
 def test_transform_never_routes_prediction_without_prediction_context(self):
  r,g,d=route_docs.route('NetworkTransform fluide avec interpolation')
  ids={x['id'] for x in r}
  self.assertIn('network-transform',ids)
  self.assertNotIn('predicted-policy',ids)
  self.assertIn('plug-n-play-components/network-transform.md',d)
  self.assertNotIn('client-side-prediction/prediction-policies.md',d)
 def test_health_event_routes_sync(self):
  r,g,d=route_docs.route('Implémente la synchronisation de santé avec événements')
  self.assertIn('sync-serialization',{x['id'] for x in r})
  self.assertIn('core/sync-types-decision.md',g)
 def test_animator_routes_wrapper(self):
  _,g,d=route_docs.route('Pourquoi mon NetworkAnimator ne synchronise pas les triggers ?')
  self.assertIn('components/network-animator.md',g)
  self.assertIn('plug-n-play-components/network-animator.md',d)
 def test_network_audio_assets(self):
  _,g,d=route_docs.route('NetworkAudioSource PlayOneShot dynamique')
  self.assertIn('components/network-audio.md',g)
  self.assertIn('systems-and-modules/network-manager/network-assets.md',d)
 def test_asset_registries(self):
  _,g,d=route_docs.route('Configurer NetworkSceneAssets pour scene additive')
  self.assertIn('core/network-assets-addressables.md',g)
 def test_large_data(self):
  _,g,d=route_docs.route('SyncBigData pour avatar image')
  self.assertIn('core/serialization-advanced.md',g)
 def test_pred_controller(self):
  _,g,d=route_docs.route('Contrôleur PurrDiction INPUT STATE rollback')
  self.assertIn('prediction/manager-inspector.md',g)
  self.assertIn('client-side-prediction/security.md',d)
 def test_pred_projectile(self):
  _,g,d=route_docs.route('Predicted projectile with lag compensation')
  self.assertIn('prediction/hierarchy-advanced.md',g)
  self.assertIn('client-side-prediction/lag-compensation.md',d)
 def test_predicted_state_node_is_prediction(self):
  r,g,d=route_docs.route('PredictedStateNode avec state machine')
  self.assertEqual(route_docs.context('PredictedStateNode avec state machine'),'prediction')
  self.assertIn('predicted-state-machines',{x['id'] for x in r})
  self.assertNotIn('classic-state-machines',{x['id'] for x in r})
 def test_lobby_does_not_force_voice(self):
  _,g,d=route_docs.route('Configurer PurrLobby menu de jeu')
  self.assertIn('addons/purrlobby-workflow.md',g)
  self.assertNotIn('addons/purrvoice-workflow.md',g)
 def test_voice_does_not_force_lobby(self):
  _,g,d=route_docs.route('Configurer PurrVoice microphone mute')
  self.assertIn('addons/purrvoice-workflow.md',g)
  self.assertNotIn('addons/purrlobby-workflow.md',g)
 def test_no_prediction_negation(self):
  r,g,d=route_docs.route('Je veux NetworkTransform sans prédiction pour co-op')
  self.assertNotIn('predicted-policy',{x['id'] for x in r})
  self.assertEqual(route_docs.context('sans prédiction'),'unspecified')
 def test_boundary_no_substring(self):
  self.assertFalse(route_docs.term_found(route_docs.norm('my antiNetworkTransformX'),'NetworkTransform'))
 def test_version_page_excluded_exit(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'doc.md';p.write_text('---\nversion: ">=1.4.0"\n---\n# docs')
   r=subprocess.run([sys.executable,str(ROOT/'scripts/check_doc_versions.py'),str(p),'--version','1.3.0','--strict'],capture_output=True)
   self.assertEqual(r.returncode,3,r.stdout.decode())
 def test_version_unknown_exit(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'doc.md';p.write_text('# docs')
   r=subprocess.run([sys.executable,str(ROOT/'scripts/check_doc_versions.py'),str(p),'--strict'],capture_output=True)
   self.assertEqual(r.returncode,2)
 def test_version_mixed_requires_line(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'doc.md';p.write_text('# Title\n{% version range=">=1.4.0" %}\nnew api\n{% endversion %}\n{% version range="<1.4.0" %}\nold api\n{% endversion %}')
   cmd=[sys.executable,str(ROOT/'scripts/check_doc_versions.py'),str(p),'--version','1.3.0','--strict']
   self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,3)
   self.assertEqual(subprocess.run(cmd+['--at-line','6'],capture_output=True).returncode,0)
   self.assertEqual(subprocess.run(cmd+['--at-line','3'],capture_output=True).returncode,3)
 def test_guard_indirect_audio(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'Pawn.cs'
   p.write_text('class Pawn:PredictedIdentity<I,S>{AudioSource _audio; private void DoSound(){_audio.Play();} protected override void Simulate(I i,ref S s,float dt){DoSound();}}')
   v=guard.inspect(p)
   self.assertTrue(any('Indirect' in x[2] and 'audio' in x[2].lower() for x in v),v)
 def test_guard_indirect_rpc(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'Pawn.cs'
   p.write_text('class Pawn:PredictedIdentity<I,S>{[ServerRpc] private void SendEvent(){} private void Helper(){SendEvent();} protected override void Simulate(I i,ref S s,float dt){Helper();}}')
   v=guard.inspect(p);self.assertTrue(any('RPC' in x[2] for x in v),v)
 def test_drift_ci_unmapped_blocks(self):
  with tempfile.TemporaryDirectory() as tmp:
   a=Path(tmp)/'a.json';b=Path(tmp)/'b.json'
   a.write_text('{"files":[]}')
   b.write_text('{"files":[{"path":"new/something.md","sha256":"3"}]}')
   cmd=[sys.executable,str(ROOT/'scripts/docs_drift.py'),str(a),str(b),'--fail-on-unmapped']
   self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,4)
 def test_matrix_classifies_all(self):
  files={'plug-n-play-components/network-transform.md','systems-and-modules/transports/eos-transport.md','made-with-purrnet/README.md'}
  rules=[{'docs':['plug-n-play-components/network-transform.md']}]
  result=matrix.classify(files,rules)
  self.assertEqual(result['total'],3)
  self.assertEqual(result['routed'],1)
  self.assertEqual(len(result['unrouted_technical']),1)
 def test_every_path_and_guide_exists(self):
  routes=json.loads((ROOT/'references/task-routes.json').read_text())
  self.assertGreaterEqual(len(routes['rules']),29)
  for r in routes['rules']:
   for g in r['guides']:
    self.assertTrue((ROOT/'references'/g).is_file(),(r['id'],g))
   for d in r['docs']:
    self.assertNotIn('..',Path(d).parts)
 def test_user_report_declares_limits(self):
  r=(ROOT/'QUALITY_REPORT.md').read_text()
  self.assertIn('Non exécuté',r)
  self.assertIn('Unity',r)
if __name__=='__main__':unittest.main(verbosity=2)
