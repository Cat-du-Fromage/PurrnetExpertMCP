# Version Policy and Conflict Resolution

Online doc and `dev` code can document an API missing from the
`release` or Unity installed.

## Version detection in the project

Run: `python scripts/inspect_project.py /chemin/vers/UnityProject`

In order, compare:

- `Packages/manifest.json` > `dependencies["dev.purrnet.purrnet"]` :
  direct reference (git URL, registry, local package, etc.).
- `Packages/packages-lock.json` > `dependencies["dev.purrnet.purrnet"]` :
  version and, if available, hash/revision locked.
- `Packages/dev.purrnet.purrnet/package.json` or
  `Library/PackageCache/dev.purrnet.purrnet@*/package.json` ;
  on board project Unity, `Assets/PurrNet/package.json`.
- `ProjectSettings/ProjectVersion.txt` for the exact version of Unity.

If only `#release` or `#dev` is available in the manifest, the reference
is **mobile**. Search for the committed solved in the lockfile; otherwise avoid
to announce a precise revision.

## Concrete case of outdated source

Verified on 2026-11-12: `PurrNet/PurrNet` branch `release`, file
`Assets/PurrNet/package.json`, announces `1.25.0`. The index Discord pinned by
user announces a history up to `v1.20.0` and some FAQs
employ the former owner `BlenMiner/PurrNet`.

Another contradiction: the Stray FAQ can say "no Dissonance integration",
but the organization maintains `PurrNet/PurrNet-Dissonance`, and `PurrDocs` contains
a `integrations/dissonance.md` page. A Discord answer has a date context.
Treat an archived diagnosis as a hypothesis and check it against current evidence.

## What to make visible to the user

- API confirmed in project: **Checked (local package)**.
- Confirmed only in an official commit: **Checked (commit/branche)**.
- Mentioned only in docs: **Documented, not compiled here**.
- From a FAQ or message: **History / to be confirmed**.
- Without source: **Hypothesis**, do not invent API.

Keep source: file/repo, URL, commit or version where possible,
consultation date, and branch restriction. In case of conflict,
prime the **exact** code used by Unity.

## Update v0.3 — independent addons and changes PurrDiction

The resolution **must be done by package**: `dev.purrnet.purrnet` (core), `dev.purrnet.purrdiction` (prediction), and any other `dev.purrnet.*` detected. `scripts/inspect_project.py` now returns `packages[]` with `manifest_spec`, `lock_hash` and `local_packages` for each. A project with recent core can install an older addon; the docs of the `PurrDocs/main` branch must not replace the installed C# source.

Versioned cases identified in official documents:
- **PurrDiction < 1.4.0**: old architecture for integration of `NetworkIdentity` into predicted prefabs and input diagnostics; follow the exact doc/version.
- **PurrDiction >= 1.4.0**: automatic mirroring of `NetworkIdentity` in predicted prefabs, `PredictedIdentitySpawner` obsolete; some pages of lag compensation marked >= 1.4.0; `PredictedIfOwnedWithSoftFallback` appears in the recent doc. Do not infer the presence of any API without `find_api.py` and package installed.
- Official docs are a mobile repository (capturer SHA Git); the old Stray Help messages are **not normative** and may contradict the current doc.

## Update v0.4.0 — explicit gate check

Run `scripts/check_doc_versions.py <page relative> --project <UnityProject> --strict` to obtain, by section `{% version range="..." %}` and frontmatter `version`, the applicable / excluded / unknown status according to **version PurrDiction or installed core**. This script does not automatically filter the doc and does not replace control of methods and attributes in the actually compiled C# code.

During a refresh Git docs, `scripts/sync_sources.py` preserves `references/cache/docs-index.previous.json`. `scripts/docs_drift.py` lists the changes and guides to check via roads. An unmapped page is never considered to be automatically covered; it requires classification. The old guides remain to be reviewed until human review/change agent.

## v0.7 — version of the historical bugs, API compatibility version

`python scripts/historical_issues.py "double RPC" --project <UnityProject>` compares the resolved version with the **reported historical fix**. The `older_than_claimed_fix` and `at_or_after_claimed_fix` statuses give version context. Check the actual cause independently. `PREDICTION_*` uses the PurrDiction version and other incidents use the PurrNet core version. Conflicts between `packages-lock.json` and the installed package return `CONFLICTING` and disable comparison.

Never use the `1.20.0` historical milestone as the "current version" automatically. Always read the solved Unity package; the core `release` observed on November 13, 2026 announced `1.25.0`, but this is only a dated observation.
