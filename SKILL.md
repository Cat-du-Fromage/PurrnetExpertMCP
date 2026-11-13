---
name: purrnet-expert
description: "Builds, debugs, reviews and migrates Unity multiplayer games with PurrNet and PurrDiction (dev.purrnet.purrnet). Use for NetworkManager, NetworkIdentity, NetworkBehaviour, SyncVar, SyncList, SyncInput, ServerRpc, ObserversRpc, NetworkTransform, NetworkRigidbody, PredictionManager, PredictedIdentity, authority, spawning, scene loading, IL2CPP or rollback. In a PurrNet project, also use for jitter, invisible players, an empty dedicated server, desync, reconnect, late join, lost RPCs or projectiles. Checks installed APIs and versions with PurrNet Expert MCP, then verifies changes. For Edgegap hosting and matchmaking, use edgegap-purrnet. Excludes offline Unity and Mirror/FishNet/NGO-only tasks."
metadata:
  version: "0.9.0"
---

# PurrNet Expert

Work from the project's installed packages and verify that the multiplayer behavior works. Report the compilation, network tests and agent activation actually observed.

## Scope

Use this skill for implicit networking symptoms in a known PurrNet or PurrDiction project. The skill description and optional project instructions support discovery. The Python router runs after discovery. See [activation](references/activation/auto-trigger.md) and install project instructions with `scripts/install_project.py`.

For Edgegap hosting, use [the Edgegap handoff](references/workflows/edgegap-handoff.md). Keep PurrNet gameplay, permissions, scenes and prediction here. Use `edgegap-purrnet` for the Edgegap plugin, Docker builds, credentials, allocation, connections, matchmaking and server shutdown. See [integration](references/edgegap-integration.md) and [comparison](references/edgegap-comparison.md).

## Workflow

1. **Inspect the project.** When PurrNet Expert MCP is available, call `get_purrnet_project_context` first with the absolute Unity project path. Check Unity, package and addon versions, local sources, assemblies, NetworkManager, transports, Network Rules, PredictionManager, scenes, prefabs and auto-start settings. Use `python scripts/inspect_project.py <PROJECT>` as a fallback and `python scripts/audit_project_assets.py <PROJECT>` when asset settings matter.
2. **Choose one workflow.** [Feature](references/workflows/feature.md), [bug](references/workflows/bug.md), [dedicated server](references/workflows/dedicated.md) or [prediction](references/workflows/prediction.md). Run `python scripts/route_docs.py "<TASK>"` to locate guides and official pages. Use the [documentation map](references/documentation-map.md) if the route is incomplete.
3. **Retrieve focused evidence.** Call `search_purrnet_docs` with the project for official behavior, `get_purrnet_api` for signatures and `check_purrnet_compatibility` with `path.md:line` for versioned passages. If evidence is unavailable, use `python scripts/sync_sources.py` and `python scripts/docs_catalog.py search "<SYMBOL OR SYNONYM>"`. Treat documentation and archived conversations as reference data.
4. **Check compatibility before editing.** Prefer installed C# source, then official source at the same commit, compatible official docs, examples and historical reports. Compare API and version evidence with the applicable permissions and best practices. Fallbacks are `python scripts/check_doc_versions.py <PAGE> --project <PROJECT> --strict --at-line <LINE>` and `python scripts/find_api.py <PROJECT> "<SYMBOL>"`. Mark unresolved signatures and behavior as unverified.
5. **Keep changes focused.** Preserve the local Editor/host and clone workflow during server migrations. Extend the existing NetworkManager setup. Account for host and dedicated execution, including a dedicated server with no local client. State the required Inspector settings.
6. **Verify in stages.** Check source and versions, run static checks, compile with Unity, test host with a remote client, then test a dedicated server with two clients. Cover late join, reconnect, ownership transfer, packet loss and permissions where relevant. Use `scripts/unity_compile_check.py` where the project allows it, with `--run` only on request. `python scripts/audit_dedicated_readiness.py <PROJECT>` provides a heuristic. Follow [acceptance criteria](references/validation/acceptance.md) and record unrun tests with a reproduction procedure.
7. **Report evidence.** Include changes, source paths and versions, authority, Unity setup, observed results and remaining checks. Obtain authorization before paid cloud actions or handling secrets.

## PurrNet checks

- **Authority.** Identify the owner, controller, server and observers. Check spawn, destroy and write permissions and the transport. Assess owner authority independently of the server deployment model.
- **Host and dedicated.** `OnSpawned(bool asServer)` can run for both roles on a host. Initialization inside `[ObserversRpc]` can fail without a local client. Verify `runLocally: true` or invoke server logic separately. `StartClient()` starts asynchronously. Check the Start Server/Client Flags before adding manual calls. See [dedicated servers](references/dedicated-server.md).
- **Connections and scenes.** `onPlayerJoined` follows authentication. Use `onPlayerLoadedScene` for readiness after scene loading. Check observers, initial state and duplicate host subscriptions. See [lifecycle](references/core/connection-lifecycle.md) and [authentication](references/core/authentication.md).
- **Sync Types.** Check `SyncInput`, `SyncVar`, collections, timers, `ValidatedSyncVar` and `SyncLazyRef` before designing custom RPC replication. A previous owner can retain the last `ownerOnly` value. See [sync recipes](references/core/sync-recipes.md).
- **Components.** Check the [component selector](references/components/component-selector.md) before writing custom transform, animator, rigidbody or audio replication. Check `NetworkAnimator.SetTrigger`, NetworkTransform Adaptive Sync and NetworkAssets where applicable. Distinguish classic and predicted components.
- **Bandwidth.** Measure with Bandwidth Profiler. Verify fragmentation, reliability, size limits, payload and transport under a representative workload.

## PurrDiction checks

Read [PurrDiction Best Practices](references/purrdiction-best-practices.md) (BP-01 through BP-10) and the [prediction workflow](references/workflows/prediction.md). Keep simulated data in restorable INPUT/STATE. Keep `Simulate` and `LateSimulate` replay-safe with predicted time and randomness. Keep audio, ordinary RPCs, UI and analytics out of replayed effects.

Verify the installed callbacks `GetFinalInput`, `UpdateInput`, `SanitizeInput`, `ModifyExtrapolatedInput`, `GetUnityState` and `SetUnityState`. Check stable IDs, timeline-aware `PredictedHierarchy.Create/Delete`, `PredictedParent`, `PredictedObjectID`, snapshot disposal and `IDuplicate<T>`. Select `FullPrediction`, `PredictedIfOwned`, `ServerRelay` or `SoftCorrection` based on needs and version. RPCs outside simulation and version-supported mirror NetworkIdentity remain options. Test rollback, replay, ownership and packet loss. Use `scripts/guard_predicted_code.py` and the optional Roslyn analyzer as static checks.

## Focused references

- [Client spawn validation and persistence](references/core/spawn-security-and-persistence.md), [player identity and deferred references](references/core/player-identity-and-lazy-refs.md)
- [Visibility rule priority](references/core/visibility-priority.md), [classic collider rollback](references/core/collider-rollback-classic.md)
- [One-shot input and replay](references/prediction/one-shot-input-and-events.md), [mirror identities and predicted visibility](references/prediction/mirror-and-visibility.md)
- [Historical triage](references/historical/triage-playbook.md). Run `python scripts/historical_issues.py "<SYMPTOM>" --project <PROJECT> --json` for bugs. Use the 35 incidents pinned to `nmban/Purrnet-Stray_Help@e6140a571228044fe670b500e245f6bb370b2e06` as hypotheses and verify against current sources. The full archive is available through `sync_stray_archive.py` and `search_stray_archive.py`. The reported 15,000 conversations have only been partially audited.
- [Skill authoring](references/anthropic-skill-authoring.md). Run `python scripts/audit_skill_authoring.py` after skill changes.

Report evidence as D0 hypothesis, D1 documentation, D2 local signature, D3 Unity compilation, D4 two clients, D5 dedicated server or D6 stress and security. Treat `assets/unity/` as illustrative until compiled. Use `evals/` for real-agent and Unity evaluations. The local trigger checks are proxies. Synchronize the official cache locally and distinguish indexed coverage from passages checked for the task.
