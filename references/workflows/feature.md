# Implement a PurrNet feature

## Define the observable outcome

Describe what two clients and a server should see when client A requests an action. State who may change the value, what B receives and what a late joiner restores. Include exceptions such as `ownerOnly`, visibility and `ServerRelay`.

## Inspect before editing

- Check the exact Unity version, `dev.purrnet.purrnet`, addon versions, transport, assemblies, NetworkManager, Network Rules, scenes and prefabs.
- Find existing writers, spawners and subscriptions. A `NetworkTransform` and a custom writer can compete for the same pose.
- Identify whether the object uses classic PurrNet, PurrDiction or a mirror `NetworkIdentity` for data outside prediction.

## Select an API

| Need | Candidate | Verify |
| --- | --- | --- |
| Durable score or health | Server-authoritative `SyncVar` | Owner, initial state and late join |
| Inventory | `SyncList`, with `ownerOnly` for private data | Ownership transfer and the previous owner's retained copy |
| Input to server | `SyncInput<T>` or PurrDiction `INPUT` | Server input validation |
| Transient impact | RPC or `SyncEvent` outside prediction | Observers, channel, buffering and size |
| Mobile avatar | `NetworkTransform` or `PredictedTransform` | One writer per replicated value |
| Audio | `NetworkAudioSource` or a predicted view effect | Registered assets and rollback |
| Deferred reference | `SyncLazyRef`, `GlobalNetworkID` | Target scene absent and then loaded |

Read `references/components/component-selector.md`, `references/core/sync-types-decision.md`, `references/core/messaging-and-mtu.md` and the relevant official pages. Verify signatures against the installed package.

## Set the authority and lifecycle contract

Identify the requester, owner, validator, authoritative writer and recipients. Define timing for late join, reconnect, spawn/despawn, scene loading and pooling. For PurrDiction, follow the [prediction workflow](prediction.md) and the Best Practices.

## Keep the change focused

Extend existing components where possible. Change scenes, prefabs, registries and launch flags when code alone cannot meet the requirement. For Inspector changes, provide exact paths, fields and values. Use the Editor when asset creation depends on Unity-generated GUIDs or metadata.

## Verify

- **G0** Find the API in the installed package and record its version, source and assembly requirements.
- **G1** Compile in Unity and capture the result.
- **G2** Test host and client, including allowed and rejected actions and duplicate callback handling.
- **G3** Exercise the feature on a dedicated server with two clients.
- **G4** Cover late join, reconnect, ownership transfer, scenes, visibility and relevant packet loss.

Report changed files, Inspector setup, authority, observed checks, edge cases and outstanding checks.
