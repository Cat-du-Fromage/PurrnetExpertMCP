# Case studies: symptom → test that separates causes

Each example is a **protocol**, not a common bug report. Official version and local signature remain mandatory.

## Case A — "My RPC run twice on the host"

**Archives**: Stray `QUICK_REFERENCE` notes a fix `ObserversRpc(runLocally: true)` to v1.2.0 and changelog from other RPC hosts.

- Three hypotheses: (1) old bug on actually previous package; (2) code invoked once for client AND once server on host; (3) two calls to RPC, or two NetworkManagers.
- Trace log to *invocation* and *at execution*. For a `NetworkBehaviour` with `OnSpawned(bool asServer)`, check both paths; trace `runLocally` and recipient; check that the required server effects are not only in a client-side ObserversRpc.
- Test: same host code + dedicated + two clients. **Never** remove `runLocally` without checking whether the dedicated depends on the method: the world could become empty.
- Validation: method called for good recipients; authoritative status does not depend on a local client.

## Case B — "A new client joins but his inventory is empty"

**Archive**: historical note v1.5.0 SyncList late join, more corrective SyncVar/collections up to v1.20.0.

- Capture the server content **before** the join, owner, `ownerOnly`, writing authority, serialized types, existence of the object on observation and loading of the scene.
- Discriminant test: client owner vs client non-owner; client arrived before/after spawn; `ownerOnly` must hide the data from the non-owner; `OnObserverAdded`/snapshot must serve the authorized recipient.
- For change of ownership: the former owner may **reserve the last value seen locally** — the secret must be cleaned before transfer if necessary; do not assume any automatic purging on the old owner side.
- Validation: correct inventory for new owner, no disclosure to third party, no old condition after pooling.

## Case C — "The spawne player in a bad scene / RPC received before stage"

**Archive**: spawner-scene v1.3.3, buffered RPC too early v1.9.3, broader revision 1.20.0.

- Separate: scene affiliation (`onPlayerJoinedScene`), **loaded scene** (`onPlayerLoadedScene`), object observation (`OnObserverAdded`) and first data from spawn.
- Check NetworkScenePrefabs and NetworkSceneAssets, instantization scene, Build Settings, and global priority registry.
- Avoiding a "magic" `WaitForSeconds`: prefer readiness event, a durable state or the inclusion of data from the spawn via `OnSerialize`/`OnDeserialize` if the installed API allows.
- Validation: two clients with scenes loaded in different orders, late join, unload/reload, client without hidden object.

## Case D — "My player trembles: WebTransport, NetworkRigidbody, NetworkTransform"

**Archive**: WebTransport/NetworkTransform fix 1.2.1; non-controller update 1.10.2; rework 1.20.0.

- Distinguish from *prediction* PurrDiction: if `PredictedTransform`, load `prediction/best-practices.md`, not just `NetworkTransform` classic.
- Mesurer : writer owner/server, double writer (`NetworkTransform`, Rigidbody/CharacterController), buffers/jitter, packet loss, transport WebSocket vs UDP, update phase, payload MTU.
- Test: an object moving in a straight line, then changing parent, teleport and change owner; compare host, remote, WebGL.
- Validation: correction rate/jumps, remote accuracy after late join and reconnection; profiler recorded.

## Case E — "New plugins/compilations don't work: Steam CS1061, GetClientPayload, IL2CPP"

**Archive**: FAQ offers a restart for SteamWorks CS1061; changelog 1.13.2 renames an auth override and 1.19.1 notes build patches.

- Capture **text and location** of error C#/ILPP, version Unity, asmdefs, packages, backend Mono/IL2CPP; do not choose a remedy by exception name alone.
- In an authenticator, `GetClientPayload` replaces an old `GetClientPlayload` typo from a historical revision: control the signature of the really solved class.
- A Unity/Hub restart can refresh the Steamworks import, but does not repair an absent API or an adversarial package version.
- Validation: compilation Editor + build target, runtime loading, function test after compilation.

## Case F — "A predicted ball appears and then disappears"

**Archive**: PurrDiction has hierarchy, pooling and input fixeds in the v1.2.x–v1.3.x period, but this is not an automatic explanation of any despawn.

- Verify that the spawn is requested via `INPUT`, executed in `Simulate` and confirmed by **server simulation**; a click Unity/IU without simulation can create a purely speculative object.
- Provide `STATE` restoreable, `PredictedObjectID`, `PredictedHierarchy`, one-shot extrapolation, policy and deterministic trajectory.
- Check the NetworkIdentity mirror components according to the separate PurrDiction version of PurrNet.
- Validation: host, remote client, loss/jitter, late join, spawn/replay/delete, and collision during rollback.
