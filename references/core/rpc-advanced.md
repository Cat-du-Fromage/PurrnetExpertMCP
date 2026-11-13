# RPC and Broadcast details, authority and delivery

Official: `systems-and-modules/remote-procedure-call-rpc/{README.md,generic-rpc.md,static-rpc.md,awaitable-rpc.md,fully-local-rpc.md,pre-post-processors.md}` and `systems-and-modules/broadcast.md`.

1. `ServerRpc`: client to server, ownership requirement can be controlled by rules/attribute but **do not confuse permission with business validation** (inventory quantity, ammo, move speed).
2. `ObserversRpc`: server to observing clients (sometimes clients may invoke under Network Rules). On dedicated server, the server is not automatically a local client: game-critical changes belong in server logic, with `RunLocally` only when supported and intentionally chosen.
3. `TargetRpc`: directed to specified PlayerID, typically server to one client; check observer/connection preconditions.
4. `BufferLast`: latest RPC call for future recipient, not a full persistent state/history mechanism. Use Sync Types or explicit snapshot if multiple values/interactions must be reconstructed.
5. Channels: ReliableOrdered for reliable ordered events; Unreliable/UnreliableSequenced for replaceable high-frequency updates; tune MTU handling (`UpgradeToReliable`, `Drop`, `Fragment`) and record fragment losses. `Immediate` changes flushing/latency vs batching cost.
6. Static/generic/awaitable/coroutine RPC forms are documented, but their exact support and compiler IL post-processing depend on installed version; verify attributes, return types and codegen.
7. Broadcast: no NetworkIdentity required; connection-scoped messages can run before authentication, player-scoped broadcasts require PlayerID. Unsubscribe to prevent leaked listeners. Never trust unauthenticated payloads.

Tests: host (avoid double local effects), dedicated (server-only state), recipient/observers, loss/reorder, duplicates/reconnect, permission denial, oversized data and serialization errors.
