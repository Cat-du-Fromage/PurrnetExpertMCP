# Carte de routage de l'ENSEMBLE de PurrDocs

**Source of discovery**: complete repository `https://github.com/PurrNet/PurrDocs` and `SUMMARY.md`; local copy `references/cache/official-docs/`. During the review on 12-11-2026, the Git tree contains 217 `.md` (30 `client-side-prediction`, 70 `systems-and-modules`). The synchronization script **does not filter** pages and the search tool even includes files missing from SUMMARY. This file gives a starting path, not an exhaustive list of pages.

## Routing by need

| Need | Start pages in the PurrDocs clone | Other pages to discover |
| --- | --- | --- |
| Installation, versions, migration | `getting-started/installation-setup.md`, `getting-started/getting-started.md`, `getting-started/converting-to-purrnet/` | `readme/compatibility.md`, `api-documentation.md` |
| Authority/rules/ownership | `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-identity/ownership.md` | `terminology/`, `network-visibility/`, `client-spawning-validation.md` |
| NetworkManager, players and reconnect | `systems-and-modules/network-manager/README.md`, `network-manager/connection-and-player-events.md`, `network-identity/playeridentity.md` | `network-manager/authentication.md`, scene module, network assets |
| Spawn / pool / scenes / Addressables | `systems-and-modules/network-identity/spawning-and-despawning/README.md`, `systems-and-modules/network-identity/pooling.md`, `systems-and-modules/scene-module.md` | `systems-and-modules/addressables/`, `network-manager/scene-scoped-prefabs-and-assets.md` |
| Network Synchronised Modules and Types | `systems-and-modules/network-modules/common-pitfalls.md`, `systems-and-modules/network-modules/sync-types/` | `owner-only.md`, `syncbigdata/`, networking-custom-classes |
| RPC, broadcasts | `systems-and-modules/remote-procedure-call-rpc/README.md`, `systems-and-modules/broadcast.md` | `static-rpc.md`, `generic-rpc.md`, `awaitable-rpc.md`, `fully-local-rpc.md`, `pre-post-processors.md` |
| Serialization/perfs | `systems-and-modules/bitpacker-serialization/`, `systems-and-modules/bandwidth-profiler.md`, `systems-and-modules/code-stripping.md` | `readme/performance/`, network transform, scene assets |
| Transports & latence | `systems-and-modules/transports/`, `guides/test-with-friends/` | `game-server-hosting/`, `systems-and-modules/collider-rollback.md` |
| Components plug & play | `plug-n-play-components/` | Network Transform/Animator/Physics/Bones/Audio, state machine, adaptive sync |
| PurrDiction — bases | `client-side-prediction/overview.md`, `client-side-prediction/predicted-identities.md`, `client-side-prediction/installation.md` | `client-side-prediction/README.md` |
| PurrDiction — Best Practices | **`client-side-prediction/best-practices.md`** | **`input-handling.md`, `state-handling.md`, `flow.md`, `security.md`** |
| PurrDiction — Policies, view, rollback | `client-side-prediction/prediction-policies.md`, `client-side-prediction/views-and-interpolation.md` | `predicted-physics-callbacks.md`, `prediction-manager` search |
| PurrDiction — Objects & pooling | `client-side-prediction/predicted-hierarchy.md`, `client-side-prediction/predicted-object-references.md`, `client-side-prediction/disposable-collections.md` | `built-in-components/`, `predicted-visibility.md`, `predicted-parent.md` |
| PurrDiction — Modules | `client-side-prediction/predicted-modules/README.md` | `predicted-timer-module.md`, `predicted-state-machine/` |
| PurrDiction — Security & Combat | `client-side-prediction/security.md`, `client-side-prediction/lag-compensation.md` | `deterministic-identity.md`, `multi-identity-interactions.md` |
| Addons lobby/voix/UI | `tools/purrlobby/`, `tools/purrvoice-voice-chat/`, `addons/`, `integrations/` | Accurate GitHub addons projects installed |
| Real examples | `full-game-guides/`, `community-guides/` | example code `PurrNet-Incremental-Sample`, `PurrDiction` tests |

## Blocking pages for PurrDiction mode

The `docs_catalog.py coverage` test requires at least the following pages ** when a clone is present**:

`client-side-prediction/best-practices.md`, `input-handling.md`, `state-handling.md`, `security.md`, `flow.md`, `prediction-policies.md`, `views-and-interpolation.md`, `predicted-hierarchy.md`, `predicted-object-references.md`, `disposable-collections.md`, `deterministic-identity.md`, `predicted-modules/README.md`, `built-in-components/predicted-identity-spawner.md`, `built-in-components/predicted-physics-callbacks.md`, `lag-compensation.md`.

Also: `systems-and-modules/network-modules/common-pitfalls.md`, `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-modules/sync-types/syncvar.md`, `systems-and-modules/remote-procedure-call-rpc/README.md`, `systems-and-modules/network-identity/spawning-and-despawning/README.md`.

**Required procedure for functionality not listed here**: `docs_catalog.py search <feature>` then read the relevant pages under the complete clone; never deduce "undocumented" because this map does not list it. After sync, read all the pages that affect the code to be modified, not the 217 in the context at once.

## Control v0.9 — critical pages not to be used

After `sync_sources.py`, run `python scripts/doc_coverage_matrix.py --fail-missing-routed --fail-unrouted-critical`: the inventory report **all** the Markdown pages of the clone, signal unrouted ones and block if one of the critical pages listed in the script does not have a mandatory route. This control **does not guarantee reading or understanding** by the agent and does not replace the signatures actually installed. Marketing pages, showcase games and historical resources remain accessible by search and do not need to create a large mandatory guide.

Reinforced points: [spawning client and DDOL](core/spawn-security-and-persistence.md), [PlayerIdentity / SyncLazyRef](core/player-identity-and-lazy-refs.md), [visibility priority](core/visibility-priority.md), [ColliderRollback](core/collider-rollback-classic.md), [mirroring predicted](prediction/mirror-and-visibility.md), [input one-shot](prediction/one-shot-input-and-events.md), predictable interactions between identities.
