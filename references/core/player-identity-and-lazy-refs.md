# PlayerIdentity, SyncLazyRef, order of events

**Official sources**: `systems-and-modules/network-identity/playeridentity.md`, `systems-and-modules/network-modules/sync-types/synclazyref.md`, `systems-and-modules/network-manager/connection-and-player-events.md`.

## Fast pick

| Need | Priority | Attention |
| --- | --- | --- |
| Find the representation of a `PlayerID` | `PlayerIdentity<T>.TryGetPlayer` | Authenticated player doesn't necessarily involve ready stage |
| Find the local player | `PlayerIdentity<T>.TryGetLocal` | May not be available before local allocation |
| List Players | `PlayerIdentity<T>.allPlayers` | Registry living; manage spamwn/dispawn/reconnect |
| Identity reference between scenes | `SyncLazyRef<T>` | Reference resolved later, can become again `null` |
| Predicted object reference | `PredictedObjectID` | Do not mix with classic `SyncLazyRef` |

## Targeted examples (API to check on the installed version)

```csharp
// On a class representing a player.
public class PlayerPawn : PlayerIdentity<PlayerPawn> { }

// In server logic after resolving the PlayerID.
if (PlayerPawn.TryGetPlayer(playerId, out var player))
{
    // Use player only in authorized logic. Verify permissions on the server.
}
```

```csharp
// Dans une NetworkBehaviour/NetworkIdentity :
private SyncLazyRef<NetworkIdentity> _target = new();

protected override void OnSpawned(bool asServer)
{
    _target.onChanged += OnTargetChanged;
    if (asServer) _target.value = targetIdentity; // The target must already be spawned.
}

protected override void OnDespawned(bool asServer)
{
    _target.onChanged -= OnTargetChanged;
}

private void OnTargetChanged(NetworkIdentity oldValue, NetworkIdentity newValue)
{
    // A null value means the target is absent, its scene is unloaded or it has despawned.
}
```

These snippets illustrate signatures drawn from docs; they require defined fields and control in Unity. For `SyncLazyRef` the reference is carried by `GlobalNetworkID` (Scene + NetworkID). The **target must be spawed at the time of assignment**, even if the recipient can resolve it later. At the depawn/unload the solved value can become `null` again, and then resolve after return.

## Sequence of events

`onClientConnectionState=Connected` (transport) → authentication → `onPlayerJoined`/reception of `PlayerID` → presence in the scene → `onPlayerLoadedScene` → observations by identity. This is not an immutable global order of all callbacks, but ** distinct conditions**; `onPlayerJoinedScene` reports belonging, not the end of loading. Callbacks with `asServer` can appear twice in host. A subscription after the arrival of players must read `networkManager.players` because past events are not replayed.

## Tests

Client joins late, first joins then reconnects via cookie, scene loaded after attribution `PlayerID`, target in another unloaded scene, target unloading/reloading, owner transfer, host without double initialization.

**status**: illustrative examples not compiled with Unity here.
