# Security model: authentication → PlayerID → observer → authority

Official: `systems-and-modules/network-manager/{authentication.md,connection-and-player-events.md,network-rules.md,network-visibility/README.md}`, `network-modules/owner-only.md`, `client-side-prediction/security.md`.

- Transport Connected is not authenticated; `onPlayerJoined` comes after auth. Before auth, a connection has no PlayerID or player-scoped RPCs/broadcasts. Custom `AuthenticationBehaviour<T>` and typed denial extension require declared payloads; register `AuthenticationRequest<T>` in game assembly when documented.
- Validate tokens or passwords **server-side**. Do not leak backend API credentials into client, logs, scenes or serialized assets; rate limit and handle timeouts/denials.
- Network Rules determine rights to spawn, despawn, own, observe and call methods. `Everyone` may be useful for prototypes, but cannot be assumed secure for public competitive games. Security is an ongoing server-state check, not an attribute spelling.
- `ownerOnly` only controls send target; old owner still retains prior memory on owner transfer. Private data must be explicitly invalidated/cleared before transfer if privacy requires it. A visibility rule is **not** a substitute for authorization.
- Classic visibility rules combine as OR (any allow succeeds), with owner and blacklist/whitelist exceptions; test unintended disclosure. PredictedVisibility is a **separate** PurrDiction mechanism for predicted hierarchy objects.
- Malicious packets can be correctly shaped; `SanitizeInput` normalizes ranges, but server must validate cooldown, energy, ownership, interaction distance and spawn rate using authoritative state.

Minimum verification: invalid login denied, authenticated PlayerID is created exactly once, host server/client branches not conflated, stolen ownership request denied, private state stays private on join/transfer, late join and reconnect behavior proven.
