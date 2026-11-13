# Unity scenes, prefabs and network assets — playbook

**Docs** : [Network Assets](https://purrnet.dev/docs/systems-and-modules/network-manager/network-assets), [Scene Scoped](https://purrnet.dev/docs/systems-and-modules/network-manager/scene-scoped-prefabs-and-assets), [Scene Module](https://purrnet.dev/docs/systems-and-modules/scene-module), [Addressables](https://purrnet.dev/docs/systems-and-modules/addressables), [Connection/Player Events](https://purrnet.dev/docs/systems-and-modules/network-manager/connection-and-player-events).

## 1. Table de diagnostic

| Symptom | To be inspected |
|---|---|
| Client connected but does not see prefab | NetworkIdentity, registry, Network Rules, visibility, scene loaded |
| The new player has no world | onPlayerLoadedScene, observation, durable condition, snapshots, scene actually present |
| Instantiation works in Editor but not build | asset included, Addressables catalog, build settings scene, registry resolution |
| The same prefab exists twice | host/server `asServer`, spawn path, auto-start flags, startup idempotent |
| Perf memory degrades at each scene | registre global trop large, `NetworkScenePrefabs/NetworkSceneAssets`, pooling |

## 2. Checklist Inspector

1. In the boot scene: `NetworkManager`, transport, spawn/authority rules, `NetworkPrefabs`/`NetworkAssets` records depending on the game.
2. In a non-global gameplay scene: create its ScriptableRegistry objects with `Folder / Scene` defined on this scene; place `NetworkScenePrefabs` and `NetworkSceneAssets` in a GameObject of this scene.
3. Avoid duplicates with global registry: global wins. Objects must be created in **the scene that owns the registry**; otherwise fallback on other scene and risks for clients who have not loaded it.
4. Load the network scene **before** assume that all players receive the object, check the `onPlayerLoadedScene`/`onPlayerUnloadedScene` events and visibility.
5. Addressables: save Addressables prefabs and take into account asynchronous character for spawn, RPC and scene; test slow loading, cancellation, cleanup/release on clients and server.

## 3. Timing and callbacks

- Transport `Connected` is prior to auth and allocation of a `PlayerID`.
- `onPlayerJoined` is called **after** authentication, but not necessarily after all scenes.
- Callbacks with `asServer` run for server and host client: keep server control in the `asServer` branch.
- `OnObserverAdded` / `OnObserverRemoved` are server-side and allow to produce a targeted state. Never use their only occurrence for the global durable state.
- Objects may exist on the server without being visible by a client, due to rules or scene.

## 4. Tests obligatoires

Host + clone / two client / late client build, joins with cookie, additive loading in a different order, a load of a scene under observation, connection that fails during loading, prefab of the register scene-only, destruction + respawn pool, serialization of a dynamic asset (e.g. AudioClip).
