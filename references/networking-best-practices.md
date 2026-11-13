# Classic PurrNet — technical and anti-pattern contract

Verified sources:
- https://purrnet.dev/docs/systems-and-modules/network-modules/common-pitfalls
- https://purrnet.dev/docs/systems-and-modules/network-manager/network-rules
- https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc
- https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncvar
- https://purrnet.dev/docs/systems-and-modules/network-identity/spawning-and-despawning

**Warning**: These recommendations are for the normal `NetworkIdentity` model. For `PredictedIdentity` read `purrdiction-best-practices.md` before using a type sync or RPC.

## Modules: mandatory documented rules

1. `NetworkModule`/`SyncVar`/`SyncList`/`SyncDictionary`/etc. are **fields or properties** of `NetworkIdentity`/`NetworkBehaviour` (or statically interlocked modules); no `List<SyncVar<T>>`, module arrays, dynamic intanciation as a module collection technique.
2. Set defaults in the constructor, declaration or `OnInitializeModules()` before network assignment. Keep the same module instance after spawn.
3. Imbracation possible, but **acyclic** (no module A→B→A). Serialization Inspector requires public or `[SerializeField]` depending on module.
4. Events `OnSpawned`, `OnOwnerChanged`, `OnDespawned` and subscriptions/unsubscribes follow their cycle; check exact package signature. Do not assume a unique host callback.
5. `ownerAuth`, `ownerOnly`, intervals, callbacks `onChanged`, advanced sync types: read **each** corresponding page and its restrictions, not a naive generalization to all modules.

## RPC / authority / events

- `[ServerRpc]`: client request→server; `[ObserversRpc]`: to observers; `[TargetRpc]`: to targeted `PlayerID`. Conditions (`RequireOwnership`, `RequireServer`, `RunLocally`, `BufferLast`, `Channel`, `CompressionLevel`, `MtuExceeded`, `Immediate`) vary by attribute; check signatures/version.
- RPC ** event** non-sustainable equivalent: for late join, persistent replicated state or suitable buffer solution. Do not assume that `BufferLast` reconstructs the entire history.
- `Network Rules` control spawn, despawn, property, visibility, call and sync permission; permission to call does not validate **** the interaction distance, money, damage or cooldowns. Client-owner/non-owner/server/host/dedicated case to test.
- Dedicated server 的 host: no local client; a `[ObserversRpc]` without `RunLocally` does not automatically launch its body on the server. For server initialization, prefer dedicated server branch or `RunLocally` justified; document the risks of dual execution host.

## Spawn, scene, visibility and references

- `Instantiate()` / `Destroy()` follow PurrNet rules for objects with `NetworkIdentity`, network prefab/scene and rights; check `NetworkManager`/Network Prefabs and visibility before diagnosis.
- Supported `NetworkId` or types serve as replicated references when a GameObject/Transform is not packageable as it is; inspect BitPacker real.
- Scene Management, Addressables, network visibility (distance/whitelist), owner-only data, scene-scoped assets, pooling and reconnection have separate pages. Check each subsystem used instead of assuming behavior identical to the NGO/Mirror model.
- Tester scene load/unload, player joining late, disconnection/reconnection and sleeping identities; own subscriptions.

## Transport, safety and performance

- Verify real protocol (UDP / WebTransport WS/WSS / Steam / composite), internal/external ports, WebGL scenarios and local network. `StartClient` can initially remain Disconnected before switching Connecting; avoid instant retrieving (see Edgegap).
- No secrets in clients or in the repository; authentication, rate limiting and validation of server actions. `Unsafe`/`Everyone` = prototyping tolerance, not security validation.
- Profile/BitPacker/Compression/MTU: limit repeated messages and payloads; choose channel according to semantics, not optimize without measurements.
- Respecting the PurrDiction borders: `NetworkIdentity` modules/objects may exist for chat/IU around a prefab predicted on compatible versions, **not** for its reconciled state.

## Review before PR

For each script: exact package + parent class + execution side + write authority + state/event type + late join regime + ownership + serialized references + test 2 clients + config inspector + source version.
