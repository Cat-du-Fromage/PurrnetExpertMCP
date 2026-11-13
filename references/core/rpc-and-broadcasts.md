# RPC and Broadcasts

**Official sources**: `systems-and-modules/remote-procedure-call-rpc/README.md`, `generic-rpc.md`, `static-rpc.md`, `awaitable-rpc.md`, `fully-local-rpc.md`, `pre-post-processors.md`, `systems-and-modules/broadcast.md`.

## Decision
- **`ServerRpc`**: client intent → server, then authorization/validation; do not directly transmit "applied damage" as established facts.
- **`ObserversRpc`**: server to observers of the identity, subject to Network Rules; the logic called on observe does not automatically run on dedicated server; `RunLocally` or explicit server processing for the server state.
- **`TargetRpc`**: to a targeted client, `PlayerID` parameter according to version signature. Buffered calls can help some notifications of late join, but do not replace synchronization of a durable state.
- **Broadcast**: message not linked to an identity (e.g. lobby/connection); subscription/unsubscribe to NetworkManager, distinguish connection vs Player scope (before/after authentication).

RPC can be **static, generic, awaitable and coroutine** according to version/codegen. Examine `RequireOwnership`, `RequireServer`, `RunLocally`, `BufferLast`, `Channel`, `CompressionLevel`, `MtuExceeded`, `Immediate`, arguments and policy of Network Rules. `Unreliable` is not suitable for events whose loss is a lasting change in gameplay. Define recovery and retry validation explicitly.

**PurrDiction**: Never send an ordinary RPC from `Simulate` on each replay. A UI RPC outside simulation can request a server spawn in the predicted hierarchy; see `references/prediction/hierarchy-and-parenting.md`.

## Tests
Latency/loss on Reliable/Unreliable, delivery to non-observers, absence of owner, host duplicate, dedicated and late join; inspect bandwidth for frequent RPC.
