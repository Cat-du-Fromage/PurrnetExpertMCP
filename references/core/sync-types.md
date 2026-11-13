# Sync Types and choice of mechanism

**Official sources**: `systems-and-modules/network-modules/sync-types/README.md` and its pages (`syncvar.md`, `validated-syncvar.md`, `synclist.md`, `syncdictionary.md`, `synclazyref.md`, `syncevent.md`, `synctimer.md`, `syncinput.md`, `synclist-1.md`, `synclist-1-1.md`, `synchashset.md`), `network-modules/owner-only.md`.

## Choose
- `SyncVar<T>`: replicated durable status, onChanged events, default server authority or explicit `ownerAuth`.
- `ValidatedSyncVar<T>`: Reactive change by owner with server validation and failure return; review `serverValidation`, `onValidationFail`, version and obsolete ACK cases.
- `SyncList`, `SyncDictionary`, `SyncArray`, `SyncQueue`, `SyncHashset`: synchronized collections; check serialization of elements, observation update and late join, memory cost/bandwidth.
- `SyncLazyRef`: synchronised reference (check resolution, disappearance and load); GameObject in SyncList is not equivalent to a serialized network identifier.
- `SyncEvent`: occurrence; does not replace a `SyncVar` for durable status.
- `SyncTimer`: synchronised and reconciled timer; distinguishing authority and resynchronization intervals.
- `SyncInput<T>`: input sent owner→server for server gameplay, alternative **simpler but more sensitive to latency** than client-side prediction; prefer to a RPC per frame if the design accepts the delay.

## ownershipOnly and ownership
`ownerOnly: true` actually filters the sending of a module to the owner, not only its rendering; the old owner ** retains its last local value after transfer**. If sensitive, purge/transform the status *before* change to own and control the privacy strategy. New owner receives the current state, non-owners do not receive the updates. `ownerOnly` fixed during the life of the module; `ownerAuth` allows the write owner but does not constitute a business validation.

**Module constraints**: fields/properties reported to the time compile; not `List<SyncVar<...>>`, not replaced after spawn, initialize in `OnInitializeModules`. See `network-modules.md`.

## Tests
Late join, ownership transfer, observation, client malveillant, spam, packet loss, changements de valeur rapides, payload volumineux.
