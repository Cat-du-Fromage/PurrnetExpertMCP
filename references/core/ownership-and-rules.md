# Authority, ownership and Network Rules

**Official source**: `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-identity/ownership.md`, `network-identity/spawning-and-despawning/client-spawning-validation.md`, `terminology/server-auth-safe.md`, `terminology/client-auth-everyone-unsafe.md`.

- Each mechanism must define initiator, authorized actor, validation, authoritative data and receivers. Being owner does not imply being allowed to do *all* transactions on children/identities.
- `Network Rules` influence spawn, despawn, ownership, RPC and synchronization. A `Everyone` or `Unsafe` rule accelerates prototyping but does not guarantee ** any anti-triche protection**; for economy/PvP, use server validation and restrictive permissions.
- `ServerRpc(RequireOwnership: false)` opens calls more widely; explicitly validate author and conditions. `RequireOwnership` and `RunLocally` options can overload rules: check the attribute actually installed.
- Spawns possible client according to rules: check and reject illegitimate prefabs/positions/ownership via the validation of spawning; do not trust a `NetworkIdentity` transmitted by the client.
- Change of ownership: processing initialization, observers, `ownerOnly` data, server-side cleaning and persistence. For `ownerOnly` see `sync-types.md`: the old owner retains its last value locally.
- PurrDiction policies regulate ** client timeline**, not the server authority; do not confuse them with `Network Rules`.

## Revue hostile
Non-owner client calls RPC, falsifies parameter, attempts to purchase negative, spawn a prefab not allowed, spammes several times the same message. Check dedicated server and host.
