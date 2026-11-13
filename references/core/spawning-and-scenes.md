# Spawning, prefabs, pooling, scenes, Addressables

**Official sources**: `systems-and-modules/network-identity/spawning-and-despawning/README.md`, `pooling.md`, `network-manager/network-prefabs.md`, `network-manager/scene-scoped-prefabs-and-assets.md`, `systems-and-modules/scene-module.md`, `systems-and-modules/addressables/README.md`, `addressable-spawning-and-despawning.md`, `addressable-scene-handling.md`.

- PurrNet classic supports `Instantiate`/`Destroy` objects with `NetworkIdentity` **if Network Rules allows** and if prefab/scene are saved according to configuration. Do not import `NetworkServer.Spawn()` from Mirror.
- Spawn/destroy server side: validate prefab, owner and data; an unobserved object is not necessarily destroyed on the server. Late join must rebuild the durable state by synchronization/scene, not by an ephemeral event.
- Different stage objects, itemized objects before starting, global prefabs, asset scope and scene scope. `Include Instantiated Scene Objects` is only sure if clients produce the same roots in the same order.
- For additive scenes: check who triggers loading/unloading, which NetworkManager operates, when clients are ready, and the behavior during reconnection. Do not assume that `SceneManager.LoadScene` local synchronizes the peer.
- Addressables: Check dedicated APIs for loading and RPC; do not guess signatures; test address errors and competing loads.
- Pooling: reset modules/effects/timers; child parts can be pooled separately and lose their references. See `Reference<>` documented in `pooling.md` when relevant.
- Subject matter **prescribed**: use `PredictedHierarchy`, `PredictedParent`, and specific rollback rules; do not apply the above recipe.

## Validation
Spawn/despawn in additive scene, late join, change of scene, loss of visibility, pool trouse, host + two clients + dedicated server.
