# Indicative Timeline of Stray Deposit — DO NOT use as a "last" guide

Source **archived only**: `docs/changelogs/versions.md` to `e6140a571228044fe670b500e245f6bb370b2e06`. The dates and versions below are **marks to investigate**, not proof that the correction exists or works in the current package.

| PurrNet Core version mentioned | Incident/functionality of the time | Question de diagnostic actuel |
|---|---|---|
| 1.2.0 | RPC `runLocally` en host, SteamWorks | Is it a double-context callback rather than a double RPC? |
| 1.2.1 | duplicate spawns, ownership host, WebTransport/transform | Spawn script executed twice ? another writer ? |
| 1.2.3 | `SyncVar<T>` nullable, NetworkReflection host | When do the modules start? What serialization? |
| 1.3.2 | BitPacker arrays / SyncDictionary | Is the current serializer configured correctly? |
| 1.3.3 | scenes, PlayerSpawner, callback owner during despawn, NetworkAnimator excluded from hashes | Scene loaded vs member ? `isOwner` value expected ? |
| 1.5.0 | late join lists, double tick, events | Server state, observe, subscription and host? |
| 1.8.0/1.8.2 | RPC host, Collider Rollback, EvaluateVisibility | Channel contracts, re-evaluation of the rules? |
| 1.9.3 | buffered RPC premature | Does the recipient already observe the NetworkIdentity? |
| 1.10.2 | NetworkTransform non-controller | Who writes the transform? |
| 1.13.2 | `GetClientPlayload` renowned `GetClientPayload`, types & ILPP | Does the override exist in the installed version? |
| 1.17.0/1.18.0 | ValidatedSyncVar, SyncBigData, server TargetRpc | What does the resolved source support, which direction RPC? |
| 1.19.1 | IL2CPP/build/stripping | Compile with the right backend and target. |
| 1.20.0 | RPC, transform/rigidbody, packages, scenes, asset, ownership, reconnect | Several historical fixes do not show a current bug. |

**PurrDiction: independent versioning**. The archive mentions milestones 1.2.3 and 1.3.3 in 2026 (input disposal, replay, hierarchy, policies, visibility). `>=1.4.0` features documented on PurrDocs **must not be assigned** to PurrDiction 1.3.3 on the pretext that PurrNet core 1.20 exists.

The old `BlenMiner/PurrNet` URLs, the denial of a Dissonance integration, and the "last versions" dated from the archive are not normative. In case of exception, take the `package.json` actually installed and the official release notes of its commit.
