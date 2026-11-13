# Diagnostic PurrNet — decision tree

First ask/inspect: version and commit, host/dedicated model, transport,
Network Rules, prefab or scene, logs and reproduction steps.

## RPC does not arrive

1. Confirm that the object carrying a `NetworkIdentity` is spawned and
   Observable by the recipient.
2. Identify caller: server, client owner, client non owner, host.
3. Check `Network Rules` and the restrictions of RPC attributes of the version.
4. Confirm the direction (`ServerRpc`, `ObserversRpc`, `TargetRpc`) and channel.
5. Temporarily add roles, network identity and moment logs
   then test in a dedicated server + two clients.

## Double execution in host

`OnSpawned(bool asServer)` can be called server-side AND client-side in a
host. Do not automatically diagnose a duplication bug: check
role, `RunLocally` RPC and callback logic.

## Invisible, disappeared or duplicated object

1. Confirm registered prefab (Network Prefabs) or scene identity.
2. Control the spawn/despawn rules and visibility.
3. Check who calls `Instantiate()`/`Destroy()`, how many times,
   and stage model/late join.
4. Do not add `Spawn()` borrowed from Mirror without proof in PurrNet.

## Incorrect SyncVar or state

1. Check the write authority (server/owner) and the options (`ownerAuth`,
   `ownerOnly`) supported by version.
2. Check the actual serialization of the type.
3. Check the moment of subscription to events, initializations
   and network startup.
4. Test initial values, changes, and late arrival.

## Network references and serialization

Do not assume that `Transform` or `GameObject` are serialized directly.
See the current `BitPacker` code, network identifiers and type
The historical Quick Reference suggests `NetworkId` for some cases,
but confirm the current name/type and APIs.

## Transport / performances

Diagnosing latency, packet loss, payload sizes, RPC channels and
MTU limits documented. Adapt frequency and mode of transmission.
Do not recommend a transport or relay "production" on faith alone
of a reply Discord dated.

## Check a historical problem

First consult the official changelog of **installed version**:
https://github.com/PurrNet/PurrNet/blob/release/Assets/PurrNet/CHANGELOG.md
Then check the old FAQ:
https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md
Do not propose a "v1.2.1 fix" as if this bug were still present.
