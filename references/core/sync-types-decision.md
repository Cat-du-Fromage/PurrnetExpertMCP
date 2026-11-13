# Sync Types: how to choose, validate and test

Official family: `systems-and-modules/network-modules/sync-types/` (SyncVar, Validated SyncVar, SyncList, SyncArray, SyncQueue, SyncDictionary, SyncHashset, SyncTimer, SyncEvent, SyncLazyRef, SyncInput) and `network-modules/owner-only.md`.

| Need | Candidate | Mandatory caveat |
|---|---|---|
| One persistent value (HP, score, phase) | `SyncVar<T>` | Server/ownerAuth and observers, late join initial value; onChanged subscription lifetime |
| Client responsiveness with server approval | `ValidatedSyncVar<T>` | Server callback must validate game rules; rejection and stale ACK behavior |
| Ordered dynamic collection | `SyncList<T>` | Serialization of element type; avoid raw GameObject and check NetworkId/reference strategy |
| Indexed fixed-size data | `SyncArray<T>` | Verify resize semantics and version |
| Worklist / FIFO | `SyncQueue<T>` | Select only if queue semantics match protocol |
| Key→value / sets | `SyncDictionary` / `SyncHashset` | Serializer/key equality, mutation events, catchup |
| One-off message | `SyncEvent<T>` | Event != durable state; late join does not imply replay of all events |
| Countdown | `SyncTimer` | Reconciliation frequency/bandwidth tradeoff, controller authority |
| Deferred object reference | `SyncLazyRef` | Resolution delayed until referenced object exists; avoid live GameObject in unsupported containers |
| Input→server, no client prediction | `SyncInput<T>` | Simple authoritative movement at cost of input latency; compare with PurrDiction |
| Owner-private module | `ownerOnly` | New owner catchup; old owner retains stale copy, not automatically purged |

General: modules are declared fields/properties and cannot be replaced after spawn; `OnInitializeModules` is initialization point. Never hold modules inside `List<SyncVar<T>>` as a replacement for collection sync types. Mutating fields directly is not equivalent to changing the module's `.value`.

For each use: identify controller, authorization rule, validation, rate, events and clean unsubscription, serialization, initial snapshot for late join, observer visibility, old-owner purge, disconnect/reconnect, malicious owner, packet loss.

Runtime APIs and constructor parameters vary by package version; read corresponding official page and source, don't assume this table defines signatures.
