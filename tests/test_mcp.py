import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import anyio
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from purrnet_common import SOURCE_URL
from purrnet_expert_mcp.api_lookup import lookup_installed
from purrnet_expert_mcp.indexer import CacheError, build, database, diagnose
from purrnet_expert_mcp.project import CORE, PREDICTION, inspect_project
from purrnet_expert_mcp.search import lookup_document, search_docs

COMMIT = "a" * 40
REVISION = "b" * 40
PAGE = "client-side-prediction/mirror.md"
MARKDOWN = """# Predicted Identity

## Mirroring
{% version range=">=1.4.0" %}
Automatic mirroring uses NetworkIdentity for remote players.
{% endversion %}

{% version range="<1.4.0" %}
Legacy mirroring uses PredictedIdentitySpawner.
{% endversion %}

## General
Observe visible objects after spawn.
"""
SOURCE = """namespace PurrNet;
public class NetworkManager {
    public void StartClient() { }
    [System.Obsolete("Use the other overload")]
    public void StartClient(string address) { }
    public void Wrapper() { StartClient(); }
    public string Example => "MissingMethod()";
    public event System.Action Ready;
    public int Count { get; private set; }
#if EXTRA_API
    public void ConditionalCall() { }
#endif
}
public class DifferentType {
    public void Other() {}
}
public class SyncVar<T> {}
"""


def write(root: Path, path: str, data: str | dict) -> Path:
    file = root / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(data) if isinstance(data, dict) else data, encoding="utf-8", newline="\n")
    return file


class MCPTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.project = self.root / "Unity"
        self.docs = self.root / "cache" / "official-docs"
        write(self.project, "ProjectSettings/ProjectVersion.txt", "m_EditorVersion: 6000.3.4f1\n")
        write(self.project, "Packages/manifest.json", {"dependencies": {CORE: "1.25.0", PREDICTION: "https://example.test/pkg#release"}})
        write(self.project, "Packages/packages-lock.json", {
            "dependencies": {CORE: {"version": "1.25.0", "source": "registry"},
                             PREDICTION: {"version": "https://example.test/pkg#release", "source": "git", "hash": REVISION}},
        })
        write(self.project, f"Library/PackageCache/{CORE}@old/package.json", {"name": CORE, "version": "1.20.0"})
        write(self.project, f"Library/PackageCache/{CORE}@current/package.json", {"name": CORE, "version": "1.25.0"})
        self.prediction = f"Library/PackageCache/{PREDICTION}@{REVISION[:12]}"
        write(self.project, self.prediction + "/package.json", {"name": PREDICTION, "version": "1.3.7"})
        write(self.project, f"Library/PackageCache/{CORE}@current/NetworkManager.cs", SOURCE)
        write(self.project, self.prediction + "/PredictedIdentity.cs", "namespace PurrNet.Prediction { public class PredictedIdentity<I, S> {} }")
        (self.project / "Assets").mkdir()

    def prepare_docs(self, commit=COMMIT):
        source = write(self.docs, PAGE, MARKDOWN)
        sync = {
            "source_repository": SOURCE_URL, "git_commit": commit,
            "files": [{"path": PAGE, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}],
        }
        write(self.docs.parent, "docs-index.json", sync)
        return build(self.docs)

    def test_independent_versions_and_resolved_revision(self):
        context = inspect_project(self.project)
        self.assertEqual(context["unity_version"], "6000.3.4f1")
        self.assertEqual(context["purrnet"]["version"], "1.25.0")
        self.assertEqual(context["purrdiction"]["version"], "1.3.7")
        self.assertEqual(context["purrdiction"]["lock_revision"], REVISION)
        self.assertEqual(context["purrnet"]["csharp_source_roots"], [f"Library/PackageCache/{CORE}@current"])

    def test_declarations_and_overloads(self):
        context = inspect_project(self.project)
        result = lookup_installed("PurrNet.NetworkManager.StartClient", context)
        self.assertEqual(result["status"], "declarations_found")
        rows = result["results"]
        self.assertEqual({row["signature"] for row in rows}, {"public void StartClient()", "public void StartClient(string address)"})
        self.assertEqual([row["line_start"] for row in rows], [3, 5])
        self.assertEqual([row["obsolete_attribute"] for row in rows], [False, True])
        self.assertEqual(rows[0]["namespace"], "PurrNet")
        self.assertEqual(rows[0]["package_version"], "1.25.0")
        self.assertEqual(lookup_installed("NetworkManager.Ready", context)["results"][0]["kind"], "event_field")
        self.assertEqual(lookup_installed("NetworkManager.Count", context)["results"][0]["kind"], "property")
        self.assertEqual(lookup_installed("SyncVar<T>", context)["results"][0]["generic_arity"], 1)
        self.assertEqual(lookup_installed("PredictedIdentity<INPUT, STATE>", context)["results"][0]["generic_arity"], 2)
        conditional = lookup_installed("NetworkManager.ConditionalCall", context)
        self.assertEqual(conditional["status"], "signature_unverified")
        self.assertIsNone(conditional["results"][0]["signature"])

    def test_missing_api_and_wrong_declaring_type(self):
        context = inspect_project(self.project)
        for symbol in ("NetworkManager.MissingMethod", "NetworkManager.Other", "SyncVar<T, U>"):
            with self.subTest(symbol=symbol):
                result = lookup_installed(symbol, context)
                self.assertEqual(result["status"], "not_found")
                self.assertEqual(result["results"], [])

    def test_search_product_scope_provenance_and_language_fallback(self):
        self.prepare_docs()
        context = inspect_project(self.project)
        result = search_docs(self.docs, "Comment mirroring est géré", "purrdiction", 5, context)
        self.assertEqual(result["commit"], COMMIT)
        gated = [row for row in result["results"] if row["version_conditions"]]
        self.assertEqual(len(gated), 2)
        for row in gated:
            self.assertEqual(row["path"], PAGE)
            self.assertEqual(row["section"], "Predicted Identity / Mirroring")
            self.assertIn(f"/blob/{COMMIT}/{PAGE}#L", row["url"])
            self.assertEqual(len(row["sha256"]), 64)
            self.assertLessEqual(len(row["excerpt"]), 550)
        self.assertEqual(search_docs(self.docs, "PredictedIdentitySpawner", "purrnet", 5, None)["results"], [])

    def test_version_gates_are_passage_scoped(self):
        self.prepare_docs()
        context = inspect_project(self.project)
        expected = {5: "verified_incompatible", 9: "verified_compatible", 13: "requires_source_inspection"}
        for line, status in expected.items():
            with self.subTest(line=line):
                verdict = lookup_document(self.docs, f"{PAGE}:{line}", context)
                self.assertEqual(verdict["status"], status)
                self.assertEqual(verdict["version"], "1.3.7")
        self.assertEqual(lookup_document(self.docs, PAGE, context)["status"], "requires_source_inspection")

    def test_floating_reference_without_version_is_unknown(self):
        self.prepare_docs()
        write(self.project, "Packages/packages-lock.json", {"dependencies": {}})
        (self.project / self.prediction / "package.json").unlink()
        context = inspect_project(self.project)
        self.assertIsNone(context["purrdiction"]["version"])
        self.assertIsNone(context["purrdiction"]["lock_revision"])
        self.assertEqual(context["purrdiction"]["requested_git_ref"], "release")
        self.assertEqual(lookup_document(self.docs, f"{PAGE}:5", context)["status"], "unknown")

    def test_git_lock_does_not_bless_a_conflicting_cache(self):
        old = self.project / self.prediction
        old.rename(old.with_name(f"{PREDICTION}@{'c' * 12}"))
        package = inspect_project(self.project)["purrdiction"]
        self.assertEqual(package["lock_revision"], REVISION)
        self.assertIsNone(package["version"])
        self.assertFalse(package["csharp_source_roots"])

    def test_git_cache_alone_does_not_resolve_floating_lock(self):
        write(self.project, "Packages/packages-lock.json", {
            "dependencies": {PREDICTION: {"version": "https://example.test/pkg#release", "source": "git"}},
        })
        package = inspect_project(self.project)["purrdiction"]
        self.assertIsNone(package["version"])
        self.assertEqual(package["active_source"]["version"], "1.3.7")

    def test_offline_index_survives_missing_checkout_and_inventory(self):
        self.prepare_docs()
        self.docs.rename(self.docs.with_name("unavailable"))
        (self.docs.parent / "docs-index.json").unlink()
        result = search_docs(self.docs, "mirroring", "all", 1, None)
        self.assertEqual(result["cache_status"], "snapshot_only")
        self.assertEqual(result["commit"], COMMIT)
        self.assertTrue(result["results"])

    def test_failed_rebuild_keeps_previous_commit(self):
        self.prepare_docs()
        inventory_path = self.docs.parent / "docs-index.json"
        inventory = json.loads(inventory_path.read_bytes())
        inventory["git_commit"] = "c" * 40
        write(self.docs.parent, "docs-index.json", inventory)
        write(self.docs, PAGE, MARKDOWN + "tampered")
        with self.assertRaisesRegex(CacheError, "hash mismatch"):
            build(self.docs)
        self.assertEqual(diagnose(self.docs)["status"], "stale")
        self.assertEqual(search_docs(self.docs, "mirroring", "all", 1, None)["commit"], COMMIT)
        write(self.docs, PAGE, MARKDOWN)
        self.assertEqual(build(self.docs)["commit"], "c" * 40)

    def test_missing_cache_is_actionable_and_read_only(self):
        with self.assertRaisesRegex(CacheError, "purrnet-expert-cache index"):
            search_docs(self.docs, "mirroring", "all", 1, None)
        self.assertFalse(database(self.docs).exists())

    def test_reject_project_allowlist_and_doc_path_traversal(self):
        with patch.dict(os.environ, {"PURRNET_PROJECT_ROOTS": str(self.root / "elsewhere")}):
            with self.assertRaisesRegex(ValueError, "outside PURRNET_PROJECT_ROOTS"):
                inspect_project(self.project)
        with self.assertRaises(ValueError):
            lookup_document(self.docs, "../private.md:1", {})

    def test_linked_csharp_file_is_not_read(self):
        outside = write(self.root, "secret.cs", "public class PrivateData {}")
        link = self.project / f"Library/PackageCache/{CORE}@current/PrivateData.cs"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("Symlink creation requires privileges on this platform")
        result = lookup_installed("PrivateData", inspect_project(self.project))
        self.assertEqual(result["status"], "not_found")

    def test_stdio_discovery_and_calls(self):
        self.prepare_docs()

        async def exercise():
            params = StdioServerParameters(
                command=sys.executable, args=["-m", "purrnet_expert_mcp.server"],
                cwd=str(self.root), env={"PURRNET_DOCS_DIR": str(self.docs), "PURRNET_PROJECT_ROOTS": str(self.root)},
            )
            with anyio.fail_after(25):
                async with stdio_client(params) as streams, ClientSession(*streams) as session:
                    await session.initialize()
                    tools = (await session.list_tools()).tools
                    self.assertEqual({tool.name for tool in tools}, {
                        "get_purrnet_project_context", "search_purrnet_docs", "get_purrnet_api", "check_purrnet_compatibility",
                    })
                    self.assertTrue(all(tool.annotations.read_only_hint for tool in tools))

                    async def call(name, **args):
                        result = await session.call_tool(name, args)
                        self.assertFalse(result.is_error, result.content)
                        return result.structured_content

                    project = str(self.project)
                    context = await call("get_purrnet_project_context", project=project)
                    self.assertEqual(context["purrdiction"]["version"], "1.3.7")
                    docs = await call("search_purrnet_docs", project=project, query="mirroring", product="purrdiction")
                    self.assertEqual(docs["commit"], COMMIT)
                    api = await call("get_purrnet_api", project=project, symbol="NetworkManager.StartClient")
                    self.assertEqual(len(api["results"]), 2)
                    gate = await call("check_purrnet_compatibility", project=project, reference=f"{PAGE}:5")
                    self.assertEqual(gate["status"], "verified_incompatible")

        anyio.run(exercise)


if __name__ == "__main__":
    unittest.main()
