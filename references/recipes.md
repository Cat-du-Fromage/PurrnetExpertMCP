# Operational revenue — PurrNet Expert

Purpose of each recipe: **result definition → inspection → implementation → verification**. Source paths are listed in `source-map.md`.

## A. Implementing a multiplayer feature (inventory, health, loot, doors)

**Definition of result:** two clients see the same status; invalid client entries do not modify the server; late join conforms to the need.

1. Inspect the existing Unity component, owner / `NetworkIdentity`, network rules, transport and package version.
2. Distinguish **intent** client → RPC to server, **validation/state** server-side, **sustainable replication** by `SyncVar` or adapted collection, and **cosmetic** via views/RPC.
3. Check in the local code the `SyncVar<T>`, its initialization, the `RPC` and their permissions; check the serialization of payloads.
4. Implement by isolating gameplay logic: the validation of distance, cooldown, inventory and settings is done on the server.
5. Tester owner / non-owner, host, two clients, join and RPC poorly trained. An unauthorized client must be rejected.

**Classical failure:** Copy a Mirror pattern that partially compiles but bypasses Network Rules, or send arbitrary `GameObject` to RPC.

## B. Debug RPC or SyncVar that "does not work"

**Result:** replicated cause, localized correction, same test scenario.

1. Raise the precise version, log calling side and receiver side, spam object, owner, transport, and rules.
2. Search in `references/troubleshooting.md`; if historical, check the context/version of the fix.
3. For RPC: check client/server sense, permissions, attribute, payload serializable, object spawned, observers, and host/dedicated.
4. For SyncVar: check writing authority, initialized module, observation, read vs modification and late join.
5. Change only one cause at a time; test before/after with journal/visual counter.

## C. Convertir un code solo en multijoueur

**Result:** gameplay separated in intent, authoritative logic, observable and rendered state.

1. Identify what needs to be shared and what remains local (input, camera, UI, VFX non-critical).
2. Preserving existing gameplay APIs where possible; isolating network input points.
3. Avoid synchronizing the status at each frame if an event or SyncType is enough.
4. Test non-owner clients, desynchronization, scene change and reconnection.

## D. Switching from a host to a dedicated server

**Result:** a headless process creates the world without a local client; two clients play; server shut down.

1. Inspect start flags, transport, port, `isHost`, client-only scripts, `[ObserversRpc]` world creation.
2. Correct host dependencies (`isServer`, `OnSpawned(asServer)`, `runLocally` targeted) by respecting the PurrNet version.
3. Test **local first**, headless server + 2 clients; then transport/infra; then matchmaking, separately.
4. Do not confuse internal listening port with external port of a hoster.

Read `dedicated-server.md`. For Edgegap, load `edgegap-purrnet` when installed.

## E. PurrDiction and movement

**Result:** local reactive commands, coherent server status, interpolated visuals, rollback without side effects.

1. Confirm that **PurrDiction is installed** and raise its version; it is an addon, not necessarily included with the heart PurrNet.
2. Read `PurrDocs/client-side-prediction/overview.md`, `input-handling.md`, `state-handling.md`, `flow.md` and local signatures.
3. Separate input/simulate/state/views. Non-deterministic and audio/particle effects should not be triggered uncontrolledly in a replayed simulation.
4. Test in simulated latency, remote client, join; compare the position server and render.

## F. Migrant from Mirror, NGO or FishNet

**Result:** feature migrated with *same functional rules*, and not a mechanical translation of names.

1. Identify commands/RPC/network variables/lifecycle/ownership/spawning of the old netcode.
2. Map to PurrNet mechanisms **by searching for local signatures**, page `getting-started/converting-to-purrnet/` of the official documentation.
3. Convert a vertical slice then compile; remove old packages only once their use is eliminated.
4. Test authority, network, serialization and late join; check that specific transport uses remain compatible.

## Hand-off model

- Accurate environment and level of evidence.
- Files modified and reasons.
- Scene/prefab/NetworkManager/Network Rules to configure.
- Tests performed: order and result. Tests still to be carried out: precise step + expected success.
- Source URL/revision, unverified areas and security choice.

## Imperative recipe: gameplay PurrDiction (v0.3)

1. Detect PurrDiction exact via `inspect_project.py`; if absent, do not invent types as if they were installed.
2. Read the 10 BP (`purrdiction-best-practices.md`) and documentation `best-practices.md`, `input-handling.md`, `state-handling.md`, `flow.md`, `security.md` and the feature page.
3. Write an INPUT table (intentions), STATE (everything that affects future ticks), deterministic simulation, Unity bridges, view, one-shot events, ownership and policy.
4. Check `PredictedModule` vs `NetworkModule`, predicted hierarchy and IDs; if `NetworkIdentity` coexists, use the versioned rule >=1.4.0 or the historical alternative.
5. Set up `purrdiction-test-matrix.md` tests, linter advisory and compilation/network if possible. Deliver BP-01 grid..BP-10 with OK/N/A/Unverified.
