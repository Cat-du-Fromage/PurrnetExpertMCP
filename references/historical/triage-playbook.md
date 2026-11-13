# Historical Incident-guided Debugging — protocol v0.7

**Activation**: any PurrNet bug request (RPC missing/double, `SyncVar` empty, ghost or duplicated object, ILPP error, WebGL jitter, change of owner, late join, stage problem, SteamWorks, etc.) MUST load this guide and `tools/troubleshooting-playbook.md`. Never load all 15k messages in context.

## 0. The symptom is not evidence of cause

Distinguer au minimum :

- **Bug corrected history**: the changelog archive reports a correction **in a given version**; this does not prove a bug in a modern version, nor does it prove a guaranteed fix.
- **Modern regression**: The same symptom reappears despite a more recent version; it requires a new minimal scenario, a precise commit and logs.
- **Usage/Configuration**: API not enabled, different host role, bad owner, unspawned or invisible object, scene not yet loaded, bad transport, missing packer.
- **Planned behavior**: `isOwner` can be false to destruction, server/client callbacks can coexist in host, input prediction can replay a simulation.
- **Expired tip**: old URL, old callback name, renowned component, backend/product that has evolved.

Do not declare "you need to update" only because a case looks like an archive note. Security/authority validations remain mandatory even if the archive says `Fixed`.

## 1. Order of evidence to be collected

1. `ProjectSettings/ProjectVersion.txt`, `Packages/packages-lock.json` and `package.json` package actually solved, `manifest.json`, `git hash`, `.asmdef`; PurrNet and PurrDiction are **two different versions**.
2. Mode **host / remote client / Linux Dedicated**; `NetworkManager` auto-start flags, number of instances/clients, transport and Network Rules.
3. Exact function, identity type, `asServer`, `isOwner`, owner `PlayerID`, `NetworkID`, scene, observation, tick/time stamping and error stack.
4. Result of minimal reproduction at the same commit, then comparison host vs dedicated and before/after degraded network.
5. `python scripts/historical_issues.py 'symptom' --project <PROJECT> --json`; for a particular Discord response, possibly sync the archive to the fixed revision and look for **a few extracts with context**, not a big dump.
6. Search the local source code and doc PurrDocs for current ** signatures and mechanisms**. For `>=1.4.0` blocks of PurrDiction, use the versions of the *package PurrDiction* only.
7. Formulate: (a) archive hypothesis, (b) observed evidence, (c) discriminant test, (d) limited fix, (e) tested regression.

## 2. Diagnostic matrix to apply

| Symptom | Useful historical hypothesis | Test discriminant **actuel** | Do not do |
|---|---|---|---|
| RPC `runLocally:true` deux fois | Fix 1.2.0; autre correction host 1.8.0 | trace call *and* execution with `asServer`, owner, version and destination | recommend a new update 1.2.0 without proof |
| Host creates duplicate players | old fix 1.2.1 | trace each `Instantiate`, self-start, clone, scene and `OnSpawned(bool)` | add a non-replicated client bool to hide duplication |
| `SyncVar<T>` null | fix 1.2.3 | stack + type `T` + `OnInitializeModules` + spam script | replace module after spawn |
| `SyncDictionary` illisible | improvements 1.3.2 / 1.19.0 | K/V serializer, change via sync API, snapshot late join | convertir silencieusement tout en RPC |
| Liste vide au late join | fix 1.5.0 | server-side content, view, `ownerOnly`, scene loaded | force a non-buffered RPC without durable status |
| Object appears in bad scene | fix PlayerSpawner 1.3.3 | spawner source scene, records and scenes actually loaded | create all prefabs in the DDOL scene |
| Character jitters on WebGL | fix WebTransport 1.2.1 | compare UDP and WebSocket, authority, NetworkTransform buffer, controller, RTT | conclude that WebTransport is still defective |
| Host `OnTick` deux fois | old fix 1.5.0 | trace tick, manager, contexts and subscriptions | confused with `OnSpawned(bool asServer)` two contexts |
| `isOwner` fake in OnDespawn | expected | Memorize owner during the life of the object and trace the lifecycle order | automatically declare a bug framework |
| `GetClientPlayload` does not compile | renommage 1.13.2 | inspection signature actuelle `GetClientPayload` | copy old Discord code without checking overrides |
| RPC buffered does not arrive | fix 1.9.3 / 1.20.0 | check visibility+spawn+TargetRpc, delivery channel, `bufferLast`/target | assuming that a RPC replaces a persistent state |
| `NetworkTransform` blocked on watch | fix 1.10.2 | check controller, writer, interpolation, update phase | add a second component that writes the transform |
| Reconnect/pooling: old condition | changelog 1.20.0 | `OnPoolReset`, `OnSpawned`, modules, ownerOnly, snapshot | Presuming a bug v1.20 still active |
| IL2CPP and build release fail | changelog 1.19.1 | `link.xml`, stripping, asmdef, codegen, target, vrai log | remove any security to have compiled |
| MTU trop grand / pertes | changelog 1.20.0 | size and channel, fragment loss vs corruption, Bandwidth Profiler | choose a universal fixed MTU |
| Spawn predicted then disappeared | PurrDiction archive 1.3.3 (divers correctifs) | actual prediction in `Simulate`, `INPUT` validated server, state, policy | traiter PurrDiction 1.3.3 comme PurrNet core 1.3.3 |

## 3. Example of host / late join tracks

For a *classical* network behavior: log "event, instance, tick, asServer, isOwner, localPlayer, owner, ID, scene, observeCount". Run even build as a host, as a separate client and on dedicated. If there is no tick accessible from the script, use a Unity time stamp, **without inventing** a tick API. Identifiers may have different callbacks on server/client.

For `onPlayerJoined`, see the current `connection-and-player-events.md` doc: **after authentication**, not "ready scene". Waiting `onPlayerLoadedScene` on the server. `onPlayerJoinedScene` remains useful for membership and is not proof that the loaded GameObjects are ready. Events are not replayed at subscription: see `networkManager.players` if subscription arrives late.

## 4. Responses and priority

A `incident-catalog.json` output has `historical_source`, `claimed_fixed_in`, `official_docs`, `verify`. The status compared to the version (`older_than_claimed_fix`, `at_or_after_claimed_fix`, `unknown_version`) is **a sort signal**, not an automatic update decision. Check a current changelog of the project commit and official pages as a priority. Never turn the historical description of a corrected bug into an instruction to change the production logic.
