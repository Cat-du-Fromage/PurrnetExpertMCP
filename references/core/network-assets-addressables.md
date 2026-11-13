# Registries, scene-scoped assets, Addressables

Official: `systems-and-modules/network-manager/network-prefabs.md`, `network-assets.md`, `scene-scoped-prefabs-and-assets.md`, `systems-and-modules/addressables/{README.md,addressable-spawning-and-despawning.md,addressable-scene-handling.md,addressable-rpcs.md}`.

- `NetworkPrefabs` identifies spawnable prefab assets across peers; registration/configuration matters even though code calls Unity `Instantiate/Destroy`.
- `NetworkAssets` is an **optional** cross-peer asset reference registry. Ensure dynamic `AudioClip`, ScriptableObject or other referenced assets are actually in registry; regenerate type lists after adding types.
- For scene-only assets, use `NetworkScenePrefabs` and `NetworkSceneAssets` MonoBehaviours and scene-specific registries. Avoid duplicate global registration: global wins. Global → active scene → other loaded scene fallback; the last path can warn because remote peers may not have that other scene.
- Spawn into the right scene; use registries that load and unload with the scene. Test additive scenes, late join and scene unload. Scene-local IDs are not a substitute for synchronization of scene membership.
- Addressables: read all three topical docs; validate `AddressableNetworkPrefabs`, async lifetime, cancellation, prefab registration and `Addressables.ReleaseInstance` semantics. Do not assume direct `Addressables.InstantiateAsync` and ordinary instantiate are interchangeable across installed branches.
- Include Inspector walkthrough in deliverable: NetworkManager slots, generated lists, scene registries, additive load order and build profiles.
