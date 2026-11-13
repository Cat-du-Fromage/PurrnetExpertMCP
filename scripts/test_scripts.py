#!/usr/bin/env python3
"""Offline integration tests for skill tooling, including local Git clone and complete indexing."""
from __future__ import annotations
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import inspect_project
import docs_catalog
import find_api
import guard_predicted_code
import sync_sources


def write(root, path, data):
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(data, encoding='utf-8')
    return dest


def git(*args, cwd=None):
    r = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, check=True)
    return r.stdout.strip()


class SkillScriptsTests(unittest.TestCase):
    def test_inspect_purrnet_and_purrdiction_separately(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root, 'ProjectSettings/ProjectVersion.txt', 'm_EditorVersion: 6000.3.11f1\n')
            write(root, 'Packages/manifest.json', json.dumps({'dependencies': {
                'dev.purrnet.purrnet': 'https://github.com/PurrNet/PurrNet.git?path=/Assets/PurrNet#release',
                'dev.purrnet.purrdiction': 'https://github.com/PurrNet/PurrDiction.git?path=/Assets/PurrDiction#release',
            }}))
            write(root, 'Packages/packages-lock.json', json.dumps({'dependencies': {
                'dev.purrnet.purrnet': {'version': '1.25.0', 'hash': 'abc123', 'source': 'git'},
                'dev.purrnet.purrdiction': {'version': '1.4.0', 'hash': 'def456', 'source': 'git'},
            }}))
            write(root, 'Assets/PurrNet/package.json', '{"name":"dev.purrnet.purrnet","version":"1.25.0"}')
            write(root, 'Assets/PurrDiction/package.json', '{"name":"dev.purrnet.purrdiction","version":"1.4.0"}')
            with patch.object(sys, 'argv', ['inspect_project.py', str(root)]):
                with contextlib.redirect_stdout(io.StringIO()) as f:
                    rc = inspect_project.main()
            data = json.loads(f.getvalue())
            self.assertEqual(rc, 0)
            self.assertTrue(data['purrdiction_detected'])
            self.assertEqual(len(data['packages']), 2)
            versions = {p['name']: p['lock_version'] for p in data['packages']}
            self.assertEqual(versions['dev.purrnet.purrdiction'], '1.4.0')
            self.assertEqual(versions['dev.purrnet.purrnet'], '1.25.0')
            write(root, 'Assets/PurrDiction/Runtime/Controller.cs', 'public void SanitizeInput() {}')
            self.assertIn(root / 'Assets/PurrDiction', list(find_api.roots(root)))

    def test_guard_detects_bad_predicted_tick(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(Path(tmp), 'Assets/Player.cs', '''
            class Player : PredictedIdentity<Foo, Bar> {
              protected override void Simulate(Foo input, ref Bar state, float delta) {
                var tick = Time.deltaTime;
                float damage = UnityEngine.Random.value;
                var clone = Instantiate(prefab);
                Input.GetKeyDown(KeyCode.A);
              }
            }
            ''')
            issues = guard_predicted_code.inspect(path)
            reasons = {x[2] for x in issues}
            self.assertIn('Unity/frame time', reasons)
            self.assertIn('Non-predicted RNG', reasons)
            self.assertIn('Classic Unity spawning', reasons)
            self.assertIn('Live input in replay', reasons)

    def test_summary_broken_path_fails_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            all_required = docs_catalog.CRITICAL
            for path in all_required:
                write(root, path, '# test')
            write(root, 'SUMMARY.md', '[x](client-side-prediction/best-practices.md)\n')
            index = root.parent / 'unrelated-index.json'
            index.write_text(json.dumps({'files': [{'path': p} for p in all_required]}))
            with contextlib.redirect_stdout(io.StringIO()) as f:
                self.assertEqual(docs_catalog.coverage(root, index), 0, f.getvalue())
            write(root, 'SUMMARY.md', '[x](nonexistent.md)\n')
            with contextlib.redirect_stdout(io.StringIO()) as f:
                self.assertEqual(docs_catalog.coverage(root, index), 1)

    def test_offline_git_clone_sync_indexes_all_pages_not_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            upstream = root / 'PurrDocs-upstream'
            upstream.mkdir()
            git('init', '-b', 'main', str(upstream))
            git('config', 'user.name', 'Skill Test', cwd=upstream)
            git('config', 'user.email', 'skill-test@example.com', cwd=upstream)
            for path in docs_catalog.CRITICAL:
                write(upstream, path, '# ' + path)
            write(upstream, 'tools/future-new-module/novel-api.md', '# newly added page\nExampleFoo')
            write(upstream, 'SUMMARY.md', '[New](tools/future-new-module/novel-api.md)\n' +
                  '[Best Practices](client-side-prediction/best-practices.md)\n')
            git('add', '.', cwd=upstream)
            git('commit', '-m', 'initial', cwd=upstream)
            target = root / 'cache' / 'official-docs'
            with patch.object(sync_sources, 'SOURCE_URL', str(upstream)), \
                 patch.object(sys, 'argv', ['sync_sources.py', '--output', str(target)]):
                with contextlib.redirect_stdout(io.StringIO()) as f:
                    rc = sync_sources.main()
            self.assertEqual(rc, 0, f.getvalue())
            index = target.parent / 'docs-index.json'
            data = json.loads(index.read_text())
            self.assertEqual(data['markdown_count'], len(docs_catalog.CRITICAL) + 1)
            self.assertTrue(any(x['path'] == 'tools/future-new-module/novel-api.md' for x in data['files']))
            with contextlib.redirect_stdout(io.StringIO()) as f:
                self.assertEqual(docs_catalog.coverage(target, index), 0, f.getvalue())
            # New file in PurrDocs without a refresh is not silently claimed as already synced.
            write(upstream, 'tools/future-new-module/second.md', '# Second')
            git('add', '.', cwd=upstream)
            git('commit', '-m', 'second', cwd=upstream)
            self.assertFalse((target / 'tools/future-new-module/second.md').exists())
            with patch.object(sync_sources, 'SOURCE_URL', str(upstream)), \
                 patch.object(sys, 'argv', ['sync_sources.py', '--output', str(target), '--refresh']):
                with contextlib.redirect_stdout(io.StringIO()) as f:
                    rc = sync_sources.main()
            self.assertEqual(rc, 0, f.getvalue())
            self.assertTrue((target / 'tools/future-new-module/second.md').exists())
            data = json.loads(index.read_text())
            self.assertEqual(data['markdown_count'], len(docs_catalog.CRITICAL) + 2)
            with contextlib.redirect_stdout(io.StringIO()) as f:
                self.assertEqual(docs_catalog.coverage(target, index), 0, f.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
