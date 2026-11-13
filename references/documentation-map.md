# Carte de routage de l'ENSEMBLE de PurrDocs

**Source de découverte** : dépôt complet `https://github.com/PurrNet/PurrDocs` et `SUMMARY.md`; copie locale `references/cache/official-docs/`. Lors de la revue le 12-11-2026, l'arbre Git contient 217 `.md` (30 `client-side-prediction`, 70 `systems-and-modules`). Le script de synchronisation **ne filtre pas** les pages et l'outil de recherche inclut même les fichiers absents de SUMMARY. Ce fichier donne un chemin de départ, pas une liste exhaustive des pages.

## Routage par besoin

| Besoin | Pages de départ dans le clone PurrDocs | Autres pages à découvrir |
| --- | --- | --- |
| Installation, versions, migration | `getting-started/installation-setup.md`, `getting-started/getting-started.md`, `getting-started/converting-to-purrnet/` | `readme/compatibility.md`, `api-documentation.md` |
| Authority/rules/ownership | `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-identity/ownership.md` | `terminology/`, `network-visibility/`, `client-spawning-validation.md` |
| NetworkManager, joueurs, reconnexion | `systems-and-modules/network-manager/README.md`, `network-manager/connection-and-player-events.md`, `network-identity/playeridentity.md` | `network-manager/authentication.md`, scene module, network assets |
| Spawn / pool / scenes / Addressables | `systems-and-modules/network-identity/spawning-and-despawning/README.md`, `systems-and-modules/network-identity/pooling.md`, `systems-and-modules/scene-module.md` | `systems-and-modules/addressables/`, `network-manager/scene-scoped-prefabs-and-assets.md` |
| Network Modules et types synchronisés | `systems-and-modules/network-modules/common-pitfalls.md`, `systems-and-modules/network-modules/sync-types/` | `owner-only.md`, `syncbigdata/`, networking-custom-classes |
| RPC, broadcasts | `systems-and-modules/remote-procedure-call-rpc/README.md`, `systems-and-modules/broadcast.md` | `static-rpc.md`, `generic-rpc.md`, `awaitable-rpc.md`, `fully-local-rpc.md`, `pre-post-processors.md` |
| Sérialisation/perfs | `systems-and-modules/bitpacker-serialization/`, `systems-and-modules/bandwidth-profiler.md`, `systems-and-modules/code-stripping.md` | `readme/performance/`, network transform, scene assets |
| Transports & latence | `systems-and-modules/transports/`, `guides/test-with-friends/` | `game-server-hosting/`, `systems-and-modules/collider-rollback.md` |
| Components plug & play | `plug-n-play-components/` | Network Transform/Animator/Physics/Bones/Audio, state machine, adaptive sync |
| PurrDiction — bases | `client-side-prediction/overview.md`, `client-side-prediction/predicted-identities.md`, `client-side-prediction/installation.md` | `client-side-prediction/README.md` |
| PurrDiction — Best Practices | **`client-side-prediction/best-practices.md`** | **`input-handling.md`, `state-handling.md`, `flow.md`, `security.md`** |
| PurrDiction — Policies, view, rollback | `client-side-prediction/prediction-policies.md`, `client-side-prediction/views-and-interpolation.md` | `predicted-physics-callbacks.md`, `prediction-manager` search |
| PurrDiction — Objects & pooling | `client-side-prediction/predicted-hierarchy.md`, `client-side-prediction/predicted-object-references.md`, `client-side-prediction/disposable-collections.md` | `built-in-components/`, `predicted-visibility.md`, `predicted-parent.md` |
| PurrDiction — Modules | `client-side-prediction/predicted-modules/README.md` | `predicted-timer-module.md`, `predicted-state-machine/` |
| PurrDiction — Sécurité & combat | `client-side-prediction/security.md`, `client-side-prediction/lag-compensation.md` | `deterministic-identity.md`, `multi-identity-interactions.md` |
| Addons lobby/voix/UI | `tools/purrlobby/`, `tools/purrvoice-voice-chat/`, `addons/`, `integrations/` | Projets addons GitHub exacts installés |
| Exemples réels | `full-game-guides/`, `community-guides/` | code exemple `PurrNet-Incremental-Sample`, `PurrDiction` tests |

## Pages bloquantes pour le mode PurrDiction

Le test `docs_catalog.py coverage` exige au moins la présence des pages ci-dessous **lorsqu'un clone est présent** :

`client-side-prediction/best-practices.md`, `input-handling.md`, `state-handling.md`, `security.md`, `flow.md`, `prediction-policies.md`, `views-and-interpolation.md`, `predicted-hierarchy.md`, `predicted-object-references.md`, `disposable-collections.md`, `deterministic-identity.md`, `predicted-modules/README.md`, `built-in-components/predicted-identity-spawner.md`, `built-in-components/predicted-physics-callbacks.md`, `lag-compensation.md`.

Également : `systems-and-modules/network-modules/common-pitfalls.md`, `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-modules/sync-types/syncvar.md`, `systems-and-modules/remote-procedure-call-rpc/README.md`, `systems-and-modules/network-identity/spawning-and-despawning/README.md`.

**Procédure obligatoire pour une fonctionnalité non citée ici** : `docs_catalog.py search <fonctionnalité>` puis lecture des pages pertinentes sous le clone complet ; ne jamais déduire « non documenté » parce que cette carte ne l'énumère pas. Après sync, lire toutes les pages qui touchent le code à modifier, pas les 217 dans le contexte d'un seul coup.

## Contrôle v0.9 — pages critiques à ne pas laisser sous-utilisées

Après `sync_sources.py`, lancer `python scripts/doc_coverage_matrix.py --fail-missing-routed --fail-unrouted-critical` : le rapport inventorie **toutes** les pages Markdown du clone, signale celles non routées et bloque si l'une des pages critiques listées dans le script n'a pas de route obligatoire. Ce contrôle **ne garantit pas la lecture ni la compréhension** par l'agent et ne remplace pas les signatures réellement installées. Les pages marketing, jeux vitrine et ressources historiques restent accessibles par recherche et n'ont pas besoin de créer un gros guide obligatoire.

Points renforcés : [spawning client et DDOL](core/spawn-security-and-persistence.md), [PlayerIdentity / SyncLazyRef](core/player-identity-and-lazy-refs.md), [visibility priority](core/visibility-priority.md), [ColliderRollback](core/collider-rollback-classic.md), [mirroring prédit](prediction/mirror-and-visibility.md), [input one-shot](prediction/one-shot-input-and-events.md), interactions prédictibles entre identités.
